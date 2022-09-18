from typing import Dict, Final
from enum import Enum
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from itertools import chain
import json
import shutil

import bs4
from bs4 import BeautifulSoup
import requests
import pandas as pd


req_params: Final = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate",
    "cache-control": "max-age=0",
    "accept-language": "en-US,en;q=0.9",
    "referer": "https://parking.wustl.edu/campus-shuttle-system/",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.58 Safari/537.36",
}


metrostl_urls = {
    "Metro 1 Gold": {
        "url": "https://www.metrostlouis.org/route/1-gold/",
        "route_map_url": "https://externalapps.metrostlouis.org/Libraries/MetrobusMaps/274/Map-MO-1.pdf",
    },
    "Metro 2 Red": {
        "url": "https://www.metrostlouis.org/route/2-red/",
        "route_map_url": "https://externalapps.metrostlouis.org/Libraries/MetrobusMaps/274/Map-MO-2.pdf",
    },
    "Metro 5 Green": {
        "url": "https://www.metrostlouis.org/route/5-green/",
        "route_map_url": "https://www.metrostlouis.org/route/5-green/",
    },
}

washu_urls = {
    "Campus Circulator": {"url": "https://parking.wustl.edu/items/campus-circulator/"},
    "DeBaliviere Place Shuttle": {
        "url": "https://parking.wustl.edu/items/debaliviere-place/"
    },
    "Delmar Loop Shuttle": {"url": "https://parking.wustl.edu/items/delmar-loop/"},
    "Lewis Center Shuttle": {"url": "https://parking.wustl.edu/items/lewis-center/"},
    "Skinker-DeBaliviere Shuttle": {
        "url": "https://parking.wustl.edu/items/skinker-debaliviere/"
    },
    "South Campus Shuttle": {"url": "https://parking.wustl.edu/items/south-campus/"},
    "West Campus Shuttle": {
        "url": "https://parking.wustl.edu/items/west-campus-shuttle/"
    },
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
    _getter = table_name_getter[url_type]
    return {_getter(table): dfs[i] for i, table in enumerate(tables)}


if __name__ == "__main__":
    json_record = {}
    metro_shuttle_names = []
    washu_shuttle_names = []
    mutex = Lock()

    def add_to_record(
        name: str, url: str, mp: Dict[str, pd.DataFrame], route_map_url=None
    ):
        record = {"srcUrl": url, "keys": list(mp.keys())}
        for key, df in mp.items():
            record[key] = df.to_dict("list")
            record[key]["keys"] = list(df.keys())

        if route_map_url:
            record["routeMapUrl"] = route_map_url

        mutex.acquire()
        json_record[name] = record
        mutex.release()

    def process_one_route(
        name: str, url_type: URLType, url: str, route_map_url: str | None = None
    ):
        mp = get_tables_from_url(url, url_type)
        add_to_record(name, url, mp, route_map_url)


    with ThreadPoolExecutor() as executor:
        futures = []

        # build metro data
        for name, meta in metrostl_urls.items():
            url = meta["url"]
            route_map_url = meta.get("route_map_url")
            print(name, url)
            metro_shuttle_names.append(name)
            fut = executor.submit(
                lambda: process_one_route(name, URLType.METRO, url, route_map_url)
            )
            futures.append(fut)

        # build washu shuttles data
        for name, meta in washu_urls.items():
            url = meta["url"]
            print(name, url)
            washu_shuttle_names.append(name)
            fut = executor.submit(lambda: process_one_route(name, URLType.WASHU, url, None))
            futures.append(fut)

        [f.result() for f in futures]


    json_record["shuttleNames"] = {
        "washu": washu_shuttle_names,
        "metro": metro_shuttle_names,
    }
    json_record["buildDate"] = datetime.now().strftime("%b %d, %Y")

    for name in chain(washu_shuttle_names, metro_shuttle_names):
        assert name in json_record

    # save to file
    fname = "data.json"
    with open(fname, "w") as fp:
        json.dump(json_record, fp, indent=2)

    print(f"Saved record to {fname}")

    frontend_public = Path("./frontend/public")
    if frontend_public.exists():
        dest = shutil.copyfile(fname, str(frontend_public / fname))
        print(f"Copied record to {frontend_public}")
