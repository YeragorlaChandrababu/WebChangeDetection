import pandas as pd
import os
from mail import send_notification_email
import numpy as np
from log import log_to_file

def get_website_table(url):
    log_to_file("Grade Card - Get from Web")
    try:
        tables=pd.read_html(url)
        grade_df=tables[5][['COURSE','Asgn1','LAB1','TERM END THEORY','TERM END PRACTICAL','STATUS' ]]
        grade_df = grade_df.iloc[:-1]
        return grade_df
    except Exception as e:
        log_to_file(f"Error extracting tables from {url}: {e}")
        return None
    
def detect_changes(url, last_table):
    log_to_file("Grade Card - Detect Changes")
    current_table = get_website_table(url)
    current_table_df = get_formatted_current_df(current_table)
    if current_table_df is not None:
        if last_table is not None and current_table_df.to_html()!=last_table.to_html():
            current_table_df.reset_index(drop=True, inplace=True)
            send_notification_email(current_table_df, "Grade Card", url)
    return current_table_df

def get_formatted_current_df( current_table_df):
        log_to_file("Grade Card - Content Extraction")
        course_code_map = {
        "MCS211":'Design and Analysis of Algorithms',
        "MCS212":'Discrete Mathematics',
        "MCS213":'Software Engineering',
        "MCS214":'Professional Skills and Ethics',
        "MCS215":'Security and Cyber Laws',
        "MCSL216":'DAA and Web Design Lab',
        "MCSL217":'Software Engineering Lab',
        "MCS218":'Data Communication and Computer Networks',
        "MCS219":'Object Oriented Analysis and Design',
        "MCS220":'Web Technologies',
        "MCS221":'Data Warehousing and Data Mining',
        "MCSL222":'OOAD and Web Technologies Lab',
        "MCSL223":'Computer Networks and Data Mining Lab',
        "MCS224":'Artificial Intelligence and Machine Learning',
        "MCS225":"Accountancy and Financial Management",
        "MCS226":"Data Science and Big Data",
        "MCS227":"Cloud Computing and IoT",
        "MCSL228":"AI and Machine Learning Lab",
        "MCSL229":"Cloud and Data Science Lab"
        }
        changed_table_df = current_table_df[~current_table_df['COURSE'].str.contains('MCS201|MCS208')]
        changed_table_df.reset_index(drop=True,inplace=True)
        changed_table_df = changed_table_df.copy()
        changed_table_df.replace('-',0,inplace=True)
        changed_table_df['TERM END PRACTICAL'] = changed_table_df['TERM END PRACTICAL'].astype(int)
        changed_table_df['TERM END THEORY'] = changed_table_df['TERM END THEORY'].astype(int)
        changed_table_df['LAB1'] = changed_table_df['LAB1'].astype(int)
        changed_table_df['Asgn1'] = changed_table_df['Asgn1'].astype(int)
        changed_table_df['Course Name'] = changed_table_df['COURSE'].map(course_code_map)
        changed_table_df['Theory/Practical Marks'] = changed_table_df['TERM END THEORY']+changed_table_df['TERM END PRACTICAL']
        conditions = changed_table_df['COURSE'].isin(["MCSL216", "MCSL222", "MCSL223"])

# Assign values based on conditions
        changed_table_df['Max Marks'] = np.where(conditions, 300, 200)
        # print(changed_table_df[['COURSE', 'Course Name', 'Asgn1', 'LAB1', 'TERM END THEORY',
        #       'TERM END PRACTICAL','STATUS', 'Max Marks']])
        # changed_table_df.to_html("C:\Users\cyera\Python\ChangeDetection\change_det_proj\Fen.html",index=0)
        changed_table_df['Max Marks'] = changed_table_df['Max Marks'].astype(int)
        total_sum_of_marks = str(changed_table_df['Max Marks'].sum())
        
        prac_Sum = changed_table_df['TERM END PRACTICAL'].sum()
        
        the_Sum = changed_table_df['TERM END THEORY'].sum()
        lab_sum=changed_table_df['LAB1'].sum()
        num_rows = changed_table_df.shape[0]
        assig_Sum=changed_table_df['Asgn1'].sum()
        ssum = the_Sum+prac_Sum+assig_Sum+lab_sum
        cond = changed_table_df['STATUS'].str.contains('Not',case=False)
        noofSubsF=0
        noofSubsF += np.sum(cond)
        if(changed_table_df["STATUS"].str.contains('Not', case=False)).any()or num_rows<5:
                fresult="Fail"
        else:
                fresult="Pass"
        changed_table_df.loc[changed_table_df['STATUS'].str.contains("NOT"), 'STATUS'] = "Fail"
        changed_table_df.loc[changed_table_df['STATUS'].str.contains("COMPLETED"), 'STATUS'] = "Pass"
        changed_table_df['LAB1'] = changed_table_df['LAB1'].replace(0, 'NA')
        changed_table_df=changed_table_df[['COURSE', 'Course Name', 'Theory/Practical Marks', 'Asgn1','LAB1','Max Marks','STATUS']].reset_index(drop=True)
        
        changed_table_df.loc[len(changed_table_df)]=["Total",num_rows,the_Sum+prac_Sum, assig_Sum,lab_sum, total_sum_of_marks, fresult]
        changed_table_df.loc[len(changed_table_df)]=["","","Grand Total",":-",ssum, total_sum_of_marks, fresult]
        # changed_table_df.loc[len(changed_table_df)+1] = ['Name: '+name+' Reg No: '+i, num_rows, lab_sum+the_Sum+prac_Sum, total_sum_of_marks, fresult]
        changed_table_df=changed_table_df.rename(columns={'COURSE':'Course Code', 'Asgn1':'Assignments', 'LAB1':'Lab', 'STATUS':'Result'})
        changed_table_df.reset_index(drop=True,inplace=True)
        # new_df.loc[len(new_df)] = ['Name', 'Reg No.',
        #                            'No.of Subj', 'Sec.Marks', 'Total', 'Result']
        # new_df.loc[len(new_df)+1] = [name,i, num_rows,noofSubsF,ssum, total_sum_of_marks, fresult]
        # new_df.reset_index(drop=True)
        return changed_table_df
