from typing import Dict, List
from datetime import datetime
import json

from bs4 import BeautifulSoup
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


def getTablesFromUrl(url: str) -> List[pd.DataFrame]:
    resp = requests.get(url, req_params)
    soup = BeautifulSoup(resp.text, "lxml")

    tables = soup.find_all("table")

    dfs = pd.read_html(str(tables))
    return dfs

def getTablesFromWashuUrl(url: str) -> Dict[str, pd.DataFrame]:
    resp = requests.get(url, req_params)
    soup = BeautifulSoup(resp.text, "lxml")
    tables = soup.find_all("table")
    dfs = pd.read_html(str(tables))
    
    mp = {}
    for i, table in enumerate(tables):
        name = table.parent.parent.find_previous_sibling("dt").text
        mp[name] = dfs[i]
        
    return mp


def main():
    json_record = {}
    shuttle_names = []

    # build washu shuttles data
    for name, url in washu_urls.items():
        print(name, url)
        mp = getTablesFromWashuUrl(url)

        assert len(mp) >= 2
        for k in mp.keys():
            mp[k].fillna("", inplace=True)

        # db.update(name_week, dfs[0])
        # db.update(name_weekend, dfs[1])
        json_record[name] = {}
        json_record[name]["srcUrl"] = url
        json_record[name]["keys"] = list(mp.keys())
        for key, df in mp.items():
            json_record[name][key] = df.to_dict("list")
            json_record[name][key]["keys"] = list(df.keys())

        shuttle_names.append(name)
    
    json_record["shuttleNames"] = shuttle_names

    # timestamp data
    dt = datetime.now()
    json_record["buildDate"] = f"{dt.year}-{dt.month}-{dt.day}"

    with open("data.json", "w") as fp:
        json.dump(json_record, fp)


if __name__ == "__main__":
    main()
