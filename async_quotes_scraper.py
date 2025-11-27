#!/usr/bin/env python3
"""
async_quotes_scraper.py
Asynchronous web scraper using asyncio + aiohttp + BeautifulSoup.

Scrapes quotes from https://quotes.toscrape.com (safe test site).
Saves results to quotes.csv.

Usage:
    python async_quotes_scraper.py
"""

import asyncio
import csv
import random
import time
from typing import List, Dict, Optional

import aiofiles
import aiohttp
from bs4 import BeautifulSoup

# ---------- CONFIG ----------
BASE_URL = "https://quotes.toscrape.com/page/{page}/"
CONCURRENCY = 5                 # max concurrent requests
REQUEST_TIMEOUT = 15            # seconds
MAX_RETRIES = 3
BACKOFF_BASE = 0.5              # exponential backoff base seconds
OUTPUT_CSV = "quotes.csv"
USER_AGENT = "AsyncScraper/1.0 (+https://example.com/info)"
# ----------------------------

# Simple helper to build headers
HEADERS = {"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"}


async def fetch(session: aiohttp.ClientSession, url: str, sem: asyncio.Semaphore) -> Optional[str]:
    """
    Fetch page content with retries and exponential backoff.
    Returns HTML text or None on repeated failure.
    """
    async with sem:  # limit concurrent connections
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
                async with session.get(url, timeout=timeout) as resp:
                    # simple status check
                    if resp.status == 200:
                        text = await resp.text()
                        return text
                    else:
                        # Non-200: treat as failure to be retried (but maybe don't retry 404)
                        if resp.status == 404:
                            print(f"[{url}] 404 Not Found. Stopping retries.")
                            return None
                        raise aiohttp.ClientResponseError(
                            history=resp.history, request_info=resp.request_info,
                            status=resp.status, message=await resp.text()
                        )
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                wait = BACKOFF_BASE * (2 ** (attempt - 1)) + random.uniform(0, 0.3)
                print(f"[{url}] attempt {attempt} failed: {e}. Backing off {wait:.2f}s")
                await asyncio.sleep(wait)
        print(f"[{url}] all {MAX_RETRIES} attempts failed.")
        return None


def parse_quotes(html: str) -> List[Dict[str, str]]:
    """
    Parse quotes from the page HTML using BeautifulSoup.
    Returns list of dicts: {'quote': ..., 'author': ..., 'tags': 'tag1|tag2'}
    """
    soup = BeautifulSoup(html, "lxml")
    quote_divs = soup.select("div.quote")
    results = []
    for q in quote_divs:
        text_el = q.select_one("span.text")
        author_el = q.select_one("small.author")
        tag_els = q.select("div.tags a.tag")

        quote_text = text_el.get_text(strip=True) if text_el else ""
        author = author_el.get_text(strip=True) if author_el else ""
        tags = "|".join([t.get_text(strip=True) for t in tag_els]) if tag_els else ""

        results.append({"quote": quote_text, "author": author, "tags": tags})
    return results


async def save_to_csv(rows: List[Dict[str, str]], filename: str):
    """
    Save rows to CSV asynchronously using aiofiles.
    """
    # If file exists, we append. For simplicity, overwrite each run:
    async with aiofiles.open(filename, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(await f.__aenter__())  # using csv with aiofiles needs a small workaround
        # write headers
        await f.write("quote,author,tags\n")
        for r in rows:
            # simple CSV escaping - ensures newlines/commas won't break CSV columns
            quote = r["quote"].replace('"', '""')
            author = r["author"].replace('"', '""')
            tags = r["tags"].replace('"', '""')
            line = f'"{quote}","{author}","{tags}"\n'
            await f.write(line)


async def scrape_page(session: aiohttp.ClientSession, page: int, sem: asyncio.Semaphore) -> List[Dict[str, str]]:
    """
    Fetch and parse a single page number. Returns parsed results or empty if failure.
    """
    url = BASE_URL.format(page=page)
    html = await fetch(session, url, sem)
    if not html:
        return []
    return parse_quotes(html)


async def main(total_pages: int = 10):
    """
    Orchestrates concurrent scraping of pages 1..total_pages
    """
    connector = aiohttp.TCPConnector(limit_per_host=CONCURRENCY)
    sem = asyncio.Semaphore(CONCURRENCY)

    # Use a single session for all requests (recommended)
    async with aiohttp.ClientSession(headers=HEADERS, connector=connector) as session:
        # create tasks
        tasks = [asyncio.create_task(scrape_page(session, page, sem)) for page in range(1, total_pages + 1)]

        all_results: List[Dict[str, str]] = []
        start = time.time()
        # gather in a way that we can process results as they finish
        for coro in asyncio.as_completed(tasks):
            page_results = await coro
            all_results.extend(page_results)
            print(f"Fetched page chunk: {len(page_results)} quotes (total so far: {len(all_results)})")

        duration = time.time() - start
        print(f"Scraped {len(all_results)} quotes from {total_pages} pages in {duration:.2f}s")

        if all_results:
            await save_to_csv(all_results, OUTPUT_CSV)
            print(f"Saved to {OUTPUT_CSV}")


if __name__ == "__main__":
    # pick how many pages you want to fetch (quotes.toscrape.com has 10 pages)
    total_pages_to_scrape = 10
    asyncio.run(main(total_pages_to_scrape))
