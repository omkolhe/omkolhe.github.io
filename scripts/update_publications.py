"""Update publications.json from a Google Scholar profile.

Usage:
  pip install scholarly
  python scripts/update_publications.py GOOGLE_SCHOLAR_USER_ID

Notes:
  Google Scholar does not offer an official public API, so this uses the
  third-party scholarly package. It may occasionally fail if Scholar blocks
  automated access. For a robust public website, commit publications.json
  after this script updates it.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from scholarly import scholarly
except ImportError as exc:
    raise SystemExit("Install dependency first: pip install scholarly") from exc


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] == "GOOGLE_SCHOLAR_USER_ID":
        raise SystemExit("Usage: python scripts/update_publications.py YOUR_GOOGLE_SCHOLAR_USER_ID")

    scholar_id = sys.argv[1]
    author = scholarly.search_author_id(scholar_id)
    author = scholarly.fill(author, sections=["publications"])

    publications = []
    for pub in author.get("publications", []):
        bib = pub.get("bib", {})
        title = bib.get("title", "Untitled")
        year = bib.get("pub_year", "")
        venue = bib.get("venue", "")
        authors = bib.get("author", "")
        url = pub.get("pub_url", "")
        publications.append({
            "title": title,
            "authors": authors,
            "venue": venue,
            "year": year,
            "links": ([{"label": "Google Scholar", "url": url}] if url else []),
        })

    out = Path(__file__).resolve().parents[1] / "publications.json"
    out.write_text(json.dumps(publications, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(publications)} publications to {out}")


if __name__ == "__main__":
    main()
