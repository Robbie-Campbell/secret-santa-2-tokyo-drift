from typing import List


class Person:
    """
    Class Representing a "Person", with their name, email address and a list of other "Persons" that they should not get
    as a Secret Santa.
    """
    def __init__(self, email: str, name: str, do_not_send: List[str]):
        self.email: str = email
        self.name: str = name
        self.do_not_send: List[str] = do_not_send
