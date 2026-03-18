import streamlit as st
import pandas as pd
from pypdf import PdfReader
from io import BytesIO

st.set_page_config(page_title="Historical Document App", layout="wide")
st.title("Historical Document App")

def extract_pdf_text(uploaded_file) -> str:
    try:
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
    "Upload PDF or image files",
    type=["pdf", "jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_files:
    rows = []

    for f in uploaded_files:
        extracted_text = ""

        if f.type == "application/pdf" or f.name.lower().endswith(".pdf"):
            extracted_text = extract_pdf_text(f)
        else:
            extracted_text = "[Image uploaded - OCR not added yet]"

        preview = extracted_text[:500] if extracted_text else ""

        rows.append({
            "filename": f.name,
            "title": "",
            "author": "",
            "date": "",
            "subject": "",
            "recipient": "",
            "summary": preview,
            "location": ""
        })

    df = pd.DataFrame(rows)

    st.subheader("Extracted metadata")
    st.dataframe(df, use_container_width=True)

    st.subheader("Preview")
    for _, row in df.iterrows():
        st.markdown(f"**{row['filename']}**")
        st.text(row["summary"] if row["summary"] else "[No text extracted]")
        st.markdown("---")

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download CSV",
        data=csv,
        file_name="metadata.csv",
        mime="text/csv"
    )
else:
    st.info("Upload one or more files to begin.")
