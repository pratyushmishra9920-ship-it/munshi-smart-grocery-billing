from decimal import Decimal
from unittest.mock import patch

from app.order_service import process_order


def test_order_is_extracted_matched_and_billed():
    extracted = [
        {"name": "aata", "quantity": 2, "unit": "kg"},
        {"name": "sarson tel", "quantity": 1, "unit": "litre"},
    ]

    with patch(
        "app.order_service.extract_items",
        return_value=extracted,
    ):
        result = process_order(
            "2 kg aata and 1 litre sarson tel"
        )

    assert result["status"] == "success"
    assert result["total"] == Decimal("230.00")
    assert len(result["items"]) == 2


def test_unknown_product_requires_review():
    extracted = [
        {"name": "space rocket", "quantity": 1, "unit": "pcs"},
    ]

    with patch(
        "app.order_service.extract_items",
        return_value=extracted,
    ):
        result = process_order("one space rocket")

    assert result["status"] == "needs_review"
    assert result["total"] is None
