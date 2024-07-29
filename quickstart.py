import datetime
import os.path
import requests

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

# Initialize Google Calendar service
def initialize_google_calendar():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                ".credentials/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("calendar", "v3", credentials=creds)


# Function to get upcoming events from Google Calendar
def get_upcoming_events(service):
    try:
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        print("Getting the upcoming 10 events")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
        else:
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                print(start, event["summary"])

    except HttpError as error:
        print(f"An error occurred: {error}")

# Function to create a new event in Google Calendar
def create_event(service, summary, location, description, start_datetime, end_datetime):
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_datetime,
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_datetime,
            'timeZone': 'UTC',
        },
    }

    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created successfully!')
        print('Event Link: %s' % (event.get('htmlLink')))

    except HttpError as error:
        print(f'An error occurred: {error}')

