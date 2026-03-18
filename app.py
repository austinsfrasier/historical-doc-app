import streamlit as st
import pandas as pd

st.set_page_config(page_title="Historical Document App", layout="wide")
st.title("Historical Document App")
st.success("App is live.")

uploaded_files = st.file_uploader(
    "Upload PDF or image files",
    type=["pdf", "jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_files:
    df = pd.DataFrame([{"filename": f.name} for f in uploaded_files])
    st.subheader("Uploaded files")
    st.dataframe(df, use_container_width=True)
else:
    st.info("Upload one or more files to begin.")
