from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os
import pandas as pd
import smtplib
from email.mime.base import MIMEBase
from email import encoders
from log import log_to_file

def send_notification_email(changed_df, content, url):
        changed_df = pd.DataFrame(changed_df)
        log_to_file("Mail Service - "+changed_df.to_string())
        email_config = {
        'sender_email': 'yeragorla.b@gmail.com',
        'recipient_email': 'cyeragorla@gmail.com',
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 465,
        'email_password': 'cybt atzk plut avhf'
        }
        current_time = datetime.now().time()
        formatted_time = current_time.strftime("%I:%M:%S %p")
        subject = f"Change observed in the {content} status: {formatted_time}"
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = email_config['sender_email']
        msg["To"] = email_config['recipient_email']
        body = f"{content} Status Changed at: \n{url}<br><br>"
        if not changed_df.empty:
            body += f"<br>{changed_df.to_html(index=False)}<br><br>"
        else:
            body += "No tables found on the website."
        msg.attach(MIMEText(body, "html"))
        with smtplib.SMTP_SSL(email_config['smtp_server'], email_config['smtp_port']) as server:
            server.login(email_config['sender_email'], email_config['email_password'])
            server.sendmail(email_config['sender_email'], [email_config['recipient_email']], msg.as_string())

def send_log_file():
        log_to_file("Mail Service - Send Log File")
        email_config = {
        'sender_email': 'yeragorla.b@gmail.com',
        'recipient_email': 'cyeragorla@gmail.com',
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 465,
        'email_password': 'cybt atzk plut avhf'
        }
        current_time = datetime.now().time()
        formatted_time = current_time.strftime("%I:%M:%S %p")
        subject = f"Today's Log File: {formatted_time}"
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = email_config['sender_email']
        msg["To"] = email_config['recipient_email']
        body = f"Please find the log file for: {formatted_time}<br><br>"
        log_file_path = os.path.join(os.getcwd(), 'logfile.txt')
        attachment = open(log_file_path, "rb")
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename=logfile.txt")
        msg.attach(part)
        msg.attach(MIMEText(body, "html"))
        with smtplib.SMTP_SSL(email_config['smtp_server'], email_config['smtp_port']) as server:
            server.login(email_config['sender_email'], email_config['email_password'])
            server.sendmail(email_config['sender_email'], [email_config['recipient_email']], msg.as_string())