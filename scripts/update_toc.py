import os
import re
from typing import List, Tuple


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


HEADING_RE = re.compile(r"^(#+)\s+(.*\S)\s*$")


def slugify_github(text: str, used: dict) -> str:
    """Convert heading text to a GitHub-style anchor, tracking duplicates."""
    # Strip leading/trailing spaces
    text = text.strip().lower()
    # Remove markdown inline formatting characters that don't affect the visible text
    # but keep letters, digits, spaces, hyphens and underscores.
    text = re.sub(r"[^\w\- ]+", "", text)
    # Replace spaces with hyphens
    text = re.sub(r"\s+", "-", text)
    # Collapse multiple hyphens
    text = re.sub(r"-{2,}", "-", text)
    # Trim stray hyphens
    text = text.strip("-")
    base = text
    if base in used:
        used[base] += 1
        text = f"{base}-{used[base]}"
    else:
        used[base] = 0
    return text


def extract_headings(lines: List[str]) -> List[Tuple[int, int, str]]:
    """Return list of (index, level, text) for headings, skipping the main title (# ...)."""
    headings = []
    for i, line in enumerate(lines):
        m = HEADING_RE.match(line)
        if not m:
            continue
        level = len(m.group(1))
        text = m.group(2)
        if level == 1:
            # Skip document title in TOC by default
            continue
        headings.append((i, level, text))
    return headings


def find_toc_region(lines: List[str]) -> Tuple[int, int, int]:
    """
    Find an existing TOC region.
    Returns (toc_heading_index, toc_content_start, toc_content_end_exclusive)
    or (-1, -1, -1) if not found.
    """
    toc_idx = -1
    toc_level = None
    for i, line in enumerate(lines):
        stripped = line.strip().lower()
        if stripped.startswith("## ") or stripped.startswith("### "):
            # Heading line
            level = 2 if stripped.startswith("## ") else 3
            heading_text = stripped.lstrip("#").strip()
            if heading_text in ("table of contents", "contents"):
                toc_idx = i
                toc_level = level
                break
    if toc_idx == -1:
        return -1, -1, -1

    # TOC content starts after the heading line and any immediate blank line
    start = toc_idx + 1
    if start < len(lines) and lines[start].strip() == "":
        start += 1

    # TOC ends before the next heading of same or higher level (or EOF)
    end = len(lines)
    for j in range(start, len(lines)):
        m = HEADING_RE.match(lines[j])
        if not m:
            continue
        level = len(m.group(1))
        if level <= toc_level:
            end = j
            break
    return toc_idx, start, end


def build_toc_lines(headings: List[Tuple[int, int, str]]) -> List[str]:
    used: dict = {}
    toc_lines: List[str] = []
    for _, level, text in headings:
        anchor = slugify_github(text, used)
        # Start TOC from level 2 (##). Deeper levels are indented.
        indent = max(0, level - 2) * 2 * " "
        toc_lines.append(f"{indent}- [{text}](#{anchor})\n")
    return toc_lines


def find_insert_position(lines: List[str]) -> int:
    """
    Decide where to insert a new TOC:
    - After a leading YAML front-matter block if present.
    - Otherwise, after the first level-1 heading and any following blank line.
    - Fallback to start of document.
    """
    # YAML front-matter
    if len(lines) >= 3 and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                # Insert after closing '---'
                return i + 1

    # After first main title
    for i, line in enumerate(lines):
        m = HEADING_RE.match(line)
        if m and len(m.group(1)) == 1:
            pos = i + 1
            # Skip an immediate blank line
            if pos < len(lines) and lines[pos].strip() == "":
                pos += 1
            return pos

    return 0


def process_file(path: str) -> bool:
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    headings = extract_headings(lines)
    if not headings:
        return False

    toc_idx, toc_start, toc_end = find_toc_region(lines)
    toc_lines = build_toc_lines(headings)

    if toc_idx == -1:
        # Insert a new TOC
        insert_at = find_insert_position(lines)
        new_lines = (
            lines[:insert_at]
            + ["\n" if insert_at > 0 and lines[insert_at - 1].strip() != "" else ""]
            + ["## Table of Contents\n", "\n"]
            + toc_lines
            + ["\n"]
            + lines[insert_at:]
        )
    else:
        # Replace existing TOC content, keep heading line
        new_lines = (
            lines[:toc_idx + 1]
            + ["\n"]
            + toc_lines
            + ["\n"]
            + lines[toc_end:]
        )

    if new_lines == lines:
        return False

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.writelines(new_lines)
    return True


def is_markdown_file(path: str) -> bool:
    return path.lower().endswith(".md")


def main() -> None:
    changed_files = []
    for root, dirs, files in os.walk(ROOT_DIR):
        # Skip typical non-doc directories if present
        dirs[:] = [d for d in dirs if d not in {".git", ".cursor", "node_modules", ".venv", "venv", "__pycache__"}]
        for name in files:
            if not is_markdown_file(name):
                continue
            path = os.path.join(root, name)
            if process_file(path):
                changed_files.append(os.path.relpath(path, ROOT_DIR))

    if changed_files:
        print("Updated TOC in:")
        for p in changed_files:
            print(f" - {p}")
    else:
        print("No TOC changes were necessary.")


if __name__ == "__main__":
    main()

