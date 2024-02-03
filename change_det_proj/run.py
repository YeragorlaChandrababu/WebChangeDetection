from datetime import datetime
import schedule
import time
import pandas as pd
from grade import detect_changes as gradecard_detect
from log import log_to_file
from result import detect_changes as result_detect
from mail import send_log_file
import random

class ScheduledTasks:
    def __init__(self):
        log_to_file("Scheduled Tasks")
        # self.assignment_url = "https://admission.ignou.ac.in/changeadmdata/StatusAssignment.ASP?submit=1&enrno=2250992032&program=MCA_NEW"
        self.result_url = "https://termendresult.ignou.ac.in/TermEndDec23/TermEndDec23.asp?eno=2250992032&myhide=1"
        self.gradecard_url = "https://gradecard.ignou.ac.in/gradecard/view_gradecard.aspx?eno=2250992032&prog=MCA_NEW&type=1"
        self.assignment_df = pd.DataFrame()
        self.grade_df = pd.DataFrame()
        self.result_df = pd.DataFrame()

    def run_task(self):
        log_to_file("Calling Tasks")
        # self.assignment_df = assign_detect(self.assignment_url, self.assignment_df)
        self.grade_df=gradecard_detect(self.gradecard_url, self.grade_df)
        self.result_df = result_detect(self.result_url, self.result_df)

        
    def schedule_tasks(self):
        log_to_file("Current Date & Time "+ str(datetime.now().time()))
        for hour in range(4, 15):
            random_minute = random.randint(0, 59)
            schedule_time = f"{hour:02d}:{random_minute:02d}"
            schedule.every().hour.at(schedule_time).do(self.run_task)
            if hour == 14:
                send_log_file()
            
    def run(self):
        log_to_file("Run")
        self.schedule_tasks()
        while True:
            schedule.run_pending()
            next_event = schedule.idle_seconds()
            time_until_next_event = max(next_event, 0)
            log_to_file("Will be running in next: "+str(next_event/60)+ " minutes")
            time.sleep(time_until_next_event)
            

if __name__ == "__main__":
    tasks = ScheduledTasks()
    tasks.run()