#!/usr/bin/env python3
"""
async_quotes_scraper.py
Asynchronous web scraper using asyncio + aiohttp + BeautifulSoup.

Fixed CSV saving to use aiofiles correctly.
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

HEADERS = {"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"}


async def fetch(session: aiohttp.ClientSession, url: str, sem: asyncio.Semaphore) -> Optional[str]:
    async with sem:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
                async with session.get(url, timeout=timeout) as resp:
                    if resp.status == 200:
                        return await resp.text()
                    else:
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
    We manually produce lines with proper quoting (double quotes doubled).
    """
    # Open file and write header + rows
    async with aiofiles.open(filename, mode="w", encoding="utf-8", newline="") as f:
        # write header
        await f.write('"quote","author","tags"\n')
        for r in rows:
            # CSV quoting: double any internal quotes, then wrap fields in double quotes
            quote = r["quote"].replace('"', '""')
            author = r["author"].replace('"', '""')
            tags = r["tags"].replace('"', '""')
            line = f'"{quote}","{author}","{tags}"\n'
            await f.write(line)


async def scrape_page(session: aiohttp.ClientSession, page: int, sem: asyncio.Semaphore) -> List[Dict[str, str]]:
    url = BASE_URL.format(page=page)
    html = await fetch(session, url, sem)
    if not html:
        return []
    return parse_quotes(html)


async def main(total_pages: int = 10):
    connector = aiohttp.TCPConnector(limit_per_host=CONCURRENCY)
    sem = asyncio.Semaphore(CONCURRENCY)

    async with aiohttp.ClientSession(headers=HEADERS, connector=connector) as session:
        tasks = [asyncio.create_task(scrape_page(session, page, sem)) for page in range(1, total_pages + 1)]

        all_results: List[Dict[str, str]] = []
        start = time.time()

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
    total_pages_to_scrape = 10
    asyncio.run(main(total_pages_to_scrape))
