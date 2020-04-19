import os

from rpc.server import start

if __name__ == "__main__":
    start(
        os.environ.get("GRPC_HOST", "0.0.0.0"),
        os.environ.get("GRPC_PORT", "5001")
    )
