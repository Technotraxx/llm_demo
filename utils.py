import streamlit as st
import os
import time
import base64
import pandas as pd
import smtplib
import chardet
import requests
import re

from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pypdf import PdfReader
from docx import Document

def load_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ''.join(page.extract_text() for page in reader.pages)
    word_count = len(text.split())
    return text, word_count

def load_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ''.join(page.extract_text() for page in reader.pages)
    word_count = len(text.split())
    return text, word_count

def load_docx(uploaded_file):
    doc = Document(uploaded_file)
    text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    word_count = len(text.split())
    return text, word_count

def load_txt(uploaded_file):
    text = uploaded_file.read().decode("utf-8")
    word_count = len(text.split())
    return text, word_count

def load_csv(uploaded_file):
    # Bestimmen der Kodierung
    rawdata = uploaded_file.read()
    result = chardet.detect(rawdata)
    charenc = result['encoding']
    uploaded_file.seek(0)  # Setze den Dateizeiger zurück

    # Lesen der CSV-Datei mit Fehlerbehandlung für problematische Zeilen
    df = pd.read_csv(uploaded_file, encoding=charenc, on_bad_lines='skip')
    text = df.to_string()
    word_count = len(text.split())
    return text, word_count

def load_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    text = ' '.join([para.get_text() for para in paragraphs])
    word_count = len(text.split())
    return text, word_count
 
def reload_page():
    st.experimental_rerun()

def generate_unique_filename(prefix, extension):
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")  # Format: Jahr-Monat-Tag_Stunde-Minute-Sekunde
    unique_id = base64.urlsafe_b64encode(os.urandom(6)).decode('utf-8').rstrip('=')
    return f"{prefix}_{timestamp}_{unique_id}.{extension}"

def save_text(filename, text):
    with open(filename, "w") as file:
        file.write(text)

def save_csv(filename, text):
    with open(filename, "w") as file:
        file.write(text)

def save_doc(filename, text):
    with open(filename, "w") as file:
        file.write(text)

def save_xls(filename, text):
    with open(filename, "w") as file:
        file.write(text)

def send_email(subject, body, to_email, from_email, password):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        st.success("Email sent successfully!")
    except Exception as e:
        st.error(f"Failed to send email: {e}")
