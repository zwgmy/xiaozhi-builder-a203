#!/usr/bin/env python3
"""Apply the A203 board integration to a pinned XiaoZhi upstream checkout."""

from pathlib import Path
import shutil
import sys

UPSTREAM_COMMIT = "67ca62d4bb7d91e514d7ccd5e6977745002f41f4"
BOARD_SYMBOL = "BOARD_TYPE_A203"


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: prepare_upstream.py <xiaozhi-esp32-checkout>")

    repo_root = Path(__file__).resolve().parents[1]
    upstream = Path(sys.argv[1]).resolve()
    board_source = repo_root / "main" / "boards" / "a203"
    board_target = upstream / "main" / "boards" / "a203"

    required = [
        upstream / "main" / "Kconfig.projbuild",
        upstream / "main" / "CMakeLists.txt",
        board_source / "config.h",
        board_source / "config.json",
        board_source / "a203_board.cc",
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit("Required file(s) missing:\n" + "\n".join(missing))

    shutil.copytree(board_source, board_target, dirs_exist_ok=True)

    kconfig_path = upstream / "main" / "Kconfig.projbuild"
    kconfig = kconfig_path.read_text(encoding="utf-8")
    if f"config {BOARD_SYMBOL}" not in kconfig:
        choice_start = kconfig.find("choice BOARD_TYPE")
        choice_end = kconfig.find("endchoice", choice_start)
        if choice_start < 0 or choice_end < 0:
            raise SystemExit("Could not locate BOARD_TYPE Kconfig choice")
        entry = (
            '    config BOARD_TYPE_A203\n'
            '        bool "Ai-Thinker ESP-S3-12K-KIT A203"\n'
            '        depends on IDF_TARGET_ESP32S3\n'
        )
        kconfig = kconfig[:choice_end] + entry + kconfig[choice_end:]
        kconfig_path.write_text(kconfig, encoding="utf-8")

    cmake_path = upstream / "main" / "CMakeLists.txt"
    cmake = cmake_path.read_text(encoding="utf-8")
    if "CONFIG_BOARD_TYPE_A203" not in cmake:
        marker = 'if(NOT BOARD_DIR AND NOT CMAKE_BUILD_EARLY_EXPANSION)'
        if marker not in cmake:
            raise SystemExit("Could not locate board selection terminator in main/CMakeLists.txt")
        marker_pos = cmake.find(marker)
        chain_end = cmake.rfind("endif()", 0, marker_pos)
        if chain_end < 0:
            raise SystemExit("Could not locate end of board selection if/elseif chain")
        entry = (
            'elseif(CONFIG_BOARD_TYPE_A203)\n'
            '    set(BOARD_DIR "a203")\n'
        )
        cmake = cmake[:chain_end] + entry + cmake[chain_end:]
        cmake_path.write_text(cmake, encoding="utf-8")

    print(f"A203 board copied to {board_target}")
    print(f"Registered {BOARD_SYMBOL} in Kconfig and CMake")
    print(f"Upstream expected commit: {UPSTREAM_COMMIT}")


if __name__ == "__main__":
    main()
