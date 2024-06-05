import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import time
import base64

def reload_page():
    st.experimental_rerun()

def generate_unique_filename(prefix, extension):
    timestamp = int(time.time())
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
