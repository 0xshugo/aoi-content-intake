#!/usr/bin/env python3
"""Merge edition catalog JSON + used-urls.txt into materials.jsonl (backfill)."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


def norm_url(u: str) -> str:
    u = u.strip()
    if not u.startswith("https://"):
        return ""
    return u.rstrip("/")


def host(u: str) -> str:
    return urlparse(u).netloc or ""


def load_editions(editions_dir: Path) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for p in sorted(editions_dir.glob("*.json")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        edition = data.get("edition") or data
        eid = edition.get("edition_id") or p.stem
        edate = edition.get("edition_date") or (eid[:10] if len(eid) >= 10 else "")
        for item in edition.get("items") or []:
            url = norm_url(item.get("source_url") or "")
            if not url:
                continue
            rec = out.setdefault(
                url,
                {
                    "url": url,
                    "canonical_host": host(url),
                    "first_seen_at": f"{edate}T12:00:00+09:00" if edate else "1970-01-01T00:00:00+09:00",
                    "snapshot_ids": [],
                    "axis_matches": [],
                    "used_in": [],
                    "provenance": "backfill",
                },
            )
            used = {
                "product": "news_edition",
                "date": edate,
                "artifact_id": eid,
            }
            if used not in rec["used_in"]:
                rec["used_in"].append(used)
    return out


def merge_used_urls(ledger: dict[str, dict], path: Path) -> None:
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        url = norm_url(line.split("#")[0].strip())
        if not url:
            continue
        if url in ledger:
            continue
        ledger[url] = {
            "url": url,
            "canonical_host": host(url),
            "first_seen_at": "1970-01-01T00:00:00+09:00",
            "snapshot_ids": [],
            "axis_matches": [],
            "used_in": [],
            "provenance": "backfill-used-urls-only",
        }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--editions-dir", type=Path, required=True)
    ap.add_argument("--used-urls", type=Path, default=None)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    if not args.editions_dir.is_dir():
        print("editions-dir missing", file=sys.stderr)
        return 2
    ledger = load_editions(args.editions_dir)
    if args.used_urls:
        merge_used_urls(ledger, args.used_urls)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        for url in sorted(ledger):
            f.write(json.dumps(ledger[url], ensure_ascii=False) + "\n")
    print(len(ledger), "materials ->", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())