#!/usr/bin/python3
""" An atypical search engine scanner that scans search engines with dorked queries returning potentially vulnerable URLs.
"""
from requests.models import HTTPError
from .network import (
    connection_test,
    fetch,
)
from .engines import load_engine
from .types import ScanResults, SearchEngine
import concurrent.futures
from rich.progress import Progress
from rich.console import Console


# TODO: add query arg
def DorkScan(
    dorks: list[str],
    search_engine: str,
    pages: int = 1,
    silent: bool = False,
    console: Console = Console(),
) -> list[ScanResults]:
    """Scrape a search engine result page for (potentially) vulnerably sites.

    To view an example of the function in action run:
        `python3 -m dorkscan`

    Usage:
        ```python
        from dorkscan import DorkScan
        results = DorkScan(["inurl:.php?", "inurl:admin.php"], "BING", 1,)
        print(results)
        ```

    Required Args:
        dorks: list[str] -
            a list of string dork queries ie. "inurl:.php?=","inurl:admin.php"
        search_engine: str
            Bing / Ask / Wow.

    Optional Args:
        pages: int -
            Number of search engine result pages to scan.
        silent: bool -
            Disable stdout printing
        console: Console -
            [rich](https://rich.readthedocs.io/en/stable/reference/console.html) console object for printing.

    Return:
        list[ScanResults]
    """
    if silent == True:
        console.quiet = True

    if not connection_test():
        raise HTTPError("Failed to ping google.com")
    try:
        load_engine(search_engine, dork=dorks[0], page=1)
    except:
        console.print_exception()
    # -- END ARG CHECKS

    # -- BEGIN SCAN
    final: list[ScanResults] = []
    # TODO: overall progress
    for page in range(1, pages + 1):
        results = []
        with Progress() as progress:
            task = progress.add_task(
                f"Dorking {search_engine} page {page}: ", total=len(dorks)
            )
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                for dork in dorks:
                    # engine = load_engine(search_engine, dork, page)
                    futures.append(
                        executor.submit(
                            fetch, engine=load_engine(search_engine, dork, page)
                        )
                    )
                for future in concurrent.futures.as_completed(futures):
                    results.append(future.result())
                    progress.advance(task)

        final.append(
            {
                "page": page,
                # TODO: catch empty url maybe `and not None`?
                "results": [result for result in results if len(result["urls"]) > 0],
            }
        )

    return final
