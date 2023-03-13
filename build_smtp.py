import smtplib
from notification import *
from _datetime import datetime
import time
import getpass


class Server:
    def __init__(self):
        self.notifications = []

    def main_loop(self):
        #print('Hello! Would you like to add notification?')
        #print('You can use Y for yes and N for No')
        self.add_notification('remindersfrompy@gmail.com', 'Test Email', 'With Class', year=2023, month=3, day=13, hour=14)
        self.add_notification('remindersfrompy@gmail.com', 'Test Email', 'With Class', year=2023, month=3, day=13, hour=14)
        self.sort_by_time()
        print(self.notifications[0].print_not())
        print(self.notifications[1].print_not())

        while len(self.notifications) != 0:
            now = datetime.now()
            if self.notifications[0].get_year() == now.year:
                if self.notifications[0].get_month() == now.month:
                    if self.notifications[0].get_day() == now.day:
                        if self.notifications[0].get_hour() == now.hour:
                            self._init_serv(self.notifications[0])
                            del self.notifications[0]
            print(f'{now.hour}')
            time.sleep(5)

    # Function "add_notification" creates a Notification object and append this object to the 'self.notifications' list
    def add_notification(self, receiver_email, subject, body, year, month, day, hour):
        note = Notification(receiver_email, subject, body, year, month, day, hour)
        self.notifications.append(note)

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
            print(f'Error: {str(e)}')
            server.quit()

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

    def quit(self, server):
        server.quit()
        print('End of the session')
