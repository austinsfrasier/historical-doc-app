import streamlit as st
import pandas as pd

st.set_page_config(page_title="Historical Document App", layout="wide")

st.title("Historical Document App")
st.markdown("Upload PDFs or images to begin extracting metadata.")

uploaded_files = st.file_uploader(
    "Upload files",
    type=["pdf", "jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_files:
    data = []

    for file in uploaded_files:
        data.append({
            "filename": file.name,
            "title": "",
            "author": "",
            "date": "",
            "subject": "",
            "recipient": "",
            "summary": "",
            "location": ""
        })

    df = pd.DataFrame(data)

    st.subheader("Extracted metadata")
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "metadata.csv", "text/csv")

else:
    st.info("Upload one or more files to begin.")
