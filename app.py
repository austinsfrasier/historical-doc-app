import streamlit as st
import pandas as pd

st.set_page_config(page_title="Historical Document App", layout="wide")
st.title("Historical Document App")

uploaded_files = st.file_uploader(
    "Upload PDF or image files",
    type=["pdf", "jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_files:
    rows = []
    for f in uploaded_files:
        rows.append({
            "filename": f.name,
            "title": "",
            "author": "",
            "date": "",
            "subject": "",
            "recipient": "",
            "summary": "",
            "location": ""
        })

    df = pd.DataFrame(rows)
    st.subheader("Extracted metadata")
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download CSV",
        data=csv,
        file_name="metadata.csv",
        mime="text/csv"
    )
else:
    st.info("Upload one or more files to begin.")
