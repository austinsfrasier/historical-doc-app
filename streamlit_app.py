import streamlit as st
import pandas as pd
from pypdf import PdfReader
from io import BytesIO

st.set_page_config(page_title="Historical Document App", layout="wide")
st.title("Historical Document App")
st.markdown("Upload PDFs or images to begin extracting metadata.")

def extract_pdf_text(uploaded_file) -> str:
    try:
        uploaded_file.seek(0)
        pdf_bytes = BytesIO(uploaded_file.read())
        reader = PdfReader(pdf_bytes)
        text_parts = []

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)

        return "\n".join(text_parts).strip()
    except Exception as e:
        return f"[PDF extraction error: {e}]"

uploaded_files = st.file_uploader(
    "Upload files",
    type=["pdf", "jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_files:
    data = []

    for file in uploaded_files:
        summary_text = ""

        if file.name.lower().endswith(".pdf"):
            summary_text = extract_pdf_text(file)[:500]
        else:
            summary_text = "[Image uploaded - OCR not added yet]"

        data.append({
            "filename": file.name,
            "title": "",
            "author": "",
            "date": "",
            "subject": "",
            "recipient": "",
            "summary": summary_text,
            "location": ""
        })

    df = pd.DataFrame(data)

    st.subheader("Extracted metadata")
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "metadata.csv", "text/csv")

    st.subheader("Text preview")
    for _, row in df.iterrows():
        st.markdown(f"**{row['filename']}**")
        st.text(row["summary"] if row["summary"] else "[No text extracted]")
        st.markdown("---")
else:
    st.info("Upload one or more files to begin.")
