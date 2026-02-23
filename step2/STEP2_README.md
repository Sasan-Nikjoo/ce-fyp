# 📊 Market Data Scraper (Gold & Crude Oil)

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4.x-green.svg)
![Requests](https://img.shields.io/badge/Requests-2.x-orange.svg)

## 📖 Overview
This project is a robust, Python-based web scraping tool designed to extract financial market data, along with its surrounding contextual text and images. The generated dataset is structured specifically for downstream **Sentiment Analysis** and **Vision-Language Model (VLM)** processing to investigate correlations between market prices and digital media semantics.

**Current Targets:**
1. **18K Gold** from [TGJU.org](https://www.tgju.org/)
2. **Brent Crude Oil** from [OilPrice.com](https://oilprice.com/)

---

## ✨ Key Features
- **🎯 Precision Scraping:** Accurately targets and extracts specific price values using unique HTML attributes (e.g., `data-col` and `data-hash`), making it resilient to standard CSS class changes.
- **🧹 Text Purification:** Downloads raw HTML and strips away noise (`<script>`, `<style>`, etc.) to generate clean, pure text files (`pure_text.txt`) ready for Natural Language Processing (NLP).
- **🖼️ Automated Image Harvesting:** Automatically parses the DOM, resolves absolute URLs, and downloads contextually relevant images from the target pages.
- **📂 Structured Output:** Automatically provisions an organized file hierarchy for raw data, clean data, and media assets.

---

## ⚙️ Technical Details & Methodology
- **`requests`:** Configured with a custom `User-Agent` header (`Mozilla/5.0...`) to mimic legitimate browser traffic and bypass basic anti-bot mechanisms (e.g., HTTP 403 Forbidden errors).
- **`BeautifulSoup4`:** Employed as the core HTML parser.
  - **For Gold:** Located via `soup.find('span', attrs={'data-col': 'info.last_trade.PDrCotVal'})`.
  - **For Oil:** Located by first finding the row `soup.find('tr', attrs={'data-hash': 'Brent-Crude'})` and subsequently querying the `<td class="value">` within that node.

---

## 🚀 Getting Started

### Prerequisites
Ensure you have Python installed. It is recommended to use a virtual environment. Install the required dependencies using pip:
```bash
pip install requests beautifulsoup4
```

### Execution
Simply execute the Python script from your terminal:
```bash
python Crawler.py
```

---

## 📁 Output Directory Structure
Upon successful execution, the script generates an `outputs/` directory in the root folder with the following structure:

```text
outputs/
├── gold/
│   ├── images/
│   │   ├── image_1.jpg
│   │   └── ...
│   ├── clean_page.html
│   ├── pure_text.txt
│   └── raw_page.html
└── oil/
    ├── images/
    │   ├── image_1.jpg
    │   └── ...
    ├── clean_page.html
    ├── pure_text.txt
    └── raw_page.html
```