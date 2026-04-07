
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
        
        for random_stat in item.secondary:
            actual_min = response_json["body"][0][f"secondary_min_{random_stat}"]
            actual_max = response_json["body"][0][f"secondary_max_{random_stat}"]

            desired_min, desired_max = item.get_secondary_ranges(item.secondary[random_stat])

            if desired_min < actual_min or desired_max > actual_max:
                raise Exception(f"{item.item} {random_stat} range {desired_min}:{desired_max} is out of bounds ({actual_min}:{actual_max})")

    def attempt_to_buy_items(self) -> list[MarketQueryParams]:
        bought_items = []

        for item in self.items:
            item.has_sold = 0
            item.has_expired = 0

            cand_items = DarkerDBApi().get_market(item).body

            if len(cand_items) == 0:
                continue

            cand_items.sort(key=lambda x: x.price, reverse=False)
            if self._attempt_to_buy_item(item, cand_items):
                bought_items.append(item)

        return bought_items

    def _attempt_to_buy_item(self, item: MarketQueryParams, potential_listings: list[MarketItem]) -> bool:
        for listing in potential_listings:
            print(f"Attempting to buy {listing.item} for {listing.price} gold")
        # Assume buy succeeds for now
        return True