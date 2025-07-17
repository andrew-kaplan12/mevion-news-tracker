import feedparser
import requests
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import os
import platform

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

# --- Functions ---
def build_rss_url(keyword):
    return f"https://news.google.com/rss/search?q={keyword.replace(' ', '+')}&hl=en-US&gl=US&ceid=US:en"

def resolve_final_url(google_news_url):
    try:
        response = requests.get(google_news_url, allow_redirects=True, timeout=10)
        return response.url
    except requests.RequestException:
        return google_news_url

def fetch_news_articles():
    all_articles = []
    cutoff_date = datetime.now() - timedelta(days=DAYS_BACK)

    for keyword in KEYWORDS:
        feed = feedparser.parse(build_rss_url(keyword))
        for entry in feed.entries:
            try:
                pub_date = datetime(*entry.published_parsed[:6])
            except:
                pub_date = datetime.now()

            if pub_date >= cutoff_date:
                resolved_link = resolve_final_url(entry.link)
                article = {
                    "title": entry.title,
                    "link": resolved_link,
                    "published": pub_date.strftime('%Y-%m-%d'),
                    "keyword": keyword
                }
                all_articles.append(article)
                if len(all_articles) >= MAX_ARTICLES:
                    return all_articles
    return all_articles

def save_basic_pdf(articles, filename):
    doc = SimpleDocTemplate(filename, pagesize=LETTER, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    content = []

    content.append(Paragraph("Proton Therapy News – Links, Dates, and Titles", styles["Title"]))
    content.append(Spacer(1, 0.3 * inch))

    for article in articles:
        content.append(Paragraph(f"<b>{article['title']}</b>", styleN))
        content.append(Paragraph(f"<b>Date:</b> {article['published']} &nbsp;&nbsp; <b>Keyword:</b> {article['keyword']}", styleN))
        content.append(Paragraph(f"<b>Link:</b> <a href='{article['link']}' color='blue'>{article['link']}</a>", styleN))
        content.append(Spacer(1, 0.25 * inch))

    doc.build(content)
    print(f"✅ Saved PDF to {filename}")

# --- Main ---
if __name__ == "__main__":
    print("📡 Fetching news articles...")
    articles = fetch_news_articles()
    output_path = "Proton_Therapy_Articles.pdf"
    if articles:
        save_basic_pdf(articles, output_path)
    else:
        print("⚠️ No articles found.")

