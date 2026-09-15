#!/usr/bin/env python3
"""Check built pages for consistent sharing metadata and obsolete course names."""

import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit


OBSOLETE_NAMES = re.compile(
    r"Future\s+Literacy|Video\s+and\s+Robot\s+Foundation\s+Models", re.I
)


class PageHead(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_head = False
        self.in_title = False
        self.title = ""
        self.canonical = ""
        self.meta = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "head":
            self.in_head = True
        if not self.in_head:
            return
        if tag == "title":
            self.in_title = True
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs.get("href", "")
        if tag == "meta":
            key = attrs.get("property", attrs.get("name", ""))
            self.meta.setdefault(key, []).append(attrs.get("content", ""))

    def handle_endtag(self, tag):
        if tag == "head":
            self.in_head = False
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_head and self.in_title:
            self.title += data


def check_site(root):
    errors = []
    checked = 0
    for path in sorted(root.rglob("*")):
        if path.suffix not in {".html", ".json"}:
            continue
        source = path.read_text(encoding="utf-8")
        text = json.dumps(json.loads(source), ensure_ascii=False) if path.suffix == ".json" else html.unescape(source)
        if OBSOLETE_NAMES.search(text) or OBSOLETE_NAMES.search(re.sub(r"<[^>]+>", " ", text)):
            errors.append(f"{path.relative_to(root)}: obsolete course or lecture name")
        if path.suffix != ".html":
            continue
        head = PageHead()
        head.feed(source)
        if not any("mkdocs-" in value for value in head.meta.get("generator", [])):
            continue
        checked += 1
        required = (
            "description", "og:title", "og:description", "og:url", "og:site_name",
            "twitter:title", "twitter:description", "twitter:card",
        )
        missing = [key for key in required if len(head.meta.get(key, [])) != 1 or not head.meta[key][0].strip()]
        if missing:
            errors.append(f"{path.relative_to(root)}: missing, empty, or duplicate metadata: {', '.join(missing)}")
            continue
        meta = {key: values[0] for key, values in head.meta.items()}
        if meta["og:title"] != meta["twitter:title"]:
            errors.append(f"{path.relative_to(root)}: sharing titles disagree")
        if not (meta["description"] == meta["og:description"] == meta["twitter:description"]):
            errors.append(f"{path.relative_to(root)}: page and sharing descriptions disagree")
        if path.name != "404.html" and head.title.strip() not in {
            meta["og:title"], f'{meta["og:title"]} - {meta["og:site_name"]}'
        }:
            errors.append(f"{path.relative_to(root)}: page and sharing titles disagree")
        url = urlsplit(meta["og:url"])
        if url.scheme not in {"http", "https"} or not url.netloc or (head.canonical and meta["og:url"] != head.canonical):
            errors.append(f"{path.relative_to(root)}: sharing URL is not the absolute canonical URL")
    if not checked:
        errors.append(f"{root}: no built MkDocs pages found; build the site first")
    return checked, errors


if __name__ == "__main__":
    count, errors = check_site(Path(sys.argv[1] if len(sys.argv) > 1 else "site"))
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        sys.exit(1)
    print(f"Checked {count} MkDocs pages: sharing metadata agrees; no obsolete course names in HTML or JSON.")
