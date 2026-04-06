import os
import requests

from py_types.darker_db_api import MarketResponse

DARKER_DB_URI = os.getenv("DARKER_DB_URI")


class DarkerDBApi:

    def __init__(self):
        self.darker_db_uri = DARKER_DB_URI

    def get_market(self, params: dict) -> MarketResponse:
        request_params = {
            "has_sold": False,
        }
        request_params.update(params or {})

        response = requests.get(
            f'{self.darker_db_uri}v1/market',
            params=request_params
        )

        if response.status_code != 200:
            raise Exception(f"v1/market {request_params} responded with {response.status_code}")

        return MarketResponse.model_validate(response.json())