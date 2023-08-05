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
            },
            "BING": {
                "base_url": "https://www.bing.com/search",
                "headers": new_user_agent(),
                "params": {"q": dork, "first": page * 10 + 1},
            },
            "WOW": {
                "base_url": "https://www.wow.com/search",
                "headers": new_user_agent(),
                "params": {"q": dork, "b": page * 8},
            },
        }
        if engine.upper() == "BING":
            return search_engines["BING"]
        elif engine.upper()  == "ASK":
            return search_engines["ASK"]
        elif engine.upper() == "WOW":
            return search_engines["WOW"]
        else:
            return ValueError(f"{engine} is not supported")