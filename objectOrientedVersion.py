import os
import sys

import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import choice

sys.setrecursionlimit(5000)


class Person:
    def __init__(self, email, name, do_not_send):
        self.email = email
        self.name = name
        self.do_not_send = do_not_send


class Generator:
    def __init__(self):
        self.people_array = [Person("#######", "#######", ["#######"]),
                             Person("#######", "#######", []),
                             Person("#######", "#######", ["#######"]),
                             Person("#######", "#######", ["#######"]),
                             Person("#######", "#######", []),
                             Person("#######", "#######", []),
                             Person("#######", "#######", ["#######"]),
                             Person("#######", "#######", [])]
        self.used_people = []
        self.decided_santa_list = dict()
        self.sender = "#######@gmail.com"
        self.email_list = self.get_valid_email_list()

    def check_person_is_valid_for_santa(self, santa, count=0):
        while True:
            present_receiver = self.get_random_person_from_list()
            if self.check_if_compatible(santa, present_receiver):
                return present_receiver.name
            elif count >= len(self.people_array) + 20:
                self.used_people.clear()
                return False
            return self.check_person_is_valid_for_santa(santa, count + 1)

    def check_if_compatible(self, santa, present_receiver):
        return santa.name != present_receiver.name and present_receiver.name not in \
               santa.do_not_send and present_receiver.name not in self.used_people

    def get_valid_email_list(self):
        while True:
            self.add_santa_present_receiver_to_email_list()
            if False in self.decided_santa_list.values():
                self.decided_santa_list.clear()
                return self.get_valid_email_list()
            if len(self.decided_santa_list.values()) == len(self.people_array):
                return self.decided_santa_list

    def add_santa_present_receiver_to_email_list(self):
        santa = self.get_random_person_from_list()
        self.append_to_email_list(santa, self.check_person_is_valid_for_santa(santa))

    def append_to_email_list(self, santa, present_receiver):
        self.decided_santa_list[santa.email] = present_receiver
        self.used_people.append(present_receiver)

    def get_random_person_from_list(self):
        return choice(self.people_array)

    def send_fancy_emails(self):
        for santa in self.email_list:
            self.send_email_single(santa)

    def send_email_single(self, santa):
        message = self.construct_message(santa)
        s = smtplib.SMTP_SSL(host="smtp.gmail.com", port=465)
        s.login(user=self.sender, password="#######")
        s.sendmail(self.sender, santa, message.as_string())

    def construct_message(self, santa):
        message = MIMEMultipart('related')
        message['Subject'] = "HO HO HO It's Santa!"
        message_alt = MIMEMultipart('Secret Santa Email')
        base_dir = os.path.dirname(os.path.abspath(__file__))
        message.attach(message_alt)

        image = open(base_dir + "\\santa.jpg", "rb")
        santa_clause = MIMEImage(image.read())
        image.close()
        santa_clause.add_header("Content-ID", "<santa>")
        message_text = MIMEText("<h1>It's Christmas time!</h1><br><p>It's time to celebrate christmas "
                                "and i'm your secret santa! Don't tell anyone, but you have <h1>{}</h1> as "
                                "your present receiver, good luck and have a <b>Merry Christmas!</b><br>"
                                "<img src='cid:santa'>!".format(self.email_list[santa]), 'html')
        message_alt.attach(message_text)
        message['From'] = self.sender
        message['To'] = santa
        message.attach(santa_clause)
        return message


Generator().send_fancy_emails()
