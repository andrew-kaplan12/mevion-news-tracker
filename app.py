import streamlit as st
import feedparser
import requests
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import io

# --- Configuration ---
KEYWORDS = [
    "Mevion", "proton therapy", "compact proton therapy", "FLASH radiotherapy",
    "pencil beam scanning", "adaptive proton therapy", "upright proton therapy",
    "Leo Cancer Care", "IBA proton therapy", "Varian proton therapy", "P-Cure",
    "Hitachi proton therapy", "Sumitomo proton", "Stanford proton therapy",
    "Mayo Clinic proton", "UCHealth proton", "Duke proton therapy",
    "CMS proton therapy", "proton therapy reimbursement",
    "proton therapy insurance coverage", "ASTRO payment policy",
    "proton center construction", "proton therapy investment",
    "proton therapy market growth", "value-based oncology proton"
]
DAYS_BACK = 30
MAX_ARTICLES = 200

# --- Streamlit UI ---
st.set_page_config(page_title="Mevion News Tracker")
st.title("📰 Mevion News Tracker")
st.markdown("This tool searches Google News RSS feeds and generates a downloadable PDF of recent, relevant articles.")

# --- News Fetching Logic ---
@st.cache_data
def fetch_articles():
    all_articles = []
    cutoff_date = datetime.now() - timedelta(days=DAYS_BACK)

    for keyword in KEYWORDS:
        rss_url = f"https://news.google.com/rss/search?q={keyword.replace(' ', '+')}&hl=en-US&gl=US&ceid=US:en"
        feed = feedparser.parse(rss_url)

        for entry in feed.entries:
            try:
                pub_date = datetime(*entry.published_parsed[:6])
            except:
                pub_date = datetime.now()

            if pub_date >= cutoff_date:
                try:
                    final_url = requests.get(entry.link, allow_redirects=True, timeout=10).url
                except:
                    final_url = entry.link

                article = {
                    "title": entry.title,
                    "link": final_url,
                    "published": pub_date.strftime('%Y-%m-%d'),
                    "keyword": keyword
                }
                all_articles.append(article)

            if len(all_articles) >= MAX_ARTICLES:
                return all_articles
    return all_articles

# --- PDF Generator ---
def generate_pdf(articles):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=LETTER)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("Proton Therapy News – Links, Dates, and Titles", styles["Title"]))
    content.append(Spacer(1, 0.3 * inch))

    for article in articles:
        content.append(Paragraph(f"<b>{article['title']}</b>", styles["BodyText"]))
        content.append(Paragraph(f"<b>Date:</b> {article['published']} &nbsp;&nbsp; <b>Keyword:</b> {article['keyword']}", styles["BodyText"]))
        content.append(Paragraph(f"<b>Link:</b> <a href='{article['link']}' color='blue'>{article['link']}</a>", styles["BodyText"]))
        content.append(Spacer(1, 0.25 * inch))

    doc.build(content)
    buffer.seek(0)
    return buffer

# --- Main Logic ---
if st.button("Run News Tracker and Generate PDF"):
    with st.spinner("Fetching and generating..."):
        articles = fetch_articles()
        if articles:
            pdf_bytes = generate_pdf(articles)
            st.success(f"✅ {len(articles)} articles found.")
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_bytes,
                file_name="Proton_Therapy_Articles.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("No relevant articles found in the past 30 days.")
