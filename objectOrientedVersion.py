import os
import sys

import smtplib
import ssl
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import choice
from secrets import people_one, sender, password
from person import Person
from typing import List, Union

sys.setrecursionlimit(2000)


class Generator:
    """
    Class which generates a list of candidates to send Secret Santa emails to.
    """
    def __init__(self) -> None:
        self.people_array: List[Person] = people_one
        self.used_people = []
        self.decided_santa_list = dict()
        self.sender: str = sender
        self.email_list = self.get_valid_email_list()

    def get_valid_email_list(self) -> dict:
        """
        Recursively gets a valid email list from the given people list.
        :return: A valid email list from the given people list.
        """
        while True:
            self.add_santa_present_receiver_to_email_list()
            if False in self.decided_santa_list.values():
                try:
                    self.decided_santa_list.clear()
                    return self.get_valid_email_list()
                except RecursionError:
                    raise (f"Couldn't find a solution, please try again! (it is possible your list has a solution," +
                           f" but i was not able to find it in {sys.getrecursionlimit()} tries)")
            if len(self.decided_santa_list.values()) == len(self.people_array):
                return self.decided_santa_list

    def add_santa_present_receiver_to_email_list(self) -> None:
        """
        Adds a present receiver to the email list.
        """
        santa = self.get_random_person_from_list()
        self.append_to_email_list(santa, self.check_person_is_valid_as_santa(santa))

    def check_person_is_valid_as_santa(self, person: Person, count: int = 0) -> Union[str, bool]:
        """
        Recursive method which checks if a given "Present Receiver" is a valid candidate to be Secret Santa of
        the given person, if not, recurse and try again.
        :param person: The Person to generate a secret Santa for.
        :param count: The number of iterations of the recursive check.
        :return: Either a valid person for the Secret Santa list or a "False" flag (which later indicates the list is
        invalid).
        """
        while True:
            present_receiver = self.get_random_person_from_list()
            if self.check_if_compatible(person, present_receiver):
                return present_receiver.name
            elif count >= len(self.people_array) + 20:
                self.used_people.clear()
                return False
            return self.check_person_is_valid_as_santa(person, count + 1)

    def check_if_compatible(self, santa: Person, present_receiver: Person) -> bool:
        """
        Checks if a given Person is a valid candidate as a Secret Santa (if they are not both the santa and receiver,
        the Santa is not in the do not send list of the Receiver and they have not already been used).
        :param santa: The person who would be Santa.
        :param present_receiver: The Person who would receive the Present.
        :return: Whether a given Person is a valid candidate as a Secret Santa.
        """
        return santa.name != present_receiver.name and present_receiver.name not in \
            santa.do_not_send and present_receiver.name not in self.used_people

    def append_to_email_list(self, santa: Person, present_receiver_name: str) -> None:
        """
        Appends a person to the decided Santa List (as a key of the email and the value of the name of the present
        receiver)
        :param santa: The Sender of the present.
        :param present_receiver_name: The receiver of the present.
        """
        self.decided_santa_list[santa.email] = present_receiver_name
        self.used_people.append(present_receiver_name)

    def get_random_person_from_list(self) -> Person:
        """
        Gets a random Person from the people List.
        :return: A random person from the people list.
        """
        return choice(self.people_array)

    def send_fancy_emails(self) -> None:
        """
        Sends all of the emails to the present_receivers.
        """
        for santa in self.email_list:
            self.send_email_single(santa)

    def send_email_single(self, santa) -> None:
        """
        Sends a single Secret Santa email.
        :param santa: The Santa who is sending the email.
        """
        message = self.construct_message(santa)
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp.gmail.com", 25) as s:
            s.connect('smtp.gmail.com', 587)
            s.ehlo()
            s.starttls(context=context)
            s.ehlo()
            s.login(user=self.sender, password=password)
            s.sendmail(self.sender, santa, message.as_string())
            print("sent", santa)

    def construct_message(self, santa: str) -> MIMEMultipart:
        """
        Constructs a nice looking email to send to the Secret Santa.
        :param santa: The email of the Person who will be sending the Secret Santa present.
        :return: A nice looking email to send to the Secret Santa.
        """
        message = MIMEMultipart('related')
        message['Subject'] = "HO HO HO It's Santa!"
        message_alt = MIMEMultipart('Secret Santa Email')
        base_dir = os.path.dirname(os.path.abspath(__file__))
        message.attach(message_alt)

        image = open(base_dir + "\\santa.jpg", "rb")
        santa_clause = MIMEImage(image.read())
        image.close()
        santa_clause.add_header("Content-ID", "<santa>")
        message_text = MIMEText(f"<h1>It's Christmas time!</h1><br><p>It's time to celebrate christmas "
                                f"and i'm your secret santa! Don't tell anyone, but you have <h1>{self.email_list[present_receiver]}</h1> as "
                                f"your present receiver, good luck and have a <b>Merry Christmas!</b><br>"
                                f"<img src='cid:santa'>!", 'html')
        message_alt.attach(message_text)
        message['From'] = self.sender
        message['To'] = santa
        message.attach(santa_clause)
        return message


if __name__ == "__main__":
    generator = Generator()
    generator.send_fancy_emails()
