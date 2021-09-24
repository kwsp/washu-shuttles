from typing import List
import json

from bs4 import BeautifulSoup
import numpy as np
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
    "Campus Circulator": "https://parking.wustl.edu/items/campus-circulator/",
}


def getTablesFromUrl(url: str) -> List[pd.DataFrame]:
    resp = requests.get(url, req_params)
    soup = BeautifulSoup(resp.text, "lxml")

    tables = soup.find_all("table")

    dfs = pd.read_html(str(tables))
    return dfs


def main():
    json_record = {}
    for name, url in urls.items():
        dfs = getTablesFromUrl(url)

        # first table is week day, second table is weekend
        # for metro, second is saturday and third is sunday but
        # for metro green line they are the same.
        assert len(dfs) >= 2
        name_week = name + " Weekday"
        name_weekend = name + " Weekend"
        for i in range(len(dfs)):
            dfs[i].replace(np.nan, '', inplace=True)
            
        db.update(name_week, dfs[0])
        db.update(name_weekend, dfs[1])

        json_record[name_week] = dfs[0].to_dict("list")
        json_record[name_weekend] = dfs[1].to_dict("list")
        json_record[name_week]["keys"] = list(dfs[0].keys())
        json_record[name_weekend]["keys"] = list(dfs[1].keys())
        json_record[name_week]["src_url"] = url
        json_record[name_weekend]["src_url"] = url

    with open("data.json", "w") as fp:
        json.dump(json_record, fp)


if __name__ == "__main__":
    main()
