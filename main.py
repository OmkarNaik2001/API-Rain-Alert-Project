import requests
from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

api_key = os.getenv("API_KEY")
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone = os.getenv("TWILIO_PHONE_NUMBER")
to_phone = os.getenv("TO_PHONE_NUMBER")

parameters = {
    "lat": 19.075983,
    "lon": 72.877655,
    "appid": api_key,
    "cnt": 4,
}
will_rain = False
response = requests.get("https://api.openweathermap.org/data/2.5/forecast", params=parameters)
response.raise_for_status()
weather_data = response.json()

for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="It's going to rain, please carry an umbrella ☔",
        from_=twilio_phone,
        to=to_phone,
    )

    print(message.status)
