#!/usr/bin/env python3
"""
Health-check live tool URLs declared in data/tools.yml.

For every entry where status == "live", resolve astro_url against
https://paulgibbonsadvisory.com and assert HTTP 200. Designed to run in
CI as a non-blocking warning (see .github/workflows/mkdocs.yml).

Usage:
  python scripts/check_live_urls.py

Exit 0 if all live URLs return 200, exit 1 otherwise.
"""

import logging
import sys
from pathlib import Path

import requests
import yaml

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).parent.parent
MANIFEST_PATH = REPO_ROOT / "data" / "tools.yml"
BASE_URL = "https://paulgibbonsadvisory.com"
TIMEOUT_SECONDS = 10
USER_AGENT = "adaptive-adoption-ci/1.0"


def resolve_url(astro_url: str) -> str:
    if astro_url.startswith("http://") or astro_url.startswith("https://"):
        return astro_url
    if not astro_url.startswith("/"):
        astro_url = "/" + astro_url
    return BASE_URL + astro_url


def check_url(url: str) -> tuple[int | None, str]:
    try:
        resp = requests.get(
            url,
            timeout=TIMEOUT_SECONDS,
            allow_redirects=True,
            headers={"User-Agent": USER_AGENT},
        )
        return resp.status_code, ""
    except requests.RequestException as exc:
        return None, str(exc)


def main() -> int:
    logger.info("=== check_live_urls.py start ===")

    if not MANIFEST_PATH.exists():
        logger.error(f"Manifest not found: {MANIFEST_PATH}")
        return 1

    with open(MANIFEST_PATH, encoding="utf-8") as f:
        manifest = yaml.safe_load(f)

    tools = manifest.get("tools", []) if isinstance(manifest, dict) else []
    live = [t for t in tools if t.get("status") == "live"]
    logger.info(f"Found {len(live)} live tools to check")

    results = []
    for entry in live:
        slug = entry.get("slug", "<no-slug>")
        astro_url = entry.get("astro_url")
        if not astro_url:
            results.append((slug, "(missing astro_url)", None, "no URL"))
            continue
        url = resolve_url(astro_url)
        status, err = check_url(url)
        results.append((slug, url, status, err))

    slug_w = max((len(r[0]) for r in results), default=4)
    url_w = max((len(r[1]) for r in results), default=3)
    header = f"{'slug':<{slug_w}}  {'url':<{url_w}}  status"
    print(header)
    print("-" * len(header))

    failures = 0
    for slug, url, status, err in results:
        if status == 200:
            line = f"{slug:<{slug_w}}  {url:<{url_w}}  200 OK"
        else:
            failures += 1
            detail = f"ERR {err}" if status is None else f"HTTP {status}"
            line = f"{slug:<{slug_w}}  {url:<{url_w}}  {detail}"
        print(line)

    total = len(results)
    passed = total - failures
    summary = f"{'PASS' if failures == 0 else 'FAIL'} {passed}/{total}"
    print()
    print(summary)
    logger.info(summary)

    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
