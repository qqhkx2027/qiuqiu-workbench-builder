#!/usr/bin/env python3
"""Small dependency-free validator for a distributable Codex-style skill."""

from pathlib import Path
import re
import sys


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors: list[str] = []
    skill = root / "SKILL.md"
    if not skill.is_file():
        errors.append("missing SKILL.md")
    else:
        text = skill.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            errors.append("SKILL.md must start with YAML frontmatter")
        else:
            closing = text.find("\n---", 4)
            frontmatter = text[4:closing] if closing != -1 else ""
            if closing == -1:
                errors.append("SKILL.md frontmatter is not closed")
            for field in ("name", "description"):
                match = re.search(rf"^{field}:\s*(.+)$", frontmatter, re.MULTILINE)
                if not match or not match.group(1).strip().strip('"\''):
                    errors.append(f"frontmatter field is missing: {field}")

        for target in re.findall(r"\]\(([^)]+)\)", text):
            target = target.split("#", 1)[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:", "/")):
                continue
            if not (root / target).exists():
                errors.append(f"broken relative link: {target}")

    agent_config = root / "agents" / "openai.yaml"
    if agent_config.exists() and "interface:" not in agent_config.read_text(encoding="utf-8"):
        errors.append("agents/openai.yaml is missing interface section")

    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Skill validation passed: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
