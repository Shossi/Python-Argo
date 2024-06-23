import json


def login(username, password):
    """

    :param username: username sent from html login form
    :param password: password sent from html login form
    :return: returns true or false, depending on wether username is present in db.
    """
    with open('test.json', 'r') as file:
        db = json.load(file)
    if username in db:
        return db[username] == password
    else:
        return False
