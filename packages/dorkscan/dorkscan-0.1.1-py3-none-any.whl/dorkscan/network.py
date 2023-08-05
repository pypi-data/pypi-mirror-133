""" DorkScan.network is a set of helper functions for the main module.
"""
import requests
from random import randint
from .types import SearchEngine, DorkResults
from lxml import html
import re


def connection_test(url: str = "https://www.google.com") -> bool:
    """A ping check that returns True or False.

    Optional Args:
        url: str
            defaults to `https://www.google.com`

    Returns:
        True / False
    """
    if requests.get(url, timeout=5000):
        return True
    else:
        return False


def fetch(engine: SearchEngine, search_term: str = None) -> DorkResults | None:
    """Fetch is used by DorkScan to GET and parse a search engine request.

    Required Args:
        engine: SearchEngine
            use load_engine() with a dork query

    Optional Args:
        search_term: str | None
            Default `None`. Add search term to dork when created GET request

    Returns:
        result: dict
            {"dork": <dork>, "urls": <filtered_links>}
    """
    search_term = "test"
    if search_term != None:
        engine["params"]["q"] = f"{engine['params']['q']} {search_term}"
    try:
        resp = requests.get(
            engine["base_url"], params=engine["params"], headers=engine["headers"]
        ).text
        blacklist = re.compile("|".join(bad_urls))
        data= html.fromstring(resp).xpath("//a/@href")
        links = [
            link
            for link in data
            if re.search(r"^http|s://", link)
            and re.search(r"\?.+\=", link)
            and not re.search(blacklist, link)
        ]
        # Links are filtered IF NOT domain blacklist AND contains query parameters
        return {"dork": engine["params"]["q"], "urls": links}
    except:
        pass


def new_user_agent() -> dict[str, str]:
    """Returns a header dictionary with a random User-Agent

    Typical Usage:
        Called within a SearchEngine object. Refer to engine.load_engines()
    """
    user_agents: list[str] = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
        "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/13.2b11866 Mobile/16A366 Safari/605.1.15",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0",
    ]
    return {"User-Agent": user_agents[randint(0, len(user_agents) - 1)]}


bad_urls: list[str] = [
    "facebook",
    "google",
    "pastebin",
    "gist",
    "github",
    "udemy",
    "jetbrains",
    "youtube",
    "whatsapp",
    "telegram",
    "twitter",
    "vuldb",
    "tenable",
    "exploit-db",
    "stackoverflow",
    "bing",
    "w3schools",
    "go.microsoft",
    "wikipedia",
    "cvedetails",
    "exploitdb",
]
