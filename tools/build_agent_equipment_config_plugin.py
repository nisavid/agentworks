#!/usr/bin/env python3.14
"""Refresh the installed plugin's runtime snapshot from canonical sources."""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "plugins/agent-equipment-config/mcp/runtime/tools"
SOURCES = ("agent_equipment_config.py", "agent_equipment_config_mcp_server.py")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="report stale files without writing")
    args = parser.parse_args()
    expected = {name: (ROOT / "tools" / name).read_bytes() for name in SOURCES}
    expected["__init__.py"] = b""
    for directory in (BUNDLE, *BUNDLE.parents):
        if directory.is_symlink():
            parser.error(f"runtime bundle directory must not be a symlink: {directory}")
    unexpected = []
    for directory, allowed in [(BUNDLE.parent, {"tools"}), (BUNDLE, set(expected))]:
        if not directory.is_dir():
            continue
        try:
            for entry in directory.iterdir():
                if entry.name in allowed:
                    continue
                if entry.name == "__pycache__" and not entry.is_symlink() and entry.is_dir():
                    continue
                unexpected.append(entry.relative_to(BUNDLE.parent).as_posix())
        except OSError as error:
            parser.error(f"cannot inspect runtime bundle: {error}")
    if unexpected:
        print("Plugin runtime snapshot contains unexpected entries: " + ", ".join(sorted(unexpected)))
        return 1
    stale = []
    for name, content in expected.items():
        target = BUNDLE / name
        if target.is_file() and not target.is_symlink() and target.read_bytes() == content:
            continue
        stale.append(name)
        if not args.check:
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.is_symlink():
                target.unlink()
            target.write_bytes(content)
    if args.check and stale:
        print("Plugin runtime snapshot is stale: " + ", ".join(stale))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
