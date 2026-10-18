import json
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3.5:4b"


def extract_items(text: str) -> list[dict]:
    """Extract product names, quantities and units from an order."""
    if not text.strip():
        raise ValueError("Order cannot be empty.")

    prompt = f"""
Extract grocery items from the order below.

Return JSON only in this format:
{{
  "items": [
    {{"name": "aata", "quantity": 2, "unit": "kg"}},
    {{"name": "sarson tel", "quantity": 1, "unit": "litre"}}
  ]
}}

Rules:
- Extract only items explicitly mentioned.
- Do not invent products or quantities.
- Do not calculate prices.
- Use kg, g, litre, ml, packet, or pcs as units.
- If a quantity or unit is unclear, do not guess.

Order: {json.dumps(text, ensure_ascii=False)}
"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "think": False,
        "format": "json",
        "options": {
            "temperature": 0,
            "num_predict": 200,
        },
        "keep_alive": "5m",
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            result = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        raise RuntimeError(f"Ollama extraction failed: {exc}") from exc

    try:
        extracted = json.loads(result["response"])
        items = extracted["items"]
    except (KeyError, TypeError, json.JSONDecodeError) as exc:
        raise ValueError("The AI returned invalid item JSON.") from exc

    if not isinstance(items, list):
        raise ValueError("The AI response must contain an items list.")

    validated = []

    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Each extracted item must be an object.")

        name = item.get("name")
        quantity = item.get("quantity")
        unit = item.get("unit")

        if not isinstance(name, str) or not name.strip():
            raise ValueError("An extracted item has an invalid name.")

        if isinstance(quantity, bool) or not isinstance(
            quantity, (int, float)
        ):
            raise ValueError("An extracted quantity must be numeric.")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        if unit not in {"kg", "g", "litre", "ml", "packet", "pcs"}:
            raise ValueError(f"Unsupported unit: {unit!r}")

        validated.append({
            "name": name.strip(),
            "quantity": quantity,
            "unit": unit,
        })

    return validated
