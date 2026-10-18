from decimal import Decimal

import pytest

from app.billing import calculate_bill, calculate_line_total


WHEAT_FLOUR = {
    "name": "Wheat Flour",
    "unit": "kg",
    "rate": "40",
}

MUSTARD_OIL = {
    "name": "Mustard Oil",
    "unit": "litre",
    "rate": "150",
}


def test_two_kg_aata_costs_80():
    result = calculate_line_total(
        Decimal("2"), "kg", WHEAT_FLOUR
    )
    assert result == Decimal("80.00")


def test_500_grams_aata_costs_20():
    result = calculate_line_total(
        Decimal("500"), "g", WHEAT_FLOUR
    )
    assert result == Decimal("20.00")


def test_one_litre_oil_costs_150():
    result = calculate_line_total(
        Decimal("1"), "litre", MUSTARD_OIL
    )
    assert result == Decimal("150.00")


def test_negative_quantity_is_rejected():
    with pytest.raises(ValueError):
        calculate_line_total(
            Decimal("-1"), "kg", WHEAT_FLOUR
        )


def test_incompatible_units_are_rejected():
    with pytest.raises(ValueError):
        calculate_line_total(
            Decimal("1"), "litre", WHEAT_FLOUR
        )


def test_bill_total():
    bill = calculate_bill([
        {
            "product": WHEAT_FLOUR,
            "quantity": Decimal("2"),
            "input_unit": "kg",
        },
        {
            "product": MUSTARD_OIL,
            "quantity": Decimal("1"),
            "input_unit": "litre",
        },
    ])

    assert bill["total"] == Decimal("230.00")
