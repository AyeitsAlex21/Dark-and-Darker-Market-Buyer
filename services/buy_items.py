
from urllib import response

from .darker_db_api import DarkerDBApi
from py_types.darker_db_api import MarketQueryParams, MarketItem, ItemQueryParams

class BuyItemsService():
    def __init__(self, items: list[MarketQueryParams]):

        for item in items:
            self._validate_item(item)

        self.items = items

    def _validate_item(self, item: MarketQueryParams) -> None:
        req_item = ItemQueryParams(
            name=item.item,
            rarity=item.rarity,
        )

        response_json = DarkerDBApi().get_item(req_item)

        if len(response_json["body"]) != 1:
            raise Exception(f"v1/item {item} responded with {response_json}")
    
    def attempt_to_buy_items(self) -> list[MarketQueryParams]:
        bought_items = []

        for item in self.items:
            cand_items = DarkerDBApi().get_market(item).body

            if len(cand_items) == 0:
                continue

            cand_items.sort(key=lambda x: x.price, reverse=False)
            if self._attempt_to_buy_item(item, cand_items):
                bought_items.append(item)

        return bought_items

    def _attempt_to_buy_item(self, item: MarketQueryParams, cand_items: list[MarketItem]) -> bool:
        cheapest = cand_items[0]
        print(f"Attempting to buy {cheapest.item} for {cheapest.price} gold")
        # Assume buy succeeds for now
        return True