from django.apps import AppConfig
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os


class CoachingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coaching'

    def ready(self):

        SCOPES = ['https://www.googleapis.com/auth/meetings.space.created']
        creds = None

        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)

            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        self.creds = creds
