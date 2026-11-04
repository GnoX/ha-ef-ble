"""
Script to generate/regenerate protocol buffer source code and typing stubs.

Uses `protoc` shipped with `grpcio-tools` so no system install is required.  Typing
stubs are heavily used for typing of device fields and instantly catch errors. They
should not be versioned as they can be quite large and useless at runtime.
"""  # noqa: INP001

from pathlib import Path

from grpc_tools import protoc

from custom_components.ef_ble.eflib import pb

PB_OUT_PATH = Path(pb.__file__).parent


def generate_proto_typedefs():
    """Generate protocol buffer source code along with typing stubs"""
    proto_dir = Path(__file__).parent
    proto_files = [
        file.relative_to(proto_dir).as_posix() for file in proto_dir.glob("*.proto")
    ]
    rc = protoc.main(
        [
            "protoc",
            f"-I={proto_dir}",
            f"--python_out={PB_OUT_PATH}",
            f"--pyi_out={PB_OUT_PATH}",
            *proto_files,
        ]
    )
    if rc != 0:
        raise SystemExit(rc)


if __name__ == "__main__":
    generate_proto_typedefs()
