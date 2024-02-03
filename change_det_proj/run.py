from datetime import datetime
import schedule
import time
import pandas as pd
from assignment import detect_changes as assign_detect
from grade import detect_changes as gradecard_detect
from log import log_to_file
from result import detect_changes as result_detect
import random

class ScheduledTasks:
    def __init__(self):
        log_to_file("ScheduledTasks")
        self.assignment_url = "https://admission.ignou.ac.in/changeadmdata/StatusAssignment.ASP?submit=1&enrno=2250992032&program=MCA_NEW"
        self.result_url = "https://termendresult.ignou.ac.in/TermEndDec23/TermEndDec23.asp?eno=2250992032&myhide=1"
        self.gradecard_url = "https://gradecard.ignou.ac.in/gradecard/view_gradecard.aspx?eno=2250992032&prog=MCA_NEW&type=1"
        self.assignment_df = pd.DataFrame()
        self.grade_df = pd.DataFrame()
        self.result_df = pd.DataFrame()

    def evening_task(self):
        self.assignment_df = assign_detect(self.assignment_url, self.assignment_df)
        self.grade_df=gradecard_detect(self.gradecard_url, self.grade_df)
        self.result_df = result_detect(self.result_url, self.result_df)

        
    def schedule_tasks(self):
        # evening_hour = random.randint(16, 17)  # Random hour in the evening (4 PM to 7 PM)
        # evening_minute = random.randint(0, 59)  # Random minute
        # schedule.every().day.at(f"{evening_hour:02d}:{evening_minute:02d}").do(self.evening_task)
        
        
        # afternoon_hour = random.randint(12, 13)  # Random hour in the evening (4 PM to 7 PM)
        # afternoon_minute = random.randint(0, 59)  # Random minute
        # schedule.every().day.at(f"{afternoon_hour:02d}:{afternoon_minute:02d}").do(self.evening_task)

        print(datetime.now().time())
        schedule.every().day.at("16:58").do(self.evening_task)  # 4 PM
        schedule.every().day.at("16:59").do(self.evening_task)  # 8 PM
    def run(self):
        self.schedule_tasks()
        while True:
            schedule.run_pending()
            # Calculate time until the next scheduled task
            next_event = schedule.idle_seconds()
            time_until_next_event = max(next_event, 0)
            print(next_event, " ", time_until_next_event)
            # Sleep exactly until the next scheduled task
            time.sleep(time_until_next_event)

if __name__ == "__main__":
    tasks = ScheduledTasks()
    tasks.run()