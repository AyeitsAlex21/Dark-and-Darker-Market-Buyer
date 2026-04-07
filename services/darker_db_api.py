import os
import requests
from dotenv import load_dotenv

load_dotenv()

from py_types.darker_db_api import ItemQueryParams, MarketResponse, MarketQueryParams

DARKER_DB_URI = os.getenv("DARKER_DB_URI")


class DarkerDBApi:

    def get_market(self, item: MarketQueryParams) -> MarketResponse:

        params = {
            "item_id": item.get_item_id(),
        }
        params.update(item.to_query_params())
        params.pop("item", None)
        params.pop("rarity", None)

        response = requests.get(
            f'{DARKER_DB_URI}v1/market',
            params=params
        )

        if response.status_code != 200:
            raise Exception(f"v1/market {item} responded with {response.status_code}")

        return MarketResponse.model_validate(response.json())

    def get_item(self, item: ItemQueryParams) -> dict:

        item_id = item.get_item_id()

        response = requests.get(
            f'{DARKER_DB_URI}v1/items',
            params={'item_id': item_id},
        )
        
        if response.status_code != 200:
            raise Exception(f"v1/item {item_id} responded with {response.status_code}")

        return response.json()