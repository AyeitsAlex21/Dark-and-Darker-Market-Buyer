from services.darker_db_api import DarkerDBApi
from py_types.darker_db_api import MarketQueryParams

print("Hello world")
if __name__ == "__main__":
    market_params =MarketQueryParams(
        item_id="AdventurerBoots_5001",
        secondary={
            "strength": "2:3"
        },
        condense=True,
    )

    market_resp = DarkerDBApi().get_market(market_params)
    
    with open("market_response.json", "w") as f:
        f.write(market_resp.model_dump_json())