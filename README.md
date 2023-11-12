# The Secret Santa Generator

A project that i keep returning to, this project sees the creation of emails for a list of users
for secret santa. The complexity comes from the ability to exclude certain people for each person (e.g. couples or people they have had before.)

# Using the program
The Program can be executed by running the main method in "main.py", but first some configuration:
- There is no GUI (yet, maybe one year) so the people list must be configured in a secrets.py file.
- The people list is a List[Person] with the first param being the email of the Present "Sender", the second being the Name of the present "Sender" and the final param being the names of other Persons in the list that are not suitable candidates for this present Sender.
- e.g. temp = [Person("Mark@email.com", "Mark", ["Jeff"])] would represent a person who's email is Mark@email.com, whos name is Mark and who should not receive "Jeff" present receiver.
- You must also configure a gmail account with an "App Password" that allows you to send emails, this can be added to the "secrets.py" file with under the variables: "sender" and "password"
- Note that the password is the App Password from Gmail not the gmail account password.

With all that configured, just press execute and it should work like a charm.