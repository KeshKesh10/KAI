"""
Google Calendar integration tool
Handles calendar events - add, list, update, delete
Requires Google Calendar API setup
"""

import os
import json
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.auth.oauthlib.flow import InstalledAppFlow
from google_auth_httplib2 import AuthorizedHttp
from googleapiclient.discovery import build
import httplib2

SCOPES = ['https://www.googleapis.com/auth/calendar']
TOKEN_FILE = 'data/google_token.json'
CREDENTIALS_FILE = 'data/credentials.json'

class CalendarTool:
    """Manages Google Calendar events"""
    
    def __init__(self):
        self.service = None
        self.calendar_id = 'primary'
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Calendar API"""
        creds = None
        
        # Load existing token
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        
        # Refresh or create new token
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Need credentials.json from Google Cloud Console
                if not os.path.exists(CREDENTIALS_FILE):
                    return False
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save token for next run
            os.makedirs('data', exist_ok=True)
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('calendar', 'v3', credentials=creds)
        return True
    
    def execute(self, args):
        """Execute calendar command"""
        if not self.service:
            return "❌ Google Calendar not configured. See /help for setup instructions."
        
        parts = args.strip().split(None, 2)
        
        if not parts:
            return "❌ Usage: /calendar <add|list|remove> [args]"
        
        action = parts[0].lower()
        params = parts[1] if len(parts) > 1 else ""
        extra = parts[2] if len(parts) > 2 else ""
        
        if action == "add":
            return self._add_event(params, extra)
        elif action == "list":
            return self._list_events(params)
        elif action == "remove":
            return self._remove_event(params)
        else:
            return f"❌ Unknown action: {action}\nUse: add, list, remove"
    
    def _add_event(self, title, description=""):
        """Add event to Google Calendar"""
        if not title:
            return "❌ Usage: /calendar add <title> [description]"
        
        try:
            event = {
                'summary': title,
                'description': description if description else '',
                'start': {
                    'dateTime': datetime.now().isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': (datetime.now() + timedelta(hours=1)).isoformat(),
                    'timeZone': 'UTC',
                },
            }
            
            result = self.service.events().insert(
                calendarId=self.calendar_id,
                body=event
            ).execute()
            
            return f"✅ Event added to Google Calendar: {title}"
        
        except Exception as e:
            return f"❌ Error adding event: {str(e)}"
    
    def _list_events(self, days="7"):
        """List upcoming events from Google Calendar"""
        try:
            num_days = int(days) if days else 7
        except ValueError:
            num_days = 7
        
        try:
            now = datetime.utcnow().isoformat() + 'Z'
            end = (datetime.utcnow() + timedelta(days=num_days)).isoformat() + 'Z'
            
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=now,
                timeMax=end,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            if not events:
                return f"📅 No events in the next {num_days} days"
            
            output = [f"📅 Events (Next {num_days} days):\n"]
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                summary = event.get('summary', 'Untitled')
                output.append(f"  • {summary} - {start}")
            
            return "\n".join(output)
        
        except Exception as e:
            return f"❌ Error listing events: {str(e)}"
    
    def _remove_event(self, event_title):
        """Remove event from Google Calendar"""
        if not event_title:
            return "❌ Usage: /calendar remove <event_title>"
        
        try:
            now = datetime.utcnow().isoformat() + 'Z'
            end = (datetime.utcnow() + timedelta(days=30)).isoformat() + 'Z'
            
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=now,
                timeMax=end,
                singleEvents=True,
                q=event_title
            ).execute()
            
            events = events_result.get('items', [])
            
            if not events:
                return f"❌ Event '{event_title}' not found"
            
            # Delete first matching event
            event_id = events[0]['id']
            self.service.events().delete(
                calendarId=self.calendar_id,
                eventId=event_id
            ).execute()
            
            return f"✅ Event deleted: {events[0].get('summary', 'Untitled')}"
        
        except Exception as e:
            return f"❌ Error removing event: {str(e)}"
