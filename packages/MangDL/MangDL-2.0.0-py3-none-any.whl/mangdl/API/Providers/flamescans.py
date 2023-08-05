import urllib
from typing import Any, Dict, List, Union

from ...utils.globals import log
from ...utils.utils import dt
from ..Base import Ch, Downloader, Manga, Search, soup


def manga(url: str) -> Manga:
    """Returns a Manga object from the given url.

    Args:
        url (str): url of the manga

    Returns:
        Manga
    """

    ms = soup(url)
    meta = {}
    for m in ms.select(".tsinfo.bixbox .imptdt"):
        i = m.select_one("i")
        meta[m.next_element.strip()] = i.text if i else m.select_one("a").text

    def chap_dict():
        op = {}
        for c in ms.select("div.eplister ul li"):
            op[c["data-num"]] = Ch(
                url         = c.select_one("a")["href"],
                ch          = c["data-num"],
                vol         = None,
                title       = c.select_one("a div div .chapternum").text,
                user        = meta["Posted By"],
                uploaded_at = dt(c.select_one("a div div .chapterdate").text, r"%B %d, %Y"),
            )
        return op

    return Manga(
        url             = url,
        covers          = [ms.select_one(".thumb .attachment-.size-.wp-post-image")["src"]],
        title           = ms.select_one("h1.entry-title").text,
        alt_titles      = ms.select_one("span.alternative").text.split(" | "),
        author          = meta["Author"].split(", "),
        status          = {k: v for v, k in enumerate(["Ongoing", "Completed", "Hiatus", "Cancelled"])}.get(meta["Status"], -1),
        updated_at      = dt(meta["Updated On"], r"%B %d, %Y"),
        created_at      = dt(meta["Posted On"], r"%B %d, %Y"),
        description     = "\n".join(i.text for i in ms.select(".entry-content.entry-content-single p")),
        chapters        = chap_dict(),
    )

def chapter(url: str) -> Ch:
    """
    Return a Ch object from the given url.

    Args:
        url (str): url of the chapter

    Returns:
        Ch
    """
    ms = soup(url)
    ch = ms.select_one("h1.entry-title").text.split()[-1]
    return Ch(
        url              = url,
        ch               = ch,
        vol              = None,
        title            = f"Chapter {ch}",
        scanlator_groups = "Flame Scans",
        imgs             = ms.select("#readerarea p img")["src"],
    )

def dl_search(title: str, **kwargs: Dict[str, Any]) -> Dict[str, str]:
    """Used for downloading when imported.

    Args:
        s (Search): [description]

    Returns:
        Dict[str, str]: [description]
    """

    sr = {}
    ms = soup(f"https://flamescans.org/?s={urllib.parse.quote_plus(title)}")
    pages = ms.select("a.page-numbers")
    if pages:
        log.debug("Multiple pages found. Starting to paginate.", "paginator")
        for p in range(int(pages[-2].text)):
            log.debug(f"Paginating page {p+1}.", "paginator")
            for r in soup(f"https://flamescans.org/page/{p+1}/?s={urllib.parse.quote_plus(title)}").select(".listupd .bs .bsx a"):
                if not r.select_one(".limit .novelabel"):
                    sr[r["title"]] = r["href"]
    else:
        log.debug("Only one page found.", "search")
        for r in ms.select(".listupd .bs .bsx a"):
            sr[r["title"]] = r["href"]
    return sr

def search(s: Search) -> List[Manga]:
    """Can be used for searching manga when using this project as a module.

    Args:
        s (Search): Search dataclass, search parameters for searching.

    Returns:
        List[Manga]: Search results.
    """
    return [manga(i) for i in dl_search(s).values()]

def cli_search(title: str, **kwargs: Dict[str, Any]) -> Dict[str, str]:
    """Format click arguments and options to their respective types,
    then pass that to `dl_search` for it to return the search results.

    Args:
        title (str): Title of the manga to search for.

    Returns:
        Dict[str, str]: Search results
    """

    log.info("Ignoring all keword arguments.", "cli_search")
    return dl_search(title, **kwargs)

def ch_fn(url: str) -> List[str]:
    """CHapter FuNction
    Returns a list of image urls from the given chapter url.

    Args:
        url (str): The url of the chapter to get the images' links from

    Returns:
        List[str]: List of image urls
    """
    return [i["src"] for i in soup(url).select("#readerarea p img")]


def chdls(url: str) -> List[Dict[Union[float, int, None], str]]:
    """CHapter Dictionary LiSt
    Returns a list of dictionaries—with the chapter number and url as the key
    and value respectively—from the given url.

    Args:
        url (str): The url of the manga to get the chapters from

    Returns:
        List[Dict[Union[float, int, None], str]]: The List of dictionaries
            containing the chapter number and url
    """
    op = []
    for c in soup(url).select("div.eplister ul li"):
        op.append({c["data-num"]: c.select_one("a")["href"]})
    return op

def dl(url: str, **kwargs: Dict[str, Any]):
    """Used for downloading when using the project as a module.

    Args:
        url (str): URL of the manga to download.
    """
    ms = soup(url)
    Downloader(ch_fn, **kwargs).dl(ms.select_one("h1.entry-title").text, chdls(url))

def cli_dl(title: str, **kwargs: Dict[str, Any]):
    """Used for downloading when using cli.

    Args:
        title (str): Title of the manga to download.
    """
    Downloader(ch_fn, **kwargs).cli(chdls, cli_search, title)
