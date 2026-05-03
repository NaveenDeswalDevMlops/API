"""Single entry-point for the GraphQL Book service demo.

Usage:
    python main.py serve      # Start only the API server
    python main.py demo       # Start server + run CRUD client flow automatically
"""

from __future__ import annotations

import argparse
import threading
import time

import uvicorn

import graphql_client
from graphql_server import app


def run_server(host: str = "127.0.0.1", port: int = 8000):
    uvicorn.run(app, host=host, port=port, log_level="info")


def run_demo(host: str = "127.0.0.1", port: int = 8000):
    server_thread = threading.Thread(
        target=run_server,
        kwargs={"host": host, "port": port},
        daemon=True,
    )
    server_thread.start()

    # Give the server a moment to boot.
    time.sleep(1.5)

    graphql_client.GRAPHQL_URL = f"http://{host}:{port}/graphql"
    graphql_client.main()


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
    else:
        run_demo(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
