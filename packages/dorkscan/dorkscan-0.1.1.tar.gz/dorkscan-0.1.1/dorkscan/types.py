from typing import TypedDict, Union


class SearchEngine(TypedDict):
    """A custom dict type for DorkScan engines.

    Example:
    ``` python
        "ASK": {
            "base_url": "https://www.ask.com/web",
            "headers": new_user_agent(),
            "params": {"q": dork, "page": page},
    ```
    """

    base_url: str
    headers: dict[str, str]
    params: dict[str, Union[str, int]]

class DorkResults(TypedDict):
    """
    dork: str
    urls: list
    """

    dork: str | int
    urls: list


class ScanResults(TypedDict):
    """
    page: int
    results: list[DorkResults]
    """

    page: int
    results: list[DorkResults]
