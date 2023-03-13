from build_smtp import *


if __name__ == "__main__":
    email = Server()

    email.main_loop()
    #email.add_notification( 'remindersfrompy@gmail.com', 'smtp-mail.outlook.com',
                            #'Test Email', 'With Class')
    #email.init_serv(email.get_notification())
    #email.send('Test Email', 'With Class')