from services.buy_items import BuyItemsService
from items_to_buy.Alex import items as alex_items
from items_to_buy.Jessie import items as jessie_items


def main():
    all_items = alex_items + jessie_items
    buy_service = BuyItemsService(all_items)
    
    # Validation is done in BuyItemsService.__init__
    bought_items = buy_service.attempt_to_buy_items()
    
    print(f"Attempted to buy {len(bought_items)} items out of {len(all_items)}")


if __name__ == "__main__":
    main()