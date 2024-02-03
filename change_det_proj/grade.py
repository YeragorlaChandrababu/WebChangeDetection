import pandas as pd
import os
from mail import send_notification_email
import numpy as np

def get_website_table(url, last_table):
    try:
        if last_table.empty:
            tables = pd.read_html(os.path.join(os.getcwd(), 'Grade.html'))
            changed_table = tables[0][['COURSE','Asgn1','LAB1','TERM END THEORY','TERM END PRACTICAL','STATUS' ]]
            changed_table.reset_index(drop=True, inplace=True)
            return changed_table
        else:
            tables=pd.read_html(url)
            df=tables[5][['COURSE','Asgn1','LAB1','TERM END THEORY','TERM END PRACTICAL','STATUS' ]]
            df = df.iloc[:-1]
            return df
    except Exception as e:
        print(f"Error extracting tables from {url}: {e}")
        return None
    
def detect_changes(url, last_table):
    current_table = get_website_table(url,last_table)
    current_table_df = get_formatted_current_df(current_table)
    if current_table is not None:
        if last_table is not None and current_table.to_html()!=last_table.to_html():
            if not last_table.empty and not current_table.empty:
                changed_table = pd.merge(last_table, current_table, how='outer', indicator=True)
                changed_table = changed_table[changed_table['_merge'] == 'right_only'].drop('_merge', axis=1)
                changed_table.reset_index(drop=True, inplace=True)
                current_table_df = get_formatted_current_df(current_table)
                send_notification_email( changed_table, "Grade Card", url,current_table_df)
            else:
                changed_table = last_table if not last_table.empty else current_table
                changed_table.reset_index(drop=True, inplace=True)
                send_notification_email( changed_table, "Grade Card", url)
        return current_table

def get_formatted_current_df( current_table_df):
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
        changed_table_df['LAB1'].replace(0,'NA',inplace=True)    
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
