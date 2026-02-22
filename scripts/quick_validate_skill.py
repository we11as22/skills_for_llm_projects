#!/usr/bin/env python3
"""Local quick validator for skill frontmatter and naming rules."""

from __future__ import annotations

import re
import sys
from pathlib import Path

MAX_SKILL_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024  # Roo/Kilo/Cursor docs


def validate_skill(skill_path: Path) -> tuple[bool, str]:
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text()
    if not content.startswith("---"):
        return False, "No YAML frontmatter found"

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter: dict[str, str] = {}
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            return False, f"Invalid frontmatter line: {line}"
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip().strip("\"'")

    name = frontmatter.get("name")
    description = frontmatter.get("description")

    if not isinstance(name, str) or not name.strip():
        return False, "Missing or invalid 'name'"
    if not isinstance(description, str) or not description.strip():
        return False, "Missing or invalid 'description'"

    name = name.strip()
    if not re.match(r"^[a-z0-9-]+$", name):
        return False, "Name should be hyphen-case"
    if name.startswith("-") or name.endswith("-") or "--" in name:
        return False, "Name cannot start/end with hyphen or contain '--'"
    if len(name) > MAX_SKILL_NAME_LENGTH:
        return False, f"Name too long ({len(name)} > {MAX_SKILL_NAME_LENGTH})"

    # Cursor/Roo/Kilo: name must match parent directory name
    dir_name = skill_path.name
    if name != dir_name:
        return False, f"Name '{name}' must match directory name '{dir_name}'"

    desc = description.strip()
    if len(desc) > MAX_DESCRIPTION_LENGTH:
        return False, f"Description too long ({len(desc)} > {MAX_DESCRIPTION_LENGTH})"

    return True, "Skill is valid!"


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: quick_validate_skill.py <skill_directory>")
        return 1

    path = Path(sys.argv[1])
    ok, msg = validate_skill(path)
    print(msg)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
