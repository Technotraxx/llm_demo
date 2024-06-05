# utils.py

import streamlit as st
import pandas as pd
from docx import Document
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def save_text(content, filename):
    with open(filename, 'w') as file:
        file.write(content)
    st.success(f"Saved as {filename}")

def save_csv(content, filename):
    df = pd.DataFrame({"Summary": [content]})
    df.to_csv(filename, index=False)
    st.success(f"Saved as {filename}")

def save_doc(content, filename):
    doc = Document()
    doc.add_paragraph(content)
    doc.save(filename)
    st.success(f"Saved as {filename}")

def save_xls(content, filename):
    df = pd.DataFrame({"Summary": [content]})
    df.to_excel(filename, index=False)
    st.success(f"Saved as {filename}")

def send_email(subject, body, to_email, from_email, from_password):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, from_password)
            text = msg.as_string()
            server.sendmail(from_email, to_email, text)
        st.success(f"Email sent to {to_email}")
    except Exception as e:
        st.error(f"Failed to send email: {e}")
