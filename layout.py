import streamlit as st
from utils import save_text, save_csv, save_doc, save_xls, generate_unique_filename

def create_sidebar():
    # Sidebar für Modell-Auswahl und Einstellungen
    st.sidebar.title("Settings")

def create_main_area():
    st.title("PDF Text Summarizer with Multiple LLMs")

    # PDF-Upload
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf", key="pdf_uploader")
    return uploaded_file

def create_output_area(summary):
    if summary:
        st.header("Output")
        st.write("Summary:")

        st.markdown(summary)
        st.divider()

        # Display the summary using markdown
        with st.expander("Copy to Clipboard"):
            st.code(summary, language='markdown', line_numbers=True)

        with st.expander("Save and Send Options"):
            # Save options
            st.write("Save the summary:")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("Save as TXT", key="save_txt_button"):
                    filename = generate_unique_filename("summary", "txt")
                    save_text(filename, summary)
                    st.success(f"Saved as {filename}")
                    with open(filename, "r") as file:
                        st.download_button(label="Download TXT", data=file, file_name=filename, mime="text/plain")
            with col2:
                if st.button("Save as CSV", key="save_csv_button"):
                    filename = generate_unique_filename("summary", "csv")
                    save_csv(filename, summary)
                    st.success(f"Saved as {filename}")
                    with open(filename, "r") as file:
                        st.download_button(label="Download CSV", data=file, file_name=filename, mime="text/csv")
            with col3:
                if st.button("Save as DOC", key="save_doc_button"):
                    filename = generate_unique_filename("summary", "docx")
                    save_doc(filename, summary)
                    st.success(f"Saved as {filename}")
                    with open(filename, "rb") as file:
                        st.download_button(label="Download DOC", data=file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            with col4:
                if st.button("Save as XLS", key="save_xls_button"):
                    filename = generate_unique_filename("summary", "xlsx")
                    save_xls(filename, summary)
                    st.success(f"Saved as {filename}")
                    with open(filename, "rb") as file:
                        st.download_button(label="Download XLS", data=file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

            # Email option
            st.write("Send the summary via email:")
            email_address = st.text_input("Email address", key="email_address")
            if st.button("Send Email", key="send_email_button"):
                send_email("Summary from Multiple LLMs", summary, email_address, st.secrets["email"], st.secrets["email_password"])
            save_xls(filename, summary)
            st.success(f"Saved as {filename}")
            with open(filename, "r") as file:
                st.download_button(label="Download XLSX", data=file, file_name=filename)
