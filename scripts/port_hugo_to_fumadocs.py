#!/usr/bin/env python3
"""Port the GPandas Hugo (LotusDocs) content tree to Fumadocs MDX.

Usage:
    python3 scripts/port_hugo_to_fumadocs.py <hugo-content-dir> <fumadocs-content-docs-dir>

What it does
------------
* `_index.md` -> `index.mdx`, every other `*.md` -> `*.mdx`, preserving the
  multi-level folder structure exactly as it is in the Hugo site.
* Writes a `meta.json` per folder so Fumadocs reproduces the Hugo `weight`
  ordering of both sections and pages.
* Rewrites Hugo constructs that MDX cannot parse:
  - `{{< ref "slug" >}}` shortcodes  -> real `/docs/...` URLs
  - `<!-- html comments -->`         -> `{/* mdx comments */}`
  - stray `<` in prose (`<nil>`, `<= n`, `(<1000 rows)`) -> `&lt;`
  - `<iframe style="...">`           -> JSX-compatible `style={{...}}`
  - LotusDocs `&nbsp;` spacer lines  -> removed (Fumadocs handles spacing)
* Maps Material Symbols icon names in frontmatter to lucide-react icon names.

Fenced code blocks (including ```mermaid) are never modified.
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

# --------------------------------------------------------------------------
# Material Symbols (LotusDocs) -> lucide-react icon names
# --------------------------------------------------------------------------
ICON_MAP = {
    "menu_book": "BookOpen",
    "rocket_launch": "Rocket",
    "upload_file": "FileUp",
    "import_export": "ArrowUpDown",
    "database": "Database",
    "table_chart": "Table",
    "add_box": "SquarePlus",
    "tune": "SlidersHorizontal",
    "post_add": "FilePlus",
    "transform": "Shuffle",
    "filter_alt": "Funnel",
    "checklist": "ListChecks",
    "sort": "ArrowDownUp",
    "label": "Tag",
    "pin_drop": "MapPin",
    "cleaning_services": "Eraser",
    "filter_none": "CopyMinus",
    "swap_horiz": "ArrowLeftRight",
    "calculate": "Calculator",
    "query_stats": "ChartColumn",
    "insights": "ChartLine",
    "workspaces": "Boxes",
    "timeline": "Activity",
    "pivot_table_chart": "Table2",
    "layers": "Layers",
    "join_inner": "Combine",
    "text_fields": "Type",
    "calendar_month": "Calendar",
    "category": "Tags",
    "bar_chart": "ChartBar",
    "view_column": "Columns3",
}

FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
REF_RE = re.compile(r"\{\{<\s*ref\s+\"([^\"]+)\"\s*>\}\}")
COMMENT_RE = re.compile(r"<!--(.*?)-->", re.DOTALL)
IFRAME_RE = re.compile(r"<iframe\b([^>]*)>\s*</iframe>", re.IGNORECASE)
ATTR_RE = re.compile(r'([a-zA-Z-]+)\s*=\s*"([^"]*)"')

# JSX tags that we deliberately keep as markup. Any other `<` in prose is a
# literal less-than sign (e.g. `<= rowCount`, `(<1000 rows)`) and has to be
# escaped, otherwise MDX tries to parse it as a JSX element.
KEEP_TAG_RE = re.compile(r"</?(?:br|iframe|Mermaid|Callout|Cards?|Steps?|Tabs?|Tab|Accordions?)\b")
LT_RE = re.compile(r"<")


# --------------------------------------------------------------------------
# Frontmatter
# --------------------------------------------------------------------------
def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Very small YAML-front-matter reader (flat `key: value` pairs only)."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    raw = text[3:end]
    body = text[end + 4 :]
    if body.startswith("\n"):
        body = body[1:]

    data: dict[str, str] = {}
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        data[key.strip()] = value
    return data, body


def dump_frontmatter(data: dict[str, str]) -> str:
    lines = ["---"]
    for key in ("title", "description", "icon"):
        if key in data and data[key]:
            value = data[key].replace("\\", "\\\\").replace('"', '\\"')
            lines.append(f'{key}: "{value}"')
    lines.append("---")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Body rewriting
# --------------------------------------------------------------------------
def to_camel(name: str) -> str:
    head, *rest = name.split("-")
    return head + "".join(part.capitalize() for part in rest)


def jsx_iframe(match: re.Match[str]) -> str:
    """Rewrite an HTML iframe into a JSX-compatible one."""
    attrs = dict(ATTR_RE.findall(match.group(1)))
    style = attrs.pop("style", "")

    parts: list[str] = []
    for key, value in attrs.items():
        name = {"class": "className"}.get(key, to_camel(key))
        parts.append(f'{name}="{value}"')

    if style:
        decls = []
        for decl in style.split(";"):
            if ":" not in decl:
                continue
            prop, _, val = decl.partition(":")
            decls.append(f"{to_camel(prop.strip())}: '{val.strip()}'")
        if decls:
            parts.append("style={{ " + ", ".join(decls) + " }}")

    return "<iframe " + " ".join(parts) + " />"


def escape_stray_lt(text: str) -> str:
    """Escape `<` characters that do not open a tag we want to keep."""

    def repl(match: re.Match[str]) -> str:
        if KEEP_TAG_RE.match(text, match.start()):
            return "<"
        return "&lt;"

    return LT_RE.sub(repl, text)


def rewrite_body(body: str, ref_urls: dict[str, str], source: Path) -> str:
    """Apply MDX-safety rewrites to everything outside fenced code blocks."""
    lines = body.splitlines()
    out: list[str] = []
    fence: str | None = None

    for line in lines:
        match = FENCE_RE.match(line)

        if fence is not None:
            out.append(line)
            if match and match.group(1).startswith(fence):
                fence = None
            continue

        if match:
            fence = match.group(1)[0] * 3
            out.append(line)
            continue

        # LotusDocs used bare `&nbsp;` paragraphs purely as vertical spacers.
        if line.strip() == "&nbsp;":
            continue

        # {{< ref "slug" >}} -> /docs/<section>/<slug>
        def resolve(m: re.Match[str]) -> str:
            target = m.group(1)
            slug, _, anchor = target.partition("#")
            slug = slug.strip().strip("/")
            slug = re.sub(r"\.md$", "", slug)
            url = ref_urls.get(slug)
            if url is None:
                raise SystemExit(
                    f"{source}: unresolved Hugo ref {target!r}. "
                    f"Known slugs: {sorted(ref_urls)}"
                )
            return f"{url}#{anchor}" if anchor else url

        line = REF_RE.sub(resolve, line)

        # HTML comments are not valid MDX; keep the note as an MDX comment.
        line = COMMENT_RE.sub(lambda m: "{/*" + m.group(1) + "*/}", line)

        line = IFRAME_RE.sub(jsx_iframe, line)

        # `<nil>` in a table cell, and comparison operators such as `<=` or
        # `<1000`, would both be parsed as JSX. Inline code spans are exempt.
        segments: list[str] = []
        last = 0
        for code in INLINE_CODE_RE.finditer(line):
            segments.append(escape_stray_lt(line[last : code.start()]))
            segments.append(code.group(0))
            last = code.end()
        segments.append(escape_stray_lt(line[last:]))
        line = "".join(segments)

        out.append(line)

    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text + "\n"


# --------------------------------------------------------------------------
# Tree walking
# --------------------------------------------------------------------------
def weight_of(data: dict[str, str], default: int = 9999) -> int:
    try:
        return int(data.get("weight", default))
    except ValueError:
        return default


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)

    src_root = Path(sys.argv[1]).resolve() / "docs"
    dest_root = Path(sys.argv[2]).resolve()

    if not src_root.is_dir():
        raise SystemExit(f"not a directory: {src_root}")

    # ---- pass 1: read every page, build the slug -> URL map ----------------
    pages: list[dict] = []
    for path in sorted(src_root.rglob("*.md")):
        data, body = split_frontmatter(path.read_text(encoding="utf-8"))
        rel = path.relative_to(src_root)
        is_index = path.name == "_index.md"
        rel_dir = rel.parent
        slug = rel_dir.name if is_index else path.stem

        if is_index and rel_dir == Path("."):
            url = "/docs"
            out_rel = Path("index.mdx")
        elif is_index:
            url = "/docs/" + rel_dir.as_posix()
            out_rel = rel_dir / "index.mdx"
        else:
            url = "/docs/" + (rel.with_suffix("").as_posix())
            out_rel = rel.with_suffix(".mdx")

        pages.append(
            {
                "src": path,
                "out_rel": out_rel,
                "rel_dir": rel_dir,
                "slug": slug,
                "url": url,
                "is_index": is_index,
                "data": data,
                "body": body,
            }
        )

    ref_urls = {
        p["slug"]: p["url"]
        for p in pages
        if not (p["is_index"] and p["rel_dir"] == Path("."))
    }
    # Hugo resolved `{{< ref "docs" >}}` style refs to the section index too.
    for p in pages:
        if p["is_index"] and p["rel_dir"] != Path("."):
            ref_urls.setdefault(p["rel_dir"].name, p["url"])

    # ---- pass 2: write MDX -------------------------------------------------
    if dest_root.exists():
        shutil.rmtree(dest_root)
    dest_root.mkdir(parents=True)

    for p in pages:
        frontmatter = {
            "title": p["data"].get("title", p["slug"]),
            "description": p["data"].get("description", ""),
        }
        icon = p["data"].get("icon")
        if icon:
            mapped = ICON_MAP.get(icon)
            if mapped is None:
                print(f"  ! no lucide mapping for icon {icon!r} ({p['src'].name})")
            else:
                frontmatter["icon"] = mapped

        body = rewrite_body(p["body"], ref_urls, p["src"])
        target = dest_root / p["out_rel"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            dump_frontmatter(frontmatter) + "\n\n" + body, encoding="utf-8"
        )
        print(f"  {p['src'].relative_to(src_root)} -> {p['out_rel']}")

    # ---- pass 3: meta.json per folder, preserving Hugo weights ------------
    by_dir: dict[Path, list[dict]] = {}
    for p in pages:
        by_dir.setdefault(p["rel_dir"], []).append(p)

    for rel_dir, entries in sorted(by_dir.items()):
        index_page = next((e for e in entries if e["is_index"]), None)
        children = [e for e in entries if not e["is_index"]]

        # Sub-folders of this directory count as ordered items too.
        subdirs = [
            d
            for d in by_dir
            if d != rel_dir and d.parent == rel_dir
        ]
        items: list[tuple[int, str]] = [
            (weight_of(e["data"]), e["slug"]) for e in children
        ]
        for d in subdirs:
            sub_index = next(
                (e for e in by_dir[d] if e["is_index"]), None
            )
            items.append(
                (weight_of(sub_index["data"] if sub_index else {}), d.name)
            )
        items.sort(key=lambda it: (it[0], it[1]))

        meta: dict[str, object] = {}
        if index_page:
            meta["title"] = index_page["data"].get("title", rel_dir.name)
            description = index_page["data"].get("description")
            if description:
                meta["description"] = description
            icon = ICON_MAP.get(index_page["data"].get("icon", ""))
            if icon:
                meta["icon"] = icon

        ordered = [name for _, name in items]
        if rel_dir == Path("."):
            # The root has no folder node, so its index page needs to be
            # listed explicitly to show up in the sidebar.
            ordered = ["index", *ordered]
        meta["pages"] = ordered

        path = dest_root / rel_dir / "meta.json"
        path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
        print(f"  meta.json <- {rel_dir}/ ({len(ordered)} items)")


if __name__ == "__main__":
    main()
