from typing import Dict
from enum import Enum
from datetime import datetime
import json

import bs4
from bs4 import BeautifulSoup, Tag
import requests
import pandas as pd


req_params = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate",
    "cache-control": "max-age=0",
    "accept-language": "en-US,en;q=0.9",
    "referer": "https://parking.wustl.edu/campus-shuttle-system/",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.58 Safari/537.36",
}

metrostl_urls = {
    "Metro Green Line": "https://www.metrostlouis.org/route/5-green/",
}

washu_urls = {
    "Campus Circulator": "https://parking.wustl.edu/items/campus-circulator/",
    "Lewis Center Shuttle": "https://parking.wustl.edu/items/lewis-center/",
    "Delmar Loop Shuttle": "https://parking.wustl.edu/items/delmar-loop/",
    "DeBaliviere Place Shuttle": "https://parking.wustl.edu/items/debaliviere-place/",
    "Skinker-DeBaliviere Shuttle": "https://parking.wustl.edu/items/skinker-debaliviere/",
    "South Campus Shuttle": "https://parking.wustl.edu/items/south-campus/",
    "West Campus Shuttle": "https://parking.wustl.edu/items/west-campus-shuttle/",
}


class URLType(Enum):
    WASHU = 1
    METRO = 2


def _get_Washu_tname(table: bs4.element.Tag) -> str:
    return table.parent.parent.find_previous_sibling("dt").text


def _get_Metro_tname(table: bs4.element.Tag) -> str:
    return table.parent.get("id").split("-")[-1].title()


table_name_getter = {
    URLType.WASHU: _get_Washu_tname,
    URLType.METRO: _get_Metro_tname,
}


def get_tables_from_url(url: str, url_type: URLType) -> Dict[str, pd.DataFrame]:
    tables = BeautifulSoup(requests.get(url, req_params).text, "lxml").find_all("table")
    dfs = [df.fillna("") for df in pd.read_html(str(tables))]
    return {
        table_name_getter[url_type](table): dfs[i] for i, table in enumerate(tables)
    }


if __name__ == "__main__":
    json_record = {}
    shuttle_names = []

    def add_to_record(name: str, url: str, mp: Dict[str, pd.DataFrame]):
        record = {"srcUrl": url, "keys": list(mp.keys())}
        for key, df in mp.items():
            record[key] = df.to_dict("list")
            record[key]["keys"] = list(df.keys())
        json_record[name] = record
        shuttle_names.append(name)

    # build metro data
    for name, url in metrostl_urls.items():
        print(name, url)
        mp = get_tables_from_url(url, URLType.METRO)
        add_to_record(name, url, mp)

    # build washu shuttles data
    for name, url in washu_urls.items():
        print(name, url)
        mp = get_tables_from_url(url, URLType.WASHU)
        add_to_record(name, url, mp)

    json_record["shuttleNames"] = shuttle_names
    json_record["buildDate"] = datetime.now().strftime("%b %d, %Y")

    with open("data.json", "w") as fp:
        json.dump(json_record, fp)
