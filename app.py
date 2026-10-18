import streamlit as st
import pandas as pd
import json
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

from app.order_service import process_order
from app.catalog import load_catalog, match_product


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Munshi | AI Grocery Billing",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# --------------------------------------------------
# Styling
# --------------------------------------------------

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .munshi-hero {
        padding: 2rem;
        border-radius: 18px;
        background: linear-gradient(120deg, #12372a, #1c5941);
        color: white;
        margin-bottom: 1.5rem;
    }

    .munshi-hero h1 {
        color: white;
        font-size: 2.8rem;
        margin-bottom: 0.4rem;
    }

    .munshi-hero p {
        color: #e1f2e8;
        font-size: 1.05rem;
        margin-bottom: 0;
    }

    .small-note {
        color: #777;
        text-align: center;
        font-size: 0.85rem;
        margin-top: 1.5rem;
    }

    div[data-testid="stMetric"] {
        border: 1px solid rgba(128, 128, 128, 0.25);
        padding: 1rem;
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def money(amount):
    """Format an amount as Indian rupees."""
    try:
        return f"₹{float(amount):,.2f}"
    except (TypeError, ValueError):
        return "₹0.00"


def use_example(value):
    """Put a sample order into the text area."""
    st.session_state["order_input"] = value


def get_ollama_status():
    """Check Ollama connectivity and Qwen model availability."""
    try:
        with urlopen(
            "http://localhost:11434/api/tags",
            timeout=2,
        ) as response:
            data = json.loads(response.read().decode("utf-8"))

        models = data.get("models", [])
        model_names = {
            model.get("name", "") for model in models
        }

        if any(
            name == "qwen3.5:4b"
            or name.startswith("qwen3.5:4b-")
            for name in model_names
        ):
            return "connected", "Qwen 3.5 · 4B is ready"

        return "missing", "Qwen 3.5 · 4B was not found"

    except (URLError, HTTPError, TimeoutError, OSError, ValueError):
        return "offline", "Ollama is not reachable"

# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    """
    <div class="munshi-hero">
        <h1>🧾 Munshi</h1>
        <p>
            Turn a simple grocery message into a clear, itemized bill —
            privately, using a local AI model.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([3, 2], vertical_alignment="center")

with left:
    st.markdown("### Create a grocery bill")
    st.caption(
        "Type naturally. Example: 2 kg aata, 1 litre sarson tel "
        "and 1 packet Maggi."
    )

with right:
    status, message = get_ollama_status()

    with st.container(border=True):
        st.markdown("### 🖥️ Local AI Engine")
        st.caption("Model: `qwen3.5:4b` · Runtime: Ollama")

        if status == "connected":
            st.success(f"🟢 {message}")
        elif status == "missing":
            st.warning(f"🟡 {message}")
        else:
            st.error(f"🔴 {message}")

        st.caption(
            "🔒 Order extraction runs locally on your computer."
        )


# --------------------------------------------------
# Example orders
# --------------------------------------------------

st.markdown("#### Try an example")

if "order_input" not in st.session_state:
    st.session_state["order_input"] = ""

examples = [
    (
        "🛒 Everyday essentials",
        "2 kg aata, 1 litre sarson tel and 1 packet maggi",
    ),
    (
        "🍪 Snacks",
        "1 packet maggi, 1 kg sugar and 2 packet biscuits",
    ),
    (
        "🥬 Vegetables",
        "1 kg potato, 2 kg onion and 500 g tomato",
    ),
]

example_cols = st.columns(3)

for col, (label, value) in zip(example_cols, examples):
    with col:
        st.button(
            label,
            key=f"example_{label}",
            use_container_width=True,
            on_click=use_example,
            args=(value,),
        )


# --------------------------------------------------
# Order input
# --------------------------------------------------

order = st.text_area(
    "Your order",
    key="order_input",
    placeholder=(
        "Example: 2 kg aata, 1 litre sarson tel "
        "and 1 packet Maggi"
    ),
    height=125,
    help=(
        "Include a quantity and unit for each item. "
        "Use the unit that matches how the product is sold."
    ),
)

button_col, tip_col = st.columns(
    [1, 3],
    vertical_alignment="center",
)

with button_col:
    generate = st.button(
        "🧾 Generate bill",
        type="primary",
        use_container_width=True,
    )

with tip_col:
    st.caption(
        "💡 Tip: If Maggi is listed by packet in your catalog, "
        "enter '1 packet Maggi' rather than '500 g Maggi'."
    )


# --------------------------------------------------
# Process order and display bill
# --------------------------------------------------

if generate:
    if not order.strip():
        st.warning(
            "Please enter your grocery order before generating a bill."
        )

    else:
        try:
            with st.spinner(
                "Understanding your order and checking catalog prices..."
            ):
                result = process_order(order.strip())

            status = result.get("status")

            # ------------------------------------------
            # Successful bill
            # ------------------------------------------

            if status == "success":
                st.success("Bill generated successfully!")

                rows = []
                catalog = load_catalog()

                for item in result.get("items", []):
                    name = item.get("name", "Unknown item")
                    quantity = item.get("quantity", "")
                    unit = item.get("unit", "")
                    line_total = item.get("line_total", 0)

                    # Find the catalog rate for display.
                    rate = "—"

                    try:
                        match = match_product(name, catalog)

                        if isinstance(match, dict):
                            product = match.get("product", {})
                            if isinstance(product, dict):
                                rate = product.get("rate", "—")
                    except Exception:
                        pass

                    if isinstance(quantity, (int, float)):
                        quantity_text = f"{quantity:g} {unit}".strip()
                    else:
                        quantity_text = f"{quantity} {unit}".strip()

                    rows.append(
                        {
                            "Product": str(name).title(),
                            "Quantity": quantity_text,
                            "Rate (₹)": str(rate),
                            "Amount (₹)": money(line_total).replace("₹", ""),
                        }
                    )

                total = result.get("total", 0)

                # Bill metrics
                metric_a, metric_b, metric_c = st.columns(3)

                metric_a.metric(
                    "Total amount",
                    money(total),
                )
                metric_b.metric(
                    "Items billed",
                    len(rows),
                )
                metric_c.metric(
                    "Billing status",
                    "Complete",
                )

                st.markdown("### 🧺 Bill summary")

                if rows:
                    st.dataframe(
                        pd.DataFrame(rows),
                        use_container_width=True,
                        hide_index=True,
                    )
                else:
                    st.info(
                        "The order was processed, but no billable "
                        "line items were returned."
                    )

                st.markdown("### Total payable")
                st.markdown(
                    f"<h2>{money(total)}</h2>",
                    unsafe_allow_html=True,
                )

                st.caption(
                    "Please verify quantities and catalog prices "
                    "before accepting payment."
                )

                with st.expander("View parsed order data"):
                    st.json(result)

            # ------------------------------------------
            # Products need review
            # ------------------------------------------

            elif status == "needs_review":
                st.warning(
                    "Some items need review before billing. "
                    "No final bill has been issued."
                )

                for item in result.get("unmatched", []):
                    name = item.get("name", "Unknown item")
                    item_status = item.get(
                        "status",
                        "needs review",
                    )

                    with st.container(border=True):
                        st.markdown(f"**{str(name).title()}**")

                        st.caption(
                            "Status: "
                            f"{str(item_status).replace('_', ' ').title()}"
                        )

                        candidates = item.get("candidates", [])

                        if candidates:
                            st.write(
                                "Possible matches:",
                                ", ".join(map(str, candidates)),
                            )

                        st.info(
                            "Check the spelling or use a product name "
                            "and unit that matches the grocery catalog."
                        )

            # ------------------------------------------
            # Empty order
            # ------------------------------------------

            elif status == "empty":
                st.info(
                    "No billable items were found. Try including "
                    "a product name, quantity, and unit."
                )

            # ------------------------------------------
            # Unexpected response
            # ------------------------------------------

            else:
                st.error(
                    "Munshi returned an unexpected result status: "
                    f"{status!r}"
                )

                with st.expander("Technical details"):
                    st.json(result)

        # ----------------------------------------------
        # User-correctable errors
        # ----------------------------------------------

        except ValueError as exc:
            message = str(exc)

            st.error("This order needs a small correction.")
            st.warning(message)

            if (
                "convert" in message.lower()
                or "unit" in message.lower()
            ):
                st.info(
                    "Use a unit that matches how the product is sold. "
                    "For example, enter **1 packet Maggi** instead "
                    "of **500 g Maggi** when the catalog lists "
                    "Maggi by packet."
                )

        # ----------------------------------------------
        # Other errors
        # ----------------------------------------------

        except Exception as exc:
            st.error("Munshi could not process this order.")

            st.info(
                "Check that Ollama is running, the local model is "
                "available, and the product catalog is readable."
            )

            with st.expander("Technical details (for debugging)"):
                st.code(f"{type(exc).__name__}: {exc}")


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.markdown(
    """
    <p class="small-note">
        Munshi · Local AI grocery billing ·
        Always verify the bill before payment.
    </p>
    """,
    unsafe_allow_html=True,
)
