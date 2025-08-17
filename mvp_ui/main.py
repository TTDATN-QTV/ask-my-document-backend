import streamlit as st
from mvp_ui.utils.api import upload_pdf, ask_question

st.set_page_config(page_title="Ask My Document", layout="wide")
st.title("Ask My Document")

# --- Upload PDF ---
st.header("1. Upload PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
file_id = st.session_state.get("file_id", "")

if uploaded_file:
    if st.button("Upload PDF"):
        with st.spinner("Uploading and indexing..."):
            response = upload_pdf(uploaded_file)
        if response.ok:
            data = response.json()
            st.success("Upload successful!")
            st.write(data)
            file_id = data.get("file_id")
            st.session_state["file_id"] = file_id
        else:
            st.error(response.text)

# --- Ask a question ---
st.header("2. Ask a question")
query = st.text_input("Your question:")
top_k = st.number_input("Top K context chunks", min_value=1, max_value=10, value=2)
file_id_input = st.text_input("File ID (from upload)", value=file_id)

if st.button("Ask") and query and file_id_input:
    with st.spinner("Getting answer..."):
        response = ask_question(query, top_k, file_id_input)
    if response.ok:
        result = response.json()
        st.subheader("Answer")
        st.write(result.get("answer", "No answer"))
        st.subheader("Context")
        st.write(result.get("context", []))
    else:
        st.error(response.text)
