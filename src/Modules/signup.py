import json


def signup(username, password):
    """
    function to add a new user to the db.
    :param username: username sent from html signup form
    :param password: password sent from html signup form
    :return: returns True if user wasn't already signed up and False if otherwise/
    """
    with open('test.json', 'r+') as file:
        db = json.load(file)
        if username in db:
            return False
        else:
            db[username] = password
            file.seek(0)
            json.dump(db, file, indent=4)
            file.truncate()
            return True
