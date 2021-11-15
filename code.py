import smtplib, ssl
from email.mime.text import MIMEText
from random import choice


class Person:
    def __init__(self, email, name, do_not_send):
        self.email = email
        self.name = name
        self.do_not_send = do_not_send


def create_people_array():
    return []


def get_random_person_from_list(arr):
    return choice(arr)


def check_if_compatible(santa, receiver, used):
    return santa.name != receiver.name and receiver.name not in santa.do_not_send and receiver.name not in used


def check_person_is_valid_for_santa(person, arr, used_people, count=0):
    while True:
        receiver = get_random_person_from_list(arr)
        if check_if_compatible(person, receiver, used_people):
            return receiver.name
        elif len(used_people) == len(arr) or count == len(arr) + 20:
            return False
        return check_person_is_valid_for_santa(person, arr, used_people, count+1)


def get_valid_email_list():
    used_people = []
    people_arr = create_people_array()
    size_arr = len(people_arr)
    email_list = dict()
    while True:
        person = get_random_person_from_list(people_arr)
        person_if_valid = check_person_is_valid_for_santa(person, people_arr, used_people)
        email_list[person.email] = person_if_valid
        used_people.append(person_if_valid)
        if False in email_list.values():
            return get_valid_email_list()
        if len(email_list.values()) == size_arr:
            break
    return email_list


print(get_valid_email_list())