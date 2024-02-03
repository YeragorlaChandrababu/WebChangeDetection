import pandas as pd
from mail import send_notification_email

def get_website_table(url, last_table):
    try:
        tables = pd.read_html(url, header=0)
        if tables:
            return tables[0]
        else:
            return last_table 
    except Exception as e:
        print(f"Error extracting tables from {url}: {e}")
        return None
    
def detect_changes(url, last_table):
    current_tables = get_website_table(url, last_table)
    if current_tables is not None:
        if last_table is not None and current_tables.to_html() != last_table.to_html():
            if not last_table.empty and not current_tables.empty:
                changed_table = pd.merge(last_table, current_tables, how='outer', indicator=True)
                changed_table = changed_table[changed_table['_merge'] == 'right_only'].drop('_merge', axis=1)
                changed_table.reset_index(drop=True, inplace=True)
                send_notification_email(changed_table, "Result",url)
            else:
                changed_table = last_table if not last_table.empty else current_tables
                changed_table.reset_index(drop=True, inplace=True)
                send_notification_email(changed_table, "Result",url)

        return current_tables