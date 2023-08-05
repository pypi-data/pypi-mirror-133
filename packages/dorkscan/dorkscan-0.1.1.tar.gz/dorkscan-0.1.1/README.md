# DorkScan

An atypical search engine scanner that scans search engines with dorked queries returning potentially vulnerable URLs.

## Installation

### PyPI

`pip install dorkscan`

### Source

> *If using a virtual environment pass the full directory path to where you cloned DorkScan*

```sh
$git clone https://gitlab.com/unkwn1/dorkscan.git
$cd dorkscan
$pip install -e dorkscan
```

## DorkScan Function

> Scrape a search engine result page for (potentially) vulnerably sites.

```python
def DorkScan(
    dorks: list[str],
    search_engine: str="BING",
    pages: int=1,
    console: Console=Console()
    ) -> list[ScanResults]
```

## Usage

To view an example of the function in action run:
 `python3 -m dorkscan`

```python
from dorkscan import DorkScan
results = DorkScan(
    search_engine: str="BING",
    pages: int=1,
    dorks: list = ["inurl:.php?", "inurl:admin.php"]
    )
print(results)
```

### Args

#### Required Args

```sh
dorks: list[str] -
    a list of string dork queries ie. "inurl:.php?=","inurl:admin.php"
search_engine: str -
    Bing / Ask / Wow.
```

#### Optional Args

```sh
pages: int -
    Number of search engine result pages to scan.
silent: bool -
    Disable stdout printing
console: Console -
    [rich](https://rich.readthedocs.io/en/stable/reference/console.html) console object for printing.
```

#### Return

```sh
`list[ScanResults]` -
    list item for each page. Each page's result dictionary contains `{"dork": str, "links": list}`
```
