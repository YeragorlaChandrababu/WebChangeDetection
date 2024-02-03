import pandas as pd
from mail import send_notification_email
import os

def get_website_tables(url, last_table):
    try:
        if last_table.empty:
            tables = pd.read_html(os.path.join(os.getcwd(), 'Assign.html'))
            return tables[0]
        else:
            tables = pd.read_html(url, flavor='bs4',header=0, skiprows=[0,1])
            return tables[1]
    except Exception as e:
        print(f"Error extracting tables from {url}: {e}")
        return None
    
def detect_changes(url, last_table):
    current_table = get_website_tables(url, last_table)
    if current_table is not None:
        if last_table is not None and current_table.to_html() != last_table.to_html():
            if not last_table.empty and not current_table.empty:
                changed_table = pd.merge(last_table, current_table, how='outer', indicator=True)
                changed_table = changed_table[changed_table['_merge'] == 'right_only'].drop('_merge', axis=1)
                changed_table.reset_index(drop=True, inplace=True)
                changed_table = changed_table.drop('Unnamed: 0', axis=1)
                changed_table.reset_index(drop=True, inplace=True)
                send_notification_email(changed_table, "Assignment",url)
            else:
                changed_table = last_table if not last_table.empty else current_table
                changed_table.reset_index(drop=True, inplace=True)
                changed_table = changed_table.drop('Unnamed: 0', axis=1)
                changed_table.reset_index(drop=True, inplace=True)
                send_notification_email(changed_table, "Assignment",url)
        return current_table
