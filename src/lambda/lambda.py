import boto3
import datetime
import json
import os
import sys

# Ensure requests is available in the Lambda environment
try:
    import requests
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--target", "/tmp/requests", "requests"])
    sys.path.append("/tmp/requests")
    import requests

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('yossi_db')
key = "L6W5ECZ2JFH2UVSHEZTXFTKZB"


def lambda_handler(event, context):
    weather_data = get_weather_data("Tel Aviv")
    save_to_dynamodb(weather_data)
    return {
        'statusCode': 200,
        'body': 'Backup completed successfully.'
    }


def get_weather_data(location):
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?key={key}&unitGroup=metric&numDays=7"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving weather data: {e}")
        return None


def save_to_dynamodb(weather_data):
    if weather_data:
        for i, day in enumerate(weather_data['days'][:7]):
            table.put_item(
                Item={
                    "yossi": f"Tel Aviv_{day['datetime']}_{i}",
                    "date": day['datetime'],
                    "humidity": str(day["humidity"]),
                    "morning_temp": str(day["tempmax"]),
                    "evening_temp": str(day["tempmin"])
                }
            )
