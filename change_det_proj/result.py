import pandas as pd
from mail import send_notification_email
from log import log_to_file

def get_website_table(url):
    log_to_file("Result - Get from Web")
    try:
        tables = pd.read_html(url, header=0)
        if tables:
            return tables[0]
    except Exception as e:
        log_to_file(f"Error extracting tables from {url}: {e}")
        return None
    
def detect_changes(url, last_table):
    log_to_file("Result - Detect Changes")
    current_tables = get_website_table(url)
    if current_tables is not None:
        if last_table is not None and current_tables.to_html() != last_table.to_html():
                current_tables.reset_index(drop=True, inplace=True)
                send_notification_email(current_tables, "Result",url)
        return current_tables