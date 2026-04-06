from services.darker_db_api import DarkerDBApi

if "__name__" == "__main__":
    market_resp = DarkerDBApi().get_market({
        "item": "RingOfVitality_5001",
    })
    print(market_resp)