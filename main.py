"""Single entry-point for the GraphQL Book service demo.

Usage:
    python main.py serve      # Start only the API server
    python main.py demo       # Start server + run CRUD client flow automatically
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time

import requests
import uvicorn

import graphql_client
from graphql_server import app


def run_server(host: str = "127.0.0.1", port: int = 8000):
    uvicorn.run(app, host=host, port=port, log_level="info")


def wait_for_server(url: str, timeout: int = 15) -> None:
    deadline = time.monotonic() + timeout
    last_error: Exception | None = None

    while time.monotonic() < deadline:
        try:
            response = requests.get(url, timeout=1)
            if response.status_code == 200:
                print(f"Server is ready: {url}")
                return
        except requests.RequestException as exc:
            last_error = exc

    raise RuntimeError(f"Server did not become ready within {timeout}s at {url}. Last error: {last_error}")


def run_demo(host: str = "127.0.0.1", port: int = 8000):
    server_cmd = [
        "uvicorn",
        "graphql_server:app",
        "--host",
        host,
        "--port",
        str(port),
    ]
    server_process = subprocess.Popen(server_cmd)

    try:
        wait_for_server(f"http://{host}:{port}/health", timeout=15)
        graphql_client.GRAPHQL_URL = f"http://{host}:{port}/graphql"
        graphql_client.main()
    finally:
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()
            server_process.wait(timeout=5)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Book GraphQL demo launcher")
    parser.add_argument(
        "mode",
        choices=["serve", "demo"],
        help="serve: run only server, demo: run server and execute CRUD client flow",
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8000, type=int)
    return parser.parse_args()


def main():
    args = parse_args()
    if args.mode == "serve":
        run_server(host=args.host, port=args.port)
    elif args.mode == "demo":
        run_demo(host=args.host, port=args.port)
    else:
        print(f"Unsupported mode: {args.mode}", file=sys.stderr)
        raise SystemExit(2)


if __name__ == "__main__":
    main()
