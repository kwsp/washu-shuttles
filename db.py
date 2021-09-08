from typing import Dict
import pandas as pd
import sqlite3 as lite


db_name = "store.sqlite"


def update(tableName: str, df: pd.DataFrame):
    with lite.connect(db_name) as conn:
        df.to_sql(tableName, conn, if_exists="replace", index=False)


def getAll() -> Dict[str, pd.DataFrame]:
    with lite.connect(db_name) as conn:
        names = pd.read_sql_query(
            'SELECT name from sqlite_master where type= "table";', conn
        )

        dfs = {}
        for name in names.name:
            df = pd.read_sql_query(f'SELECT * from "{name}"', conn)
            dfs[name] = df

    return dfs


if __name__ == "__main__":
    dfs = getAll()
    breakpoint()
