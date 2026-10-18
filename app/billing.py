from decimal import Decimal, ROUND_HALF_UP


UNIT_FACTORS = {
    "g": ("kg", Decimal("0.001")),
    "kg": ("kg", Decimal("1")),
    "ml": ("litre", Decimal("0.001")),
    "l": ("litre", Decimal("1")),
    "litre": ("litre", Decimal("1")),
    "packet": ("packet", Decimal("1")),
    "pcs": ("pcs", Decimal("1")),
}


def calculate_line_total(
    quantity: Decimal,
    input_unit: str,
    product: dict,
) -> Decimal:
    """Calculate a line total after validating units."""
    quantity = Decimal(str(quantity))
    input_unit = input_unit.strip().casefold()
    product_unit = product["unit"].strip().casefold()
    rate = Decimal(str(product["rate"]))

    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero.")

    if rate < 0:
        raise ValueError("Product rate cannot be negative.")

    if input_unit not in UNIT_FACTORS:
        raise ValueError(f"Unsupported input unit: {input_unit}")

    base_unit, factor = UNIT_FACTORS[input_unit]

    if base_unit != product_unit:
        raise ValueError(
            f"Cannot convert {input_unit} to {product_unit}."
        )

    normalized_quantity = quantity * factor
    total = normalized_quantity * rate

    return total.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


def calculate_bill(items: list[dict]) -> dict:
    """Calculate line totals and the final bill."""
    lines = []
    total = Decimal("0.00")

    for item in items:
        line_total = calculate_line_total(
            item["quantity"],
            item["input_unit"],
            item["product"],
        )

        lines.append({
            "name": item["product"]["name"],
            "quantity": str(item["quantity"]),
            "unit": item["input_unit"],
            "line_total": line_total,
        })

        total += line_total

    return {
        "items": lines,
        "total": total.quantize(Decimal("0.01")),
    }
