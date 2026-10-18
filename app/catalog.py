import csv
import re
from difflib import SequenceMatcher
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = PROJECT_ROOT / "data" / "pricelist.csv"


def normalize(text: str) -> str:
    """Normalize text for case-insensitive product matching."""
    text = text.casefold().strip()
    text = re.sub(r"[^\w\s]", " ", text)
    return " ".join(text.split())


def load_catalog(path: Path = CATALOG_PATH) -> list[dict]:
    """Load and validate products from the CSV catalogue."""
    products = []

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        required = {"name", "aliases", "unit", "rate"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(
                "CSV must contain name, aliases, unit, rate columns."
            )

        for row in reader:
            name = row["name"].strip()
            aliases = [
                alias.strip()
                for alias in row["aliases"].split(";")
                if alias.strip()
            ]
            unit = row["unit"].strip().casefold()

            if not name or not unit:
                raise ValueError("Product name and unit cannot be empty.")

            try:
                rate = float(row["rate"])
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"Invalid rate for product {name!r}."
                ) from exc

            if rate < 0:
                raise ValueError(f"Rate cannot be negative for {name!r}.")

            products.append({
                "name": name,
                "aliases": aliases,
                "unit": unit,
                "rate": rate,
            })

    return products


def match_product(
    said: str,
    products: list[dict] | None = None,
    threshold: float = 0.72,
    ambiguity_margin: float = 0.08,
) -> dict:
    """
    Return matched, ambiguous, or unknown.

    If the two best different products have similar scores,
    request confirmation instead of silently choosing one.
    """
    if products is None:
        products = load_catalog()

    query = normalize(said)

    if not query:
        return {"status": "unknown", "said": said, "candidates": []}

    scored = []

    for product in products:
        names = [product["name"], *product["aliases"]]
        best_score = max(
            SequenceMatcher(None, query, normalize(name)).ratio()
            for name in names
        )
        scored.append((best_score, product))

    scored.sort(key=lambda item: item[0], reverse=True)

    if not scored or scored[0][0] < threshold:
        return {"status": "unknown", "said": said, "candidates": []}

    best_score, best_product = scored[0]

    # Keep only the best score per distinct product.
    distinct = []
    seen_names = set()

    for score, product in scored:
        if product["name"] not in seen_names:
            distinct.append((score, product))
            seen_names.add(product["name"])

    best_score, best_product = distinct[0]

    if (
        len(distinct) > 1
        and distinct[1][0] >= threshold
        and best_score - distinct[1][0] <= ambiguity_margin
    ):
        return {
            "status": "ambiguous",
            "said": said,
            "candidates": [
                {
                    "name": product["name"],
                    "score": round(score, 3),
                }
                for score, product in distinct[:3]
            ],
        }

    return {
        "status": "matched",
        "said": said,
        "product": best_product,
        "score": round(best_score, 3),
    }
