import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Mevion News Tracker")
st.title("📰 Proton Therapy News Tool")

st.markdown("""
This tool searches Google News RSS feeds for strategic terms related to proton therapy and Mevion's ecosystem. 
It generates a PDF report with clickable article links from the past 14 days.
""")

if st.button("Run News Tracker and Generate PDF"):
    with st.spinner("Running scraper and generating PDF..."):
        result = subprocess.run(["python", "scraper.py"], capture_output=True, text=True)

    st.success("✅ Done! PDF generated.")

    pdf_path = "Proton_Therapy_Articles.pdf"
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            st.download_button("📄 Download PDF", f, file_name=pdf_path)
    else:
        st.error("PDF not found. Please check the scraper output.")
