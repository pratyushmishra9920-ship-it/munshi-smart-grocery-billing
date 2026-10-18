from app.catalog import load_catalog, match_product


def test_catalog_has_25_products():
    products = load_catalog()
    assert len(products) == 25


def test_aata_alias_matches_wheat_flour():
    result = match_product("aata")
    assert result["status"] == "matched"
    assert result["product"]["name"] == "Wheat Flour"


def test_maggi_matches():
    result = match_product("maggi")
    assert result["status"] == "matched"
    assert result["product"]["name"] == "Maggi"


def test_completely_unknown_item_is_rejected():
    result = match_product("space rocket")
    assert result["status"] == "unknown"


def test_empty_input_is_rejected():
    result = match_product("")
    assert result["status"] == "unknown"
