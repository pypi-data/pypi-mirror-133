from dataclasses import dataclass
from typing import List, Mapping
from bs4 import BeautifulSoup
from requests import Response as R
import logging
from enum import Enum
import csv
from mangawalk.utils.dateutils import created_at
from dataclasses import dataclass
from mangawalk.scraping.types.type_mangawalk import PVResult

class ComicKURL(Enum):
    HOME = "https://comic.k-manga.jp"
    PV = "https://comic.k-manga.jp/title/{}/pv"
    VOL = "https://comic.k-manga.jp/title/{}/vol/{}"
    REVIEW = "https://comic.k-manga.jp/title/{}/report/{}"
    RANK = "https://comic.k-manga.jp/rank"


class ComicKRankGen(Enum):
    TOTAL = "total"


class ComicKRankDuration(Enum):
    DAILY = "daily"


class ComicKRankSex(Enum):
    COMMON = "common"
