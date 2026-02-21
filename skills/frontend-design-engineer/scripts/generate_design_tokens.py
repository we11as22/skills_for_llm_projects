#!/usr/bin/env python3
"""Generate CSS variables and TS token exports from a JSON token file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def flatten(prefix: str, obj: dict, out: dict[str, str]) -> None:
    for key, value in obj.items():
        token = f"{prefix}-{key}" if prefix else key
        if isinstance(value, dict):
            flatten(token, value, out)
        else:
            out[token] = str(value)


def write_css(tokens: dict[str, str], output: Path) -> None:
    lines = [":root {"]
    for key, value in sorted(tokens.items()):
        lines.append(f"  --{key}: {value};")
    lines.append("}")
    output.write_text("\n".join(lines) + "\n")


def write_ts(tokens: dict[str, str], output: Path) -> None:
    lines = ["export const tokens = {"]
    for key, value in sorted(tokens.items()):
        lines.append(f'  "{key}": "{value}",')
    lines.append("} as const;\n")
    output.write_text("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON token file")
    parser.add_argument("--css-out", type=Path, default=Path("tokens.css"))
    parser.add_argument("--ts-out", type=Path, default=Path("tokens.ts"))
    args = parser.parse_args()

    data = json.loads(args.input.read_text())
    if not isinstance(data, dict):
        raise SystemExit("Token file must contain a JSON object")

    flattened: dict[str, str] = {}
    flatten("", data, flattened)
    write_css(flattened, args.css_out)
    write_ts(flattened, args.ts_out)
    print(f"Generated {len(flattened)} tokens -> {args.css_out}, {args.ts_out}")


if __name__ == "__main__":
    main()
