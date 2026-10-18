from app.extractor import extract_items


def test_extracts_basic_grocery_order():
    items = extract_items("2 kg aata and 1 litre sarson tel")

    assert len(items) == 2
    assert items[0]["quantity"] > 0
    assert items[0]["unit"] in {"kg", "g", "litre", "ml", "packet", "pcs"}
    assert items[1]["unit"] in {"kg", "g", "litre", "ml", "packet", "pcs"}
