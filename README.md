# 🧾 Munshi — Local AI Grocery Billing

Munshi converts natural-language grocery orders into clear, itemized bills using a locally running AI model.

---

## ✨ Features

- 🗣️ Natural-language grocery order extraction
- 🤖 Local AI inference using Ollama and Qwen 3.5 4B
- 🛒 Product matching against a CSV price catalog
- 🧮 Automatic bill calculation
- 🧾 Itemized bills with quantities, rates, and totals
- ⚠️ Review handling for unmatched products
- 🌐 Interactive Streamlit web interface
- 🧪 Automated tests for billing, catalog, extraction, and order processing

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Pandas
- Ollama
- Qwen 3.5 4B
- Pytest

---

## 📋 Prerequisites

Before running Munshi, make sure you have:

- Python 3.10 or newer
- [Ollama](https://ollama.com/)
- Git

---

## 🚀 Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/pratyushmishra9920-ship-it/munshi-smart-grocery-billing.git
cd munshi-smart-grocery-billing
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Download the local AI model

Make sure Ollama is installed and running.

```powershell
ollama pull qwen3.5:4b
```

### 5. Run the application

```powershell
python -m streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🧪 Run Tests

Run the test suite with:

```powershell
python -m pytest tests -v
```

**Current test result:** 14 tests passed in the local development environment.

---

## 🔒 Privacy

Munshi is designed to process grocery orders using Ollama locally on your computer. Its order-extraction workflow does not require a hosted LLM API.

---

## ⚠️ Important Notes

- Product prices are loaded from `data/pricelist.csv`.
- Use quantities and units that match the products in the catalog.
- Review the generated bill and prices before accepting payment.
- Ollama and the required Qwen model must be available to process orders.

---

## 📁 Project Structure

```text
munshi-smart-grocery-billing/
├── app/
│   ├── __init__.py
│   ├── billing.py
│   ├── catalog.py
│   ├── extractor.py
│   ├── order_service.py
│   └── test_ollama.py
├── data/
│   └── pricelist.csv
├── tests/
│   ├── test_billing.py
│   ├── test_catalog.py
│   ├── test_extractor.py
│   └── test_order_service.py
├── .gitignore
├── app.py
├── requirements.txt
└── README.md
```

---

## 📄 License

No license has been specified yet. Add a license before distributing the project under open-source terms.

