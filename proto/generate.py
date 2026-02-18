"""
Script to generate/regenerate protocol buffer source code and typing stubs

Typing stubs are used heavily for typing of device fields and can instantly catch
errors. However, they should not be versioned as they can be quite large and completely
useless for runtime.

This script requires `protoc` to be installed, see https://protobuf.dev/installation/
"""  # noqa: INP001

import subprocess
from pathlib import Path

from custom_components.ef_ble.eflib import pb

PB_OUT_PATH = Path(pb.__file__).parent


def generate_proto_typedefs():
    """Generate protocol buffer source code along with typing stubs"""
    proto_dir = Path(__file__).parent
    proto_files = [
        file.relative_to(proto_dir).as_posix() for file in proto_dir.glob("*.proto")
    ]
    subprocess.run(
        [
            "protoc",
            f"-I={proto_dir}",
            f"--python_out={PB_OUT_PATH}",
            f"--pyi_out={PB_OUT_PATH}",
            *proto_files,
        ],
        check=True,
    )


if __name__ == "__main__":
    generate_proto_typedefs()
