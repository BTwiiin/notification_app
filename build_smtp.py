import smtplib
from notification import *
from _datetime import datetime
import time
import pandas as pd
import os


class Server:
    #Constructor with the list of notifications and name of the file path
    def __init__(self):
        self.notifications = []
        self.file_path = 'data.json'
    
    # Function "pandas_frame" checks if the file exists and opens it
    def pandas_frame(self):
        try:
            os.path.exists(self.file_path)
            df = pd.read_json(self.file_path)
            return df
        except Exception as e:
            print(f'Error opening file : {str(e)}')
    
    # Function "main_loop" is just a main loop of the program :)
    def main_loop(self):
        df = self.pandas_frame()
        # If JSON file is empty we will ask user to create some new notification ( it's not completed rn)
        if df.empty:
            self.add_notification('remindersfrompy@gmail.com', 'Test Email', 'With Class',
                                  year=2023, month=3, day=13, hour=22)
            self.add_notification('remindersfrompy@gmail.com', 'Test Email', 'With Class',
                                  year=2024, month=4, day=14, hour=24)
        # Else we write everything from JSON file to our list
        else:
            j = max(df.index)
            i = 0
            while i != j:
                self.from_json_to_list(df.iloc[i, 0], df.iloc[i, 1], df.iloc[i, 2], df.iloc[i, 3],
                                       df.iloc[i, 4], df.iloc[i, 5], df.iloc[i, 6])
                #print(self.notifications[i].print_not())
                i += 1
        # While we have notifications, program will not stop
        while len(self.notifications) != 0:
            now = datetime.now()
            if self.notifications[0].get_year() == now.year:
                if self.notifications[0].get_month() == now.month:
                    if self.notifications[0].get_day() == now.day:
                        if self.notifications[0].get_hour() == now.hour:
                            self._init_serv(self.notifications[0])
                            del self.notifications[0]
            print(f'{now.hour}')
            time.sleep(1)

    # Function "add_notification" creates a Notification object and append this object to the 'self.notifications' list
    # and also appends notification to a JSON file if it exists or creates new DATAFRAME and converts it to JSON format
    def add_notification(self, receiver_email, subject, body, year, month, day, hour):
        note = Notification(receiver_email, subject, body, year, month, day, hour)
        self.notifications.append(note)
        self.sort_by_time()
        df = pd.read_json(self.file_path)
        if df.empty:
            new_data = {"receiver_email": receiver_email, "subject": subject, "body": body,
                        "year": year, "month": month, "day": day, "hour": hour}
            df = pd.DataFrame(new_data, index=[1])
            df.to_json(self.file_path, indent=4)
        else:
            new_data = {"receiver_email": receiver_email, "subject": subject, "body": body,
                        "year": year, "month": month, "day": day, "hour": hour}
            df = pd.concat([df, pd.DataFrame(new_data, index=[max(df.index) + 1 ])])
            df.to_json(self.file_path, indent=4)
    
    # Function "from_json_to_list" adds notification to our list at the beggining of the program
    def from_json_to_list(self, receiver_email, subject, body, year, month, day, hour):
        note = Notification(receiver_email, subject, body, year, month, day, hour)
        self.notifications.append(note)
        self.sort_by_time()


    # Function "_init_serv" establishes connection with host server and logins senders email. If something goes wrong it
    # throws an exception with Error description
    def _init_serv(self, notification):
        try:
            status = server = smtplib.SMTP(notification.get_server_host(), 587)
            print(f'Establishing connection: {status}')
            status = server.starttls()
            print(f'TLS {status}')
            status = server.login('remindersfrompy@outlook.com', 'Milana2412')
            print(f'Logging in {status}')

            self.send(server, notification)
            self.quit(server)
        except Exception as e:
            print(f'Error initializing the server: {str(e)}')
            server.quit()
    
    #Funstion "send" sends notification to your mail
    def send(self, server, notification):
        message = f'Subject: {notification.get_subject()}\n\n{notification.get_body()}'
        server.sendmail(notification.get_sender_email(), notification.get_receiver_email(), message)

    # Function "sort_by_time" sorts notifications so the nearest notification will be the one that triggers first
    def sort_by_time(self):
        i = 0
        while i < len(self.notifications) - 1:
            if self.notifications[i].get_year() == self.notifications[i + 1].get_year():
                if self.notifications[i].get_month() == self.notifications[i + 1].get_month():
                    if self.notifications[i].get_day() == self.notifications[i + 1].get_day():
                        if self.notifications[i].get_hour() == self.notifications[i + 1].get_hour():
                            break
                        else:
                            if self.notifications[i].get_hour() > self.notifications[i + 1].get_hour():
                                temp = self.notifications[i]
                                self.notifications[i] = self.notifications[i + 1]
                                self.notifications[i + 1] = temp
                            else:
                                break
                    else:
                        if self.notifications[i].get_day() > self.notifications[i + 1].get_day():
                            temp = self.notifications[i]
                            self.notifications[i] = self.notifications[i + 1]
                            self.notifications[i + 1] = temp
                        else:
                            break
                else:
                    if self.notifications[i].get_month() > self.notifications[i + 1].get_month():
                        temp = self.notifications[i]
                        self.notifications[i] = self.notifications[i + 1]
                        self.notifications[i + 1] = temp
                    else:
                        break
            else:
                if self.notifications[i].get_year() > self.notifications[i + 1].get_year():
                    temp = self.notifications[i]
                    self.notifications[i] = self.notifications[i + 1]
                    self.notifications[i + 1] = temp
                else:
                    break

    def get_notification(self):
        return self.notifications[0]
    
    # Function "quit" ends server's session
    def quit(self, server):
        server.quit()
        #print('End of the session')
