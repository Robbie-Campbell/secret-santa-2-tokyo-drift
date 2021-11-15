import smtplib, ssl
from email.mime.text import MIMEText
from random import choice


class Person:
    def __init__(self, email, name, do_not_send):
        self.email = email
        self.name = name
        self.do_not_send = do_not_send


def create_people_array():
    return [Person("robbielcampbell@hotmail.com", "Rab", ["Kelly"]), Person("jerseyjack.jr@gmail.com", "Jack", []),
            Person("lauren_eady@hotmail.co.uk", "Lauren", ["Tom"]),
            Person("kellybailey0711@gmail.com", "Kelly", ["Rab"]),
            Person("hannahlb215@gmail.com", "Hannah", ["Caleb"]), Person("james@castleb.org.uk", "James", []),
            Person("caleb.fortune@hotmail.co.uk", "Caleb", ["Hannah"]),
            Person("tjpeacocks@gmail.com", "Tom", ["Lauren"]), Person("up900637@myport.ac.uk", "Joe", [])]


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


# def send_emails():
#     for x, y in email_list:
#         msg = MIMEText(y, "html")
#         msg["Subject"] = "Secret Santa Test (THIS ISN'T THE REAL ONE)"
#         msg["From"] = sender
#         msg["To"] = ",".join(x)
#         s = smtplib.SMTP_SSL(host="smtp.gmail.com", port=465)
#         s.login(user=sender, password="JoeManEmpire1120")
#         s.sendmail(sender, x, msg.as_string())
#
#
# send_emails()
