"""Provide the server."""
import argparse
import logging
import sys
from os import environ as env
from pathlib import Path

import uvicorn
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import JSONResponse

from hypha import __version__ as VERSION
from hypha.asgi import ASGIGateway
from hypha.core.interface import CoreInterface
from hypha.http import HTTPProxy
from hypha.triton import TritonProxy
from hypha.utils import GZipMiddleware, GzipRoute, PatchedCORSMiddleware
from hypha.socketio import SocketIOServer

logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger("server")
logger.setLevel(logging.INFO)

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

ALLOW_HEADERS = [
    "Content-Type",
    "Authorization",
    "Access-Control-Allow-Headers",
    "Origin",
    "Accept",
    "X-Requested-With",
    "Access-Control-Request-Method",
    "Access-Control-Request-Headers",
    "Range",
    # for triton inference server
    "Inference-Header-Content-Length",
    "Accept-Encoding",
    "Content-Encoding",
]
ALLOW_METHODS = ["*"]
EXPOSE_HEADERS = [
    "Inference-Header-Content-Length",
    "Accept-Encoding",
    # "Content-Encoding",
    "Range",
    "Origin",
    "Content-Type",
]


def create_application(allow_origins) -> FastAPI:
    """Set up the server application."""
    # pylint: disable=unused-variable

    app = FastAPI(
        title="ImJoy Core Server",
        description=(
            "A server for managing imjoy plugins and \
                enabling remote procedure calls"
        ),
        version=VERSION,
    )
    app.router.route_class = GzipRoute

    static_folder = str(Path(__file__).parent / "static_files")
    app.mount("/static", StaticFiles(directory=static_folder), name="static")

    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.add_middleware(
        PatchedCORSMiddleware,
        allow_origins=allow_origins,
        allow_methods=ALLOW_METHODS,
        allow_headers=ALLOW_HEADERS,
        expose_headers=EXPOSE_HEADERS,
        allow_credentials=True,
    )
    return app


def start_builtin_services(
    app: FastAPI,
    core_interface: CoreInterface,
    args: argparse.Namespace,
) -> None:
    """Set up the socketio server."""
    # pylint: disable=too-many-arguments,too-many-locals

    def norm_url(url):
        return args.base_path.rstrip("/") + url

    HTTPProxy(core_interface)
    if args.triton_servers:
        TritonProxy(
            core_interface,
            triton_servers=args.triton_servers.split(","),
            allow_origins=args.allow_origins,
        )
    ASGIGateway(
        core_interface,
        allow_origins=args.allow_origins,
        allow_methods=ALLOW_METHODS,
        allow_headers=ALLOW_HEADERS,
        expose_headers=EXPOSE_HEADERS,
    )

    @app.get(args.base_path)
    async def home():
        return {
            "name": "Hypha",
            "version": VERSION,
        }

    @app.get(norm_url("/api/stats"))
    async def stats():
        users = core_interface.get_all_users()
        client_count = len(users)
        return {
            "plugin_count": client_count,
            "workspace_count": len(core_interface.get_all_workspace()),
            "workspaces": [w.get_summary() for w in core_interface.get_all_workspace()],
            "users": [u.id for u in users],
        }

    if args.enable_s3:
        # pylint: disable=import-outside-toplevel
        from hypha.rdf import RDFController
        from hypha.s3 import S3Controller

        s3_controller = S3Controller(
            core_interface,
            endpoint_url=args.endpoint_url,
            access_key_id=args.access_key_id,
            secret_access_key=args.secret_access_key,
            workspace_bucket=args.workspace_bucket,
            executable_path=args.executable_path,
        )

        RDFController(
            core_interface, s3_controller=s3_controller, rdf_bucket=args.rdf_bucket
        )

    if args.enable_server_apps:
        # pylint: disable=import-outside-toplevel
        from hypha.apps import ServerAppController

        ServerAppController(
            core_interface,
            port=args.port,
            apps_dir=args.apps_dir,
            in_docker=args.in_docker,
            endpoint_url=args.endpoint_url,
            access_key_id=args.access_key_id,
            secret_access_key=args.secret_access_key,
            workspace_bucket=args.workspace_bucket,
        )

    @app.get(norm_url("/health/liveness"))
    async def liveness(req: Request) -> JSONResponse:
        try:
            await sio_server.is_alive()
        except Exception:  # pylint: disable=broad-except
            return JSONResponse({"status": "DOWN"}, status_code=503)
        return JSONResponse({"status": "OK"})

    @app.on_event("startup")
    async def startup_event():
        core_interface.event_bus.emit("startup")

    @app.on_event("shutdown")
    def shutdown_event():
        core_interface.event_bus.emit("shutdown")

    # SocketIO server should be the last one to be registered
    # otherwise the server won'te be able to start properly
    sio_server = SocketIOServer(
        core_interface,
        socketio_path=norm_url("/socket.io"),
        allow_origins=args.allow_origins,
    )


def start_server(args):
    """Start the socketio server."""
    if args.allow_origins:
        args.allow_origins = args.allow_origins.split(",")
    else:
        args.allow_origins = env.get("ALLOW_ORIGINS", "*").split(",")
    application = create_application(args.allow_origins)
    local_base_url = f"http://127.0.0.1:{args.port}/{args.base_path.strip('/')}".strip(
        "/"
    )
    if args.public_base_url:
        public_base_url = args.public_base_url.strip("/")
    else:
        public_base_url = local_base_url
    core_interface = CoreInterface(
        application, public_base_url=public_base_url, local_base_url=local_base_url
    )

    start_builtin_services(application, core_interface, args)
    if args.host in ("127.0.0.1", "localhost"):
        print(
            "***Note: If you want to enable access from another host, "
            "please start with `--host=0.0.0.0`.***"
        )
    uvicorn.run(application, host=args.host, port=int(args.port))


def get_argparser():
    """Return the argument parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="host for the hypha server",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=9527,
        help="port for the hypha server",
    )
    parser.add_argument(
        "--allow-origins",
        type=str,
        default="*",
        help="origins for the hypha server",
    )
    parser.add_argument(
        "--base-path",
        type=str,
        default="/",
        help="the base path for the server",
    )
    parser.add_argument(
        "--public-base-url",
        type=str,
        default=None,
        help="the public base URL for accessing the server",
    )
    parser.add_argument(
        "--triton-servers",
        type=str,
        default=None,
        help="A list of comma separated Triton servers to proxy",
    )
    parser.add_argument(
        "--enable-server-apps",
        action="store_true",
        help="enable server applications",
    )
    parser.add_argument(
        "--enable-s3",
        action="store_true",
        help="enable S3 object storage",
    )
    parser.add_argument(
        "--in-docker",
        action="store_true",
        help="Indicate whether running in docker (e.g. "
        "server apps will run without sandboxing)",
    )
    parser.add_argument(
        "--endpoint-url",
        type=str,
        default=None,
        help="set endpoint URL for S3",
    )
    parser.add_argument(
        "--access-key-id",
        type=str,
        default=None,
        help="set AccessKeyID for S3",
    )
    parser.add_argument(
        "--secret-access-key",
        type=str,
        default=None,
        help="set SecretAccessKey for S3",
    )
    parser.add_argument(
        "--apps-dir",
        type=str,
        default="hypha-apps",
        help="temporary directory for storing installed apps",
    )
    parser.add_argument(
        "--rdf-bucket",
        type=str,
        default="hypha-rdfs",
        help="S3 bucket for storing RDF files",
    )
    parser.add_argument(
        "--workspace-bucket",
        type=str,
        default="hypha-workspaces",
        help="S3 bucket for storing workspaces",
    )
    parser.add_argument(
        "--executable-path",
        type=str,
        default="bin",
        help="temporary directory for storing executables (e.g. mc, minio)",
    )
    return parser


if __name__ == "__main__":
    arg_parser = get_argparser()
    opt = arg_parser.parse_args()
    start_server(opt)
