from typing import List

from bs4 import BeautifulSoup
import requests
import pandas as pd

import db

req_params = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate",
    "cache-control": "max-age=0",
    "accept-language": "en-US,en;q=0.9",
    "referer": "https://parking.wustl.edu/campus-shuttle-system/",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.58 Safari/537.36",
}

urls = {
    "Lewis Center Shuttle": "https://parking.wustl.edu/items/lewis-center/",
    "Delmar Loop Shuttle": "https://parking.wustl.edu/items/delmar-loop/",
    "Metro Green Line": "https://www.metrostlouis.org/route/5-green/",
}


def getTablesFromUrl(url: str) -> List[pd.DataFrame]:
    resp = requests.get(url, req_params)
    soup = BeautifulSoup(resp.text, "lxml")

    tables = soup.find_all("table")

    dfs = pd.read_html(str(tables))
    return dfs


def main():
    for name, url in urls.items():
        dfs = getTablesFromUrl(url)

        # first table is week day, second table is weekend
        # for metro, second is saturday and third is sunday but
        # for metro green line they are the same.
        assert len(dfs) >= 2
        db.update(name + "_weekday", dfs[0])
        db.update(name + "_weekend", dfs[1])


if __name__ == "__main__":
    main()

    getTablesFromUrl(urls["Metro Green Line"])
