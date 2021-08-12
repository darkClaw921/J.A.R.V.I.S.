
import datetime
import googleapiclient
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os


load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar']


calendarId = os.getenv("calendarID")
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")


class GoogleCalendar(object):
    textMessage = ""
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        self.service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)
    

    # вывод списка из десяти предстоящих событий
    def get_events_list(self):
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        
        events_result = self.service.events().list(calendarId=calendarId,
                                                   timeMin=now,
                                                   maxResults=10, 
                                                   singleEvents=True,
                                                   orderBy='startTime').execute()

        events = events_result.get('items', [])

        if not events:
            return self.textMessage + "Отдых"
        for event in events:
           
            # TODO: переделать по нормальному

            # из 2021-08-12T20:45:00+03:00 в ['20', '45', '00+03', '00']
            startEventTime = event["start"]["dateTime"].split("T")[1].split(':')
            startEventTime = f"{startEventTime[0]} : {startEventTime[1]}"

            endEventTime = event["end"]["dateTime"].split("T")[1].split(':')
            endEventTime = f"{endEventTime[0]} : {endEventTime[1]}"

            nameEvent = event["summary"]
            
            self.textMessage += f"   {nameEvent}:\n      c  {startEventTime}\n      до {endEventTime}\n\n"
        
        return self.textMessage    
