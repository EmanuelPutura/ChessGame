import random
import smtplib
import ssl

import credentials.credentials
from tools.constants import UserAccountConstants


class EmailSender:
    def __init__(self):
        self.__code = random.randint(UserAccountConstants.VERIFICATION_CODE_LOW.value, UserAccountConstants.VERIFICATION_CODE_HIGH.value)
        self.__sender = UserAccountConstants.EMAIL_SENDER.value

    @property
    def code(self):
        return self.__code

    def send(self, username, email_receiver):
        password = credentials.credentials.password
        message = UserAccountConstants.CONFIRMATION_MESSAGE.value + username + "! Your account verification code is: " + str(self.__code)
        port = 465  # for SSL
        smtp_server = "smtp.gmail.com"

        # create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(self.__sender, password)
            server.sendmail(self.__sender, email_receiver, message)
