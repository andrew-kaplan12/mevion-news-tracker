# Mevion News Tracker

This Streamlit app tracks recent and relevant news articles related to **proton therapy**, **Mevion Medical Systems**, and the broader oncology technology landscape. It’s designed to help executives and stakeholders stay informed about:

- New developments in proton therapy
- Market trends and competitor activity
- Reimbursement and regulatory news
- Strategic mentions of Mevion and partner institutions

## 🔍 What It Does

The tool pulls data from Google News RSS feeds based on key search terms, and generates a downloadable PDF with:

- Article titles
- Publication dates
- Clickable links
- Associated strategic keywords

## ⚙️ How to Use It (Locally)

1. Clone this repository or download it as a ZIP
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

4. Click the **"Run News Tracker and Generate PDF"** button
5. Download the PDF for internal distribution or review

## ✅ Requirements

- Python 3.9+
- `streamlit`, `feedparser`, `requests`, `reportlab`

## 📦 Deployment

You can deploy this directly to [Streamlit Cloud](https://streamlit.io/cloud) for company-wide access.

## 👥 Maintained By

Andrew Kaplan  
Andrew.kaplan@mevion.com
