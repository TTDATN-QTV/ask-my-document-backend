import streamlit as st
from mvp_ui.utils.api import upload_pdf, ask_question

st.set_page_config(page_title="Ask My Document", layout="wide")
st.title("Ask My Document")

# --- Upload PDF ---
st.header("1. Upload PDF")
uploaded_files = st.file_uploader("Choose PDF files", type=["pdf"], accept_multiple_files=True)
file_ids = st.session_state.get("file_ids", [])

if uploaded_files:
    if st.button("Upload PDFs"):
        new_file_ids = []
        for uploaded_file in uploaded_files:
            with st.spinner(f"Uploading {uploaded_file.name}..."):
                response = upload_pdf(uploaded_file)
            if response.ok:
                data = response.json()
                st.success(f"Uploaded {uploaded_file.name}!")
                st.write(data)
                file_id = data.get("file_id")
                if file_id:
                    new_file_ids.append(file_id)
            else:
                st.error(response.text)

        # Save the new file IDs to session
        st.session_state["file_ids"] = new_file_ids
        file_ids = new_file_ids

# --- Ask a question ---
st.header("2. Ask a question")
query = st.text_input("Your question:")
top_k = st.number_input("Top K context chunks", min_value=1, max_value=10, value=2)
file_ids_input = st.session_state.get("file_ids", [])

st.write(f"Current file IDs: {file_ids_input}")

if st.button("Ask") and query and file_ids_input:
    with st.spinner("Getting answer..."):
        response = ask_question(query, top_k, file_ids_input)
    if response.ok:
        result = response.json()
        st.subheader("Answer")
        st.write(result.get("answer", "No answer"))
        st.subheader("Context")
        context_chunks = result.get("context", [])
        for chunk in context_chunks:
            st.markdown(f"**File:** {chunk['file_name']} | **Page:** {chunk['page_number']}")
            st.write(chunk['content'])
            pdf_path = f"data/uploads/{chunk['file_id']}.pdf"
            if st.button(f"Open {chunk['file_name']} - Page {chunk['page_number']}", key=f"{chunk['file_id']}_{chunk['page_number']}"):
                st.markdown(f"[Open PDF]({pdf_path})")
    else:
        st.error(response.text)
