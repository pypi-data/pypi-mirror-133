from . import DorkScan
import requests
from rich.console import Console
from rich.syntax import Syntax
from time import sleep
from sys import exit


def main():
    scan_eg = """
    from dorkscan import DorkScan
    dorks = requests.get("https://gitlab.com/unkwn1/dorkscan/-/snippets/2228505/raw/main/default_dorks-1500.txt").text.split()[
    scan = DorkScan(pages=2,dorks=dorks,engine="bing")
    """
    console = Console()
    console.print("DorkScan Function Demonstration", no_wrap=True, style="bold green")
    sleep(1)
    console.print(Syntax(str(DorkScan.__doc__), "markdown"))
    sleep(4)
    console.clear()
    console.print(Syntax(scan_eg, "python"))
    dorks = requests.get(
        "https://gitlab.com/unkwn1/dorkscan/-/snippets/2228505/raw/main/default_dorks-1500.txt"
    ).text.split()[:350]
    console.print("Starting example using the code below:", style="yellow")
    results = {
        "scan": DorkScan(search_engine="bing", pages=2, dorks=dorks, console=console)
    }
    console.clear()
    console.print("Scan finished. Dumping result dictionary!", style="bold green")
    sleep(2)
    console.print_json(data=results)
    sleep(5)
    console.print(
        """
        Increase dorks and pages for optimal results.
        Keep rate limiting in mind.
        """,
        style="yellow bold",
    )
    console.print(
        """
        GOOD-BYE :)
        Project Home: [Unkwn1 Gitlab(]https://gitlab.com/unkwn1/dorkscan)
        Credits:
            Original project concept by: [Balgogan](https://github.com/Balgogan/)
        """,
        style="green bold",
    )
    exit(3)


main()
