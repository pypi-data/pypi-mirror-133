from .network import new_user_agent
from .types import SearchEngine

def load_engine(engine: str, dork: str, page: int) -> SearchEngine|ValueError:
        """ Creates a SearchEngine based on a dork and page. The object is used by network.fetch()
        to craft the request URL and beautifulsoup4 parser.

        Args:
            - `engine: str` - name of a supported engine

        Refer to utils.types to add your own SearchEngine dict.
        """
        search_engines: dict[str, SearchEngine] = {
            "ASK": {
                "base_url": "https://www.ask.com/web",
                "headers": new_user_agent(),
                "params": {"q": dork, "page": page},
                "soup_tag": "div",
                "soup_class": {
                    "class": "PartialSearchResults-item-url PartialSearchResults-item-top-url"
                },

            },
            "BING": {
                "base_url": "https://www.bing.com/search",
                "headers": new_user_agent(),
                "params": {"q": dork, "first": page * 10 + 1},
                "soup_tag": "cite",
                "soup_class": "",

            },
            "WOW": {
                "base_url": "https://www.wow.com/search",
                "headers": new_user_agent(),
                "params": {"q": dork, "b": page * 8},
                "soup_tag": "span",
                "soup_class": {"class": "fz-ms fw-m fc-12th wr-bw lh-17"},

            },
        }
        match engine.upper():
            case "BING":
                return search_engines["BING"]
            case "ASK":
                return search_engines["ASK"]
            case "WOW":
                return search_engines["WOW"]
            case _:
                return ValueError(f"{engine} is not supported")