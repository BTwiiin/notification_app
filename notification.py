class Notification:

    #CONSTRUCTOR
    def __init__(self, receiver_email, subject, body, year, month, day, hour):
        self.sender_email = 'remindersfrompy@outlook.com'
        self.sender_password = 'Milana2412'
        self.receiver_email = receiver_email
        self.server_host = 'smtp-mail.outlook.com'
        self.subject = subject
        self.body = body
        self.notif_year = year
        self.notif_month = month
        self.notif_day = day
        self.notif_hour = hour

    def print_not(self):
        print(f'Receiver Email: {self.receiver_email}')
        print(f'Subject: {self.subject}')
        print(f'Body: {self.body}')
        print(f'Year: {self.notif_year}')
        print(f'Month: {self.notif_month}')
        print(f'Day: {self.notif_day}')
        print(f'Hour: {self.notif_hour}')

    #GETTERS
    def get_sender_email(self):
        return self.sender_email

    def get_sender_password(self):
        return self.sender_password

    def get_receiver_email(self):
        return self.receiver_email

    def get_server_host(self):
        return self.server_host

    def get_subject(self):
        return self.subject

    def get_body(self):
        return self.body

    def get_hour(self):
        return self.notif_hour

    def get_year(self):
        return self.notif_year

    def get_month(self):
        return self.notif_month

    def get_day(self):
        return self.notif_day
