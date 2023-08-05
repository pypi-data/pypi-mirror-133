from typing import TypedDict, Union


class SearchEngine(TypedDict):
    """A custom dict type for DorkScan engines.

    Example:
    ``` python
        "ASK": {
            "base_url": "https://www.ask.com/web",
            "headers": new_user_agent(),
            "params": {"q": dork, "page": page},
            "soup_tag": "div",
            "soup_class": {
                "class": "PartialSearchResults-item-url PartialSearchResults-item-top-url"
            }
    ```
    """

    base_url: str
    headers: dict[str, str]
    params: dict[str, Union[str, int]]
    soup_tag: str
    soup_class: str | dict

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
