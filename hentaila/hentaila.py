import logging
import re

import requests
from bs4 import BeautifulSoup

from hentaila.la_types.errors import LaPageLenError
from hentaila.la_types.types_la import LaHentai, LaInfoH, LaInfo
from . import _base, directory_base
from .simple_utils import _base_func, iter_base_func

logger = logging.getLogger("LaLogger")


def get_dict_directory(info) -> LaInfoH:
    thumb = _base + info.find("img").get("src")
    title = info.find("h2").get_text()
    anime_url = _base + info.find("a").get("href")
    return LaInfoH(title, anime_url, thumb)


def get_dict_recent(info) -> LaInfo:
    thumb = _base + info.find("img").get("src")
    title = info.find("h2").get_text()
    chapter_url = _base + info.find("a").get("href")
    anime_url = chapter_url[:-2]
    episode = int(chapter_url.split("-")[-1])
    return LaInfo(title, anime_url, chapter_url, thumb, episode)


def filters_la(
        page: int = 1,
        _filter: str = "recent",
        status: int = 0,
        other: bool = False) -> dict:
    """
    :param page: number of pages
    :param _filter: "recent" or "popular"
    :param status: set 1 for "emission", set 2 for "finalized".
    :param other: True for uncensored, False for censured
    :return: filters dict
    """
    _filters = {
        "filter": _filter,
        "p": page
    }
    if status:
        _filters[f"status[{status}]"] = "on"
    elif other:
        _filters["uncensored"] = "on"
    _max_page = total_count(_filters)
    if page > _max_page:
        raise LaPageLenError(
            f"Page number {page} is larger than total page number {_max_page}")
    return _filters


def total_count(_filters: dict = None) -> int:
    _filters.pop("p")
    r = requests.get(directory_base, params=_filters)
    soup = BeautifulSoup(r.content, 'html.parser')
    return int(
        soup.find(
            "ul",
            {
                "class": "pagination episodes_nav-list"
            }).find_all("a")[-2].get_text())


class Hentaila:
    @staticmethod
    def directory(page=1, _filter="recent", status=0, other=False) -> list[LaInfoH]:
        """
        :param page: number of pages
        :param _filter: "recent" or "popular"
        :param status: set 1 for "emission", set 2 for "finalized".
        :param other: True for uncensored, False for censured
        :return: list of hentai's
        """
        _filters = filters_la(page, _filter, status, other)
        r = requests.get(
            directory_base,
            params=_filters
        )
        soup = BeautifulSoup(r.content, 'html.parser')
        _directory = soup.find("div", {"class": "grid hentais"}).find_all("article")
        return list(map(get_dict_directory, _directory))

    @staticmethod
    def get_hentai(url) -> LaHentai:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        episodes = soup.find("div", {"class": "episodes-list"}).find_all("a")
        genres = soup.find("nav", {"class": "genres"}).find_all("a")
        chapters = list(map(iter_base_func, episodes))[::-1]
        return LaHentai(
            url,
            chapters,
            soup.find("h1", {"class": "h-title"}).text,
            map(lambda x: (x.text, iter_base_func(x)), genres),
            chapters
        )

    @staticmethod
    def get_chapter(url) -> list:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        __videos = soup.find_all("script")[-3].text
        chapters = soup.find("div", {"class": "download-links"}).find_all("a")
        __chapters_videos = []
        __chapters_videos.extend(
            map(lambda x: x.replace("\\", ""), re.findall(r'https?[a-zA-Z0-9!#.:-\\/-]*', __videos))
        )
        __chapters_videos.extend(map(_base_func, chapters))
        return __chapters_videos

    @staticmethod
    def recents() -> list[LaInfo]:
        r = requests.get(_base)
        soup = BeautifulSoup(r.content, 'html.parser')
        _recents = soup.find("div", {"class": "grid episodes"}).find_all("article")
        return list(map(get_dict_recent, _recents))
