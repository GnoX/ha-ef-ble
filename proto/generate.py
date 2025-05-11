import subprocess  # noqa: INP001
from pathlib import Path

from custom_components.ef_ble.eflib import pb

PB_OUT_PATH = Path(pb.__file__).parent


def generate_proto_typedefs():
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

    subprocess.run(["ruff", "format", f"{PB_OUT_PATH}"], check=False)


if __name__ == "__main__":
    generate_proto_typedefs()
