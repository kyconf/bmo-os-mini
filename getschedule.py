
import os.path
import voice
import datetime
from dotenv import load_dotenv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


load_dotenv()
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

# taken from quickstart.py of google calendar documentation 
def main():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
    

    work_events = os.getenv("CALENDAR_ID")
    events_result = (
        service.events()
        .list(
            calendarId=work_events,
            timeMin=now,
            maxResults=3,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    
    events = events_result.get("items", [])

    response_if_today(events)
    if not events:
      print("No upcoming events found.")
      return

    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      print(start, event["summary"])
    

  except HttpError as error:
    print(f"An error occurred: {error}")



def response_if_today(events):
    if not events:
        voice.test_bmo_laptop("You have no events today!", "en_US-lessac-medium.onnx")
        return

    # UTC => toronto time 
    today_now = (datetime.datetime.utcnow() - datetime.timedelta(hours=4)).date()

    # Grab the first upcoming event
    event = events[0]
    start_raw = event['start'].get('dateTime')
    
    if not start_raw:
        print("All day event found, skipping.")
        return

    start_utc = datetime.datetime.strptime(start_raw[:-1], "%Y-%m-%dT%H:%M:%S")
    start_local = start_utc - datetime.timedelta(hours=4)
    event_date = start_local.date()

    if event_date == today_now:
        end_raw = event['end'].get('dateTime')
        end_utc = datetime.datetime.strptime(end_raw[:-1], "%Y-%m-%dT%H:%M:%S")
        end_local = end_utc - datetime.timedelta(hours=4)

        start_str = start_local.strftime("%I:%M %p").lstrip('0')

        
        end_str = end_local.strftime("%I:%M %p").lstrip('0')
        summary = event.get('summary', 'Work')

        voice_str = f"Yep! Today you are a {summary} from {start_str} to {end_str}!"
        voice.test_bmo_laptop(voice_str, "en_US-lessac-medium.onnx")
    else:
       
        day_name = start_local.strftime("%A")
        voice.test_bmo_laptop(f"                No shifts today! But you are a cashier on {day_name}!", "en_US-lessac-medium.onnx")

if __name__ == "__main__":
  main()