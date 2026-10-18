# 🧾 Munshi — Local AI Grocery Billing

Munshi converts natural-language grocery orders into itemized bills using a locally running AI model.

## ✨ Features

- Natural-language grocery order extraction
- Local AI inference with Ollama and Qwen 3.5 4B
- Product matching against a CSV price catalog
- Automatic bill calculation
- Itemized bill with quantities, rates, and totals
- Review handling for unmatched products
- Streamlit web interface
- Automated tests for billing, catalog, extraction, and order processing

## 🛠️ Tech Stack

- Python
- Streamlit
- Pandas
- Ollama
- Qwen 3.5 4B
- Pytest

## 📋 Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/)
- Git


## 🚀 Setup

### 1. Clone the repository

```bash
git clone https://github.com/pratyushmishra9920-ship-it/munshi-smart-grocery-billing.git
cd munshi-smart-grocery-billing
```

### 2. Create a virtual environment

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

Make sure [Ollama](https://ollama.com/) is installed, then run:

```powershell
ollama pull qwen3.5:4b
```

### 5. Run Munshi

```powershell
python -m streamlit run app.py
```

Open http://localhost:8501 in your browser.

## 🧪 Run Tests

```powershell
python -m pytest tests -v
```

## 🔒 Privacy

Order extraction is designed to run through Ollama locally. This project does not require a hosted LLM API for that workflow.

## ⚠️ Important

- Product prices are read from the local catalog at `data/pricelist.csv`.
- Use units that match how products are sold in the catalog.
- Review the generated bill before accepting payment.

## 📁 Project Structure

```text
munshi/
├── app/
│   ├── billing.py
│   ├── catalog.py
│   ├── extractor.py
│   └── order_service.py
├── data/
│   └── pricelist.csv
├── tests/
├── app.py
├── requirements.txt
└── README.md
```

## 📄 License

Add a license before distributing this project publicly.
