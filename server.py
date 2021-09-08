from typing import Mapping
from flask import Flask
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)


@app.route("/api")
def api():
    dfs = db.getAll()

    for key in dfs:
        # json/dicts are unordered stores, so
        # set an array of keys to keep order
        dfs[key] = dfs[key].to_dict("list")
        dfs[key]["keys"] = list(dfs[key].keys())

    return dfs


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999)
