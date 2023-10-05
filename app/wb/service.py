import json
import sys
from pprint import pprint

import requests

sys.path.append("..")
from app.config import ProdSettings  # noqa

api_link = f"https://suppliers-api.wildberries.ru"
req1 = requests.post(
    api_link + "/content/v1/cards/filter",
    headers={
        "Authorization": ProdSettings().WB_TOKEN
    },
    json={
        "vendorCodes": ["MV-031D"],
        "allowedCategoriesOnly": False
    }
)

req2 = requests.post(
    api_link + "/content/v1/cards/cursor/list",
    headers={
        "Authorization": ProdSettings().WB_TOKEN
    },
    json={
          "sort": {
              "cursor": {
                  "limit": 1
              },
              "filter": {
                  "withPhoto": -1
              }
          }
        }
)

pprint(json.loads(req1.content))
