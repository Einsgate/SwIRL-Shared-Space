from allauth.socialaccount.models import SocialAccount,SocialToken
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from django.conf import settings
from datetime import datetime

#Connect to Google Calendar
def connect_to_calendar(request):
    #Fetches the User of the request
   # account = SocialAccount.objects.get(user = request.user)
    print(request.user)
   # print(account)
    #Fetches the Acces token of the User
    token = SocialToken.objects.get(account__user = request.user)
    print(token)
    #token = SocialToken.objects.filter(account__user__exact = request.user).values('token')

    #The scope of service like if we want readonly etc
    SCOPES = ['https://www.googleapis.com/auth/calendar.events']

    #Finally making a connection request
    creds = Credentials(token.token,SCOPES )
    service = build('calendar', 'v3', credentials = creds)
    return service

def create_event(service, reservation, team_members):
    # Get attendees
    attendees = []
    for team_member in team_members:
        attendee = {}
        attendee['email'] = team_member.user_id.email
        attendees.append(attendee)
    
    
    event = {
      'summary': reservation.title,
      'location': reservation.zone_name,
      'description': reservation.description,
      'start': {
        # Convert time format to ISO format with 'T'
        'dateTime': reservation.start_time.isoformat('T'),
        'timeZone': settings.TIME_ZONE,
      },
      'end': {
        # Convert time format to ISO format with 'T'
        'dateTime': reservation.end_time.isoformat('T'),
        'timeZone': settings.TIME_ZONE,
      },

      'attendees': attendees,
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 10},
        ],
      },
    }
    
    print('ok')
    print(reservation.start_time)
    print(reservation.end_time)
    
    event = service.events().insert(calendarId='primary', body=event, sendNotifications=True).execute()
    print('Event created: %s' % (event.get('htmlLink')))
    print('done')