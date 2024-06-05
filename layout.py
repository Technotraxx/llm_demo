import streamlit as st
from utils import save_text, save_csv, save_doc, save_xls, generate_unique_filename

def create_output_area(summary):
    st.header("Summary Output")
    st.write(summary)

    st.header("Save and Send Options")

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Save as TXT", key="save_txt_button"):
            filename = generate_unique_filename("summary", "txt")
            save_text(filename, summary)
            st.success(f"Saved as {filename}")
            with open(filename, "r") as file:
                st.download_button(label="Download TXT", data=file, file_name=filename)

    with col2:
        if st.button("Save as CSV", key="save_csv_button"):
            filename = generate_unique_filename("summary", "csv")
            save_csv(filename, summary)
            st.success(f"Saved as {filename}")
            with open(filename, "r") as file:
                st.download_button(label="Download CSV", data=file, file_name=filename)

    with col3:
        if st.button("Save as DOCX", key="save_docx_button"):
            filename = generate_unique_filename("summary", "docx")
            save_doc(filename, summary)
            st.success(f"Saved as {filename}")
            with open(filename, "r") as file:
                st.download_button(label="Download DOCX", data=file, file_name=filename)

    with col4:
        if st.button("Save as XLSX", key="save_xlsx_button"):
            filename = generate_unique_filename("summary", "xlsx")
            save_xls(filename, summary)
            st.success(f"Saved as {filename}")
            with open(filename, "r") as file:
                st.download_button(label="Download XLSX", data=file, file_name=filename)
