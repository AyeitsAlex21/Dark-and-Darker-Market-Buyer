import os
import requests
from dotenv import load_dotenv

load_dotenv()

from py_types.darker_db_api import ItemQueryParams, MarketResponse, MarketQueryParams

DARKER_DB_URI = os.getenv("DARKER_DB_URI")


class DarkerDBApi:

    def get_market(self, params: MarketQueryParams) -> MarketResponse:

        response = requests.get(
            f'{DARKER_DB_URI}v1/market',
            params=params.to_query_params(),
        )

        print(params.to_query_params())

        if response.status_code != 200:
            raise Exception(f"v1/market {params} responded with {response.status_code}")

        return MarketResponse.model_validate(response.json())

    def get_item(self, item: ItemQueryParams) -> dict:

        response = requests.get(
            f'{DARKER_DB_URI}v1/item',
            params=item.to_query_params(),
        )
        
        if response.status_code != 200:
            raise Exception(f"v1/item {item} responded with {response.status_code}")

        return response.json()