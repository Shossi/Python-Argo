"""
Frontend of the program, flask is run here.
backend functions are called.
"""

from flask import Flask, render_template, request, redirect, session, send_file, send_from_directory
from datetime import timedelta
from Modules.apicall import api_call, valid_input
from Modules.get_weekdays import get_weekdays
from Modules.translate_country import translate_country
from Modules.login import login
from Modules.signup import signup
import os
import boto3
from botocore import UNSIGNED
from botocore.client import Config
import json

# backend functions.
app = Flask(__name__)
app.config["SESSION_TYPE"] = 'filesystem'
app.permanent_session_lifetime = timedelta(seconds=150)
app.config['SECRET_KEY'] = "os.urandom(4)"
data = {}

SAVE_DIR = './data/history'
BG_COLOR = os.getenv('BG_COLOR', '#ffffff')  # default to white if not set


def save_search_query(location, data):
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    filename = os.path.join(SAVE_DIR, f"{location}.json")
    with open(filename, 'a') as file:
        file.write(json.dumps(data, indent=4) + "\n")


@app.route('/', methods=['GET', 'POST'])
def start():
    """
    route start, redirects to /login  unless session is active.
    :return: redirection to login or app page.
    """
    if not session.get("username"):
        return redirect('/login')
    else:
        return redirect('/home')


@app.route('/signup', methods=['GET', 'POST'])
def sign():
    """
    signup route
    :return: redirection to login or rendering signup again with errormsg.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if signup(username, password):
            return redirect('/login')
        else:
            return render_template('signup.html', error='user already exists')
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def log():
    """
    login route. session is created here upon checking the username.
    :return: redirection to app page when login is created, also inits session
    """
    if request.method == 'POST':  # if user input was recieved : aka location was input by the user in the app
        username = request.form['username']
        password = request.form['password']
        if login(username, password):
            session["username"] = username
            return redirect('/home')
        else:
            return render_template('login.html', not_valid='Username or Password incorrect')
    else:
        return render_template('login.html')


@app.route('/home', methods=['GET', 'POST'])  # Flask running starts here.
def main():
    if session.get("username"):
        if request.method == 'POST':  # if user input was recieved : aka location was input by the user in the app
            location = request.form['location']  # loads the input from the html to a var in python.
            if valid_input(location):  # checks the validation of the input
                global data
                data = api_call(location)  # apicall returns data or False if apicall wasnt successful.
                if data:  # if was successful
                    country = translate_country(data)  # use the data to get the country's name in english
                    save_search_query(country, data)  # Save the search query and data to a file
                    # country = location
                    day_list = get_weekdays(data)  # get a list of week days
                    # both are sent to the html and are used with jijna in the html file
                    return render_template('weather.html', data=data, day_list=day_list, country=country)
                else:  # if api call returns False sends a not_valid message to the user.
                    return render_template('weather.html', not_valid="City not found, Please try again")
            else:  # if the validation of the input returned False sends a not_valid message to the user.
                return render_template('weather.html', not_valid="input Invalid, Please try again.")
        else:
            return render_template('weather.html')  # if request method isn't post, render the html page normally.
    else:
        return redirect('/login')


@app.route('/logout', methods=['GET'])
def logoff():
    session.pop("username", default=None)
    return redirect('/login')


@app.route('/download')
def download_from_s3(bucket='yoskibucket'):
    client = boto3.client('s3', config=Config(signature_version=UNSIGNED), region_name="eu-west-3")
    list_files = client.list_objects(Bucket="yoskibucket")['Contents']

    for key in list_files:
        if key['Key'].endswith('.jpg'):
            filename = key['Key']
            local_filename = f'/home/bonji/app/data/{filename}'
            os.makedirs(os.path.dirname(local_filename), exist_ok=True)
            client.download_file(
                Bucket=bucket,
                Key=filename,
                Filename=local_filename
            )
            return send_file(local_filename, as_attachment=True)
    return redirect('/login')


@app.route('/save')
def save():
    dynamodb = boto3.resource('dynamodb', region_name="eu-west-3")
    table = dynamodb.Table('yossi_db')
    location = translate_country(data)
    for i, day in enumerate(data['days'][:7]):
        table.put_item(
            Item={
                "yossi": f"{location}_{day['datetime']}_{i}",
                "date": day['datetime'],
                "humidity": str(day["humidity"]),
                "morning_temp": str(day["tempmax"]),
                "evening_temp": str(day["tempmin"])
            }
        )
    return redirect("/home")

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(SAVE_DIR, filename, as_attachment=True)

@app.route('/downloads', methods=['GET'])
def list_files():
    if session.get("username"):
        files = os.listdir(SAVE_DIR)
        return render_template('downloads.html', files=files, bg_color=BG_COLOR)
    else:
        return redirect('/home')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)  # enables running from the ide
