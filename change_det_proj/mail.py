from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import pandas as pd

def send_notification_email(changed_df, content, url, complete_df=None):
        changed_df = pd.DataFrame(changed_df)
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
        body = f"{content} Status Changed at: \n{url}.<br><br>"
        if not changed_df.empty:
            body += f"<br>{changed_df.to_html(index=False)}<br><br>"
            if complete_df is not None :
                body += f"<br>{complete_df.to_html(index=False)}<br><br>"
        else:
            body += "No tables found on the website."
        msg.attach(MIMEText(body, "html"))
        with smtplib.SMTP_SSL(email_config['smtp_server'], email_config['smtp_port']) as server:
            server.login(email_config['sender_email'], email_config['email_password'])
            server.sendmail(email_config['sender_email'], [email_config['recipient_email']], msg.as_string())