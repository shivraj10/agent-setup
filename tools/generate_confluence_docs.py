"""Generate code documentation from the project source tree (PUBLIC version).

Same as generate_confluence_docs.py but excludes proprietary modules
(genai/, smart_insight/, conversational_bi/, etc.) so the output is safe
for public sharing.

Usage:
    python tools/generate_confluence_docs_public.py                    # combined markdown to stdout
    python tools/generate_confluence_docs_public.py --out docs.md      # combined markdown to file
    python tools/generate_confluence_docs_public.py --sections-dir out/ # one .md file per section
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Ensure project root is importable
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

from ast_tools import ClassInfo, FunctionInfo, ModuleInfo, parse_ast

# ── Configuration ────────────────────────────────────────────────────

SRC_DIR = PROJECT_ROOT / "src"

# Directories to EXCLUDE from public documentation.
# Paths are relative to src/, use forward slashes.
EXCLUDED_DIRS: set[str] = {
    # Internal architecture / infrastructure
    "middleware",
    "secret_manager",
    "observability",
    "websocket_handler",
}

# Individual files to EXCLUDE (relative to src/, forward slashes).
EXCLUDED_FILES: set[str] = set()

# Friendly display names for top-level directories.
DIR_DISPLAY_NAMES: dict[str, str] = {
    "apis": "API Routes",
    "apis/routes": "API Routes",
    "apis/mock_data": "API Mock Data",
    "components": "Shared Components",
    "database": "Database Layer",
    "genai": "GenAI — Common",
    "middleware": "Middleware",
    "models": "Pydantic Models",
    "observability": "Observability & Logging",
    "secret_manager": "Secret Manager",
    "websocket_handler": "WebSocket Handler",
}


# ── Auto-discovery ───────────────────────────────────────────────────


def _is_excluded(rel_dir: str) -> bool:
    """Check if a directory (relative to src/) should be excluded."""
    normalised = rel_dir.replace("\\", "/")
    for excluded in EXCLUDED_DIRS:
        if normalised == excluded or normalised.startswith(excluded + "/"):
            return True
    return False


def _dir_display_name(rel_dir: str) -> str:
    """Return a human-readable section title for a directory path."""
    if rel_dir in DIR_DISPLAY_NAMES:
        return DIR_DISPLAY_NAMES[rel_dir]
    return rel_dir.replace("/", " — ").replace("_", " ").title()


def discover_modules(src_dir: Path) -> list[tuple[str, list[Path]]]:
    """Walk src/ and group Python files by their immediate directory.

    Returns a list of (section_title, [file_paths]) sorted by directory
    depth then name.  Root-level files go under "Application Entry Point".
    Excludes directories listed in EXCLUDED_DIRS.
    """
    groups: dict[str, list[Path]] = {}

    for py_file in sorted(src_dir.rglob("*.py")):
        if py_file.name == "__pycache__":
            continue
        if "__pycache__" in py_file.parts:
            continue

        rel = py_file.relative_to(src_dir)
        rel_dir = str(rel.parent).replace("\\", "/")

        # Skip excluded directories
        if rel_dir != "." and _is_excluded(rel_dir):
            continue

        if rel_dir == ".":
            section = "Application Entry Point"
        else:
            section = _dir_display_name(rel_dir)

        groups.setdefault(section, []).append(py_file)

    # Sort by directory depth (shallow first), then alphabetically
    def _sort_key(item: tuple[str, list[Path]]) -> tuple[int, str]:
        first_file = item[1][0]
        rel = first_file.relative_to(src_dir)
        return (len(rel.parts), item[0])

    return sorted(groups.items(), key=_sort_key)


def discover_assets(src_dir: Path, extension: str) -> list[tuple[str, list[Path]]]:
    """Discover .sql or .yaml/.yml files grouped by directory."""
    groups: dict[str, list[Path]] = {}

    for asset in sorted(src_dir.rglob(f"*{extension}")):
        if "__pycache__" in asset.parts:
            continue
        rel = asset.relative_to(src_dir)
        rel_dir = str(rel.parent).replace("\\", "/")

        # Skip excluded directories
        if _is_excluded(rel_dir):
            continue

        section = _dir_display_name(rel_dir)
        groups.setdefault(section, []).append(asset)

    def _sort_key(item: tuple[str, list[Path]]) -> tuple[int, str]:
        first_file = item[1][0]
        rel = first_file.relative_to(src_dir)
        return (len(rel.parts), item[0])

    return sorted(groups.items(), key=_sort_key)


# ── Markdown generation ──────────────────────────────────────────────
def _format_signature(func: FunctionInfo) -> str:
    """Return a one-line signature string like ``async def foo(a, b) -> str``."""
    prefix = "async def" if func.is_async else "def"
    args = ", ".join(func.args)
    ret = f" -> {func.returns}" if func.returns else ""
    return f"{prefix} {func.name}({args}){ret}"


def _format_decorators(decorators: list[str]) -> str:
    if not decorators:
        return ""
    return "\n".join(f"@{d}" for d in decorators) + "\n"


def _render_function(func: FunctionInfo, indent: int = 0) -> str:
    """Render a single function as a markdown block."""
    lines: list[str] = []
    prefix = "  " * indent
    sig = _format_signature(func)
    lines.append(f"{prefix}- `{sig}`")
    if func.docstring:
        first_line = func.docstring.strip().split("\n")[0]
        lines.append(f"{prefix}  — {first_line}")
    return "\n".join(lines)


def _render_class(cls: ClassInfo) -> str:
    """Render a class and its methods."""
    lines: list[str] = []
    bases = f"({', '.join(cls.bases)})" if cls.bases else ""
    lines.append(f"#### `class {cls.name}{bases}`")
    if cls.docstring:
        first_line = cls.docstring.strip().split("\n")[0]
        lines.append(f"> {first_line}")
    if cls.methods:
        public = [
            m
            for m in cls.methods
            if not m.name.startswith("_") or m.name in ("__init__",)
        ]
        if public:
            lines.append("")
            lines.append("**Methods:**")
            for method in public:
                lines.append(_render_function(method, indent=0))
    return "\n".join(lines)


def _render_module(info: ModuleInfo, display_name: str) -> str:
    """Render one module's documentation."""
    lines: list[str] = []
    lines.append(f"### `{display_name}`")
    if info.docstring:
        first_line = info.docstring.strip().split("\n")[0]
        lines.append(f"*{first_line}*")
    lines.append(f"- Lines: {info.total_lines}")
    lines.append("")

    if info.classes:
        for cls in info.classes:
            lines.append(_render_class(cls))
            lines.append("")

    top_funcs = [f for f in info.functions if not f.name.startswith("_")]
    if top_funcs:
        lines.append("**Module-level functions:**")
        for func in top_funcs:
            lines.append(_render_function(func))
        lines.append("")

    return "\n".join(lines)


def generate_section_markdown(title: str, py_files: list[Path]) -> str:
    """Generate markdown for a single section (one directory group)."""
    lines: list[str] = []
    lines.append(f"# {title}")
    lines.append("")

    for py_file in py_files:
        rel = py_file.relative_to(SRC_DIR)
        display = str(rel).replace("\\", "/")
        try:
            info = parse_ast(str(py_file))
            lines.append(_render_module(info, display))
        except SyntaxError as exc:
            lines.append(f"### `{display}` *(parse error: {exc})*\n")

    return "\n".join(lines)


def generate_assets_markdown() -> str:
    """Generate markdown for SQL queries and YAML prompt templates."""
    lines: list[str] = []

    # SQL
    sql_groups = discover_assets(SRC_DIR, ".sql")
    if sql_groups:
        lines.append("# SQL Queries")
        lines.append("")
        for section, files in sql_groups:
            file_names = sorted(f.name for f in files)
            lines.append(f"**{section}:** {', '.join(f'`{f}`' for f in file_names)}")
            lines.append("")

    # YAML prompts
    yaml_groups = discover_assets(SRC_DIR, ".yaml")
    yml_groups = discover_assets(SRC_DIR, ".yml")
    all_prompt_groups: dict[str, list[str]] = {}
    for section, files in yaml_groups + yml_groups:
        all_prompt_groups.setdefault(section, []).extend(f.name for f in files)

    if all_prompt_groups:
        lines.append("# Prompt Templates")
        lines.append("")
        for section, file_names in sorted(all_prompt_groups.items()):
            lines.append(f"**{section}:**")
            for name in sorted(set(file_names)):
                lines.append(f"- `{name}`")
            lines.append("")

    return "\n".join(lines)


def generate_combined_markdown() -> str:
    """Generate a single combined markdown document for the entire project."""
    sections: list[str] = []

    sections.append("# Digital Donor Journey — Code Reference (Public)")
    sections.append("")
    sections.append("> Auto-generated from the source code. GenAI modules excluded.")
    sections.append("")

    module_groups = discover_modules(SRC_DIR)

    # TOC
    sections.append("## Table of Contents")
    for title, _ in module_groups:
        anchor = title.lower().replace(" ", "-").replace("—", "").replace("  ", "-")
        sections.append(f"- [{title}](#{anchor})")
    sections.append("- [SQL Queries](#sql-queries)")
    sections.append("- [Prompt Templates](#prompt-templates)")
    sections.append("")
    sections.append("---")
    sections.append("")

    # Module sections
    for title, py_files in module_groups:
        sections.append(f"## {title}")
        sections.append("")
        for py_file in py_files:
            rel = py_file.relative_to(SRC_DIR)
            display = str(rel).replace("\\", "/")
            try:
                info = parse_ast(str(py_file))
                sections.append(_render_module(info, display))
            except SyntaxError as exc:
                sections.append(f"### `{display}` *(parse error: {exc})*\n")

    # Assets
    sections.append(generate_assets_markdown())

    return "\n".join(sections)


def generate_section_files(output_dir: Path) -> list[dict[str, str]]:
    """Write one .md file per section into output_dir.

    Returns a manifest list of {title, filename, path} for each section.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest: list[dict[str, str]] = []

    module_groups = discover_modules(SRC_DIR)

    for title, py_files in module_groups:
        slug = (
            title.lower()
            .replace(" ", "_")
            .replace("—", "")
            .replace("__", "_")
            .strip("_")
        )
        filename = f"{slug}.md"
        content = generate_section_markdown(title, py_files)
        (output_dir / filename).write_text(content, encoding="utf-8")
        manifest.append(
            {"title": title, "filename": filename, "path": str(output_dir / filename)}
        )

    # Assets section
    assets_md = generate_assets_markdown()
    if assets_md.strip():
        (output_dir / "sql_and_prompts.md").write_text(assets_md, encoding="utf-8")
        manifest.append(
            {
                "title": "SQL Queries & Prompt Templates",
                "filename": "sql_and_prompts.md",
                "path": str(output_dir / "sql_and_prompts.md"),
            }
        )

    # Write manifest
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    return manifest


# ── CLI ──────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate public code documentation (excludes GenAI modules)"
    )
    parser.add_argument("--out", type=str, help="Write combined markdown to a file")
    parser.add_argument(
        "--sections-dir",
        type=str,
        help="Write per-section .md files into this directory",
    )
    args = parser.parse_args()

    if args.sections_dir:
        manifest = generate_section_files(Path(args.sections_dir))
        print(f"✓ Generated {len(manifest)} section files in {args.sections_dir}/")
        print(f"  Manifest: {args.sections_dir}/manifest.json")
        for entry in manifest:
            print(f"  - {entry['title']} → {entry['filename']}")
    else:
        markdown = generate_combined_markdown()
        if args.out:
            Path(args.out).write_text(markdown, encoding="utf-8")
            print(f"✓ Written to {args.out}")
        else:
            print(markdown)


if __name__ == "__main__":
    main()
