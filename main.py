from services.darker_db_api import DarkerDBApi
from services.buy_items import BuyItemsService, ItemToBuy
import json


def main():
    api = DarkerDBApi()
    buy_service = BuyItemsService(api)

    # Validate items first
    validation_errors = buy_service._validate_items()
    if validation_errors:
        print("Validation errors:")
        for error in validation_errors:
            print(f"  - {error}")
        return

    # Find items in the market
    found_items = buy_service.find_items(max_price=1000, has_sold=False)

    # Group results by source file
    results_by_file: dict[str, list[ItemToBuy]] = {}
    for item in found_items:
        if item.source_file not in results_by_file:
            results_by_file[item.source_file] = []
        results_by_file[item.source_file].append(item)

    # Save results to JSON files tagged by source
    for file_name, items in results_by_file.items():
        output_file = f"market_results_{file_name}.json"

        # Convert items to dict for JSON serialization
        items_data = []
        for item in items:
            item_dict = {
                "source_file": item.source_file,
                "query_params": item.query_params.model_dump(),
                "market_item": item.market_item.model_dump(),
                "price": item.price,
                "price_per_unit": item.price_per_unit,
                "quantity": item.quantity
            }
            items_data.append(item_dict)

        combined_data = {
            "source_file": file_name,
            "total_items_found": len(items),
            "items": items_data
        }

        with open(output_file, "w") as f:
            json.dump(combined_data, f, indent=2, default=str)

        print(f"Saved {len(items)} results for {file_name} to {output_file}")

    print(f"\nTotal items found across all files: {len(found_items)}")


if __name__ == "__main__":
    main()