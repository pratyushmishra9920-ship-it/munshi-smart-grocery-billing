from decimal import Decimal

from app.catalog import load_catalog, match_product
from app.billing import calculate_bill
from app.extractor import extract_items


def process_order(text: str) -> dict:
    """Extract an order, match products and calculate its bill."""
    extracted_items = extract_items(text)
    catalog = load_catalog()

    bill_items = []
    unmatched = []

    for item in extracted_items:
        match = match_product(item["name"], catalog)

        if match["status"] != "matched":
            unmatched.append({
                "name": item["name"],
                "status": match["status"],
                "candidates": match.get("candidates", []),
            })
            continue

        bill_items.append({
            "product": match["product"],
            "quantity": Decimal(str(item["quantity"])),
            "input_unit": item["unit"],
        })

    if unmatched:
        return {
            "status": "needs_review",
            "unmatched": unmatched,
            "items": [],
            "total": None,
        }

    if not bill_items:
        return {
            "status": "empty",
            "items": [],
            "total": Decimal("0.00"),
        }

    bill = calculate_bill(bill_items)

    return {
        "status": "success",
        **bill,
    }
