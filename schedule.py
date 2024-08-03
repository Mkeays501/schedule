from bs4 import BeautifulSoup
import requests
from googleapiclient.discovery import build
from google.auth import service_account
from dotenv import load_dotenv

load_dotenv()

# Step 1: Log in and fetch the work schedule
login_url = 'https://payroll.payworks.ca/loginscreen.asp?LangID=0'
schedule_url = 'https://payroll.payworks.ca/tom/ess/TimeOffCalendar.aspx?MenuID=348'
credentials = {'customerid': 'E90086', 'username': '1604', 'password': 'Jym4x8nv!#'}

with requests.Session() as session:
    session.post(login_url, data=credentials)
    response = session.get(schedule_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Parse your schedule from the HTML content here
    schedule = parse_schedule(soup)

# Step 2: Add to Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = '/home/mrkeays/Downloads/service_account_file.json'  # Replace with your correct file path

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)

def add_event_to_calendar(event):
    event = {
        'summary': event['title'],
        'start': {'dateTime': event['start'], 'timeZone': 'UTC'},
        'end': {'dateTime': event['end'], 'timeZone': 'UTC'}
    }
    service.events().insert(calendarId='primary', body=event).execute()

def parse_schedule(soup):
    events = [{"_id":"payyy","startUrl":["https://payroll.payworks.ca/tom/ess/TimeOffCalendar.aspx?MenuID=348"],"selectors":[{"id":"when am i off","linkType":"linkFromAttributes","multiple":false,"parentSelectors":["_root"],"selector":"html","type":"SelectorLink"}],"websiteStateSetup":{"enabled":true,"performWhenNotFoundSelector":"input#PayRollNum","actions":[{"selector":"input#PayRollNum","type":"textInput","value":"E90086"},{"selector":"input#UserName","type":"textInput","value":"1604"},{"selector":"input#Password","type":"passwordInput","value":"Jym4x8nv!#"},{"selector":"a[data-ga='tile-employee schedule']","type":"click"},{"selector":".context-bar-content li:nth-of-type(5) a","type":"click"}]}}]
    # Implement your HTML parsing logic here to extract the schedule events
    # For each event, create a dictionary with 'title', 'start', and 'end' keys
    # Append the dictionary to the 'events' list
    return events
{"_id":"payyy","startUrl":["https://payroll.payworks.ca/tom/ess/TimeOffCalendar.aspx?MenuID=348"],"selectors":[{"id":"when am i off","linkType":"linkFromAttributes","multiple":false,"parentSelectors":["_root"],"selector":"html","type":"SelectorLink"}],"websiteStateSetup":{"enabled":true,"performWhenNotFoundSelector":"input#PayRollNum","actions":[{"selector":"input#PayRollNum","type":"textInput","value":"E90086"},{"selector":"input#UserName","type":"textInput","value":"1604"},{"selector":"input#Password","type":"passwordInput","value":"Jym4x8nv!#"},{"selector":"a[data-ga='tile-employee schedule']","type":"click"},{"selector":".context-bar-content li:nth-of-type(5) a","type":"click"}]}}

for event in schedule:
    add_event_to_calendar(event)
