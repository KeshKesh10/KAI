#!/usr/bin/env python3
"""
Google Calendar Setup Helper
Guides you through connecting KAI to your Google Calendar
"""

import os
import sys

CREDENTIALS_FILE = "data/credentials.json"

print("\n" + "=" * 70)
print("KAI - Google Calendar Setup")
print("=" * 70 + "\n")

# Check if credentials exist
if os.path.exists(CREDENTIALS_FILE):
    print("✅ credentials.json found!")
    print(f"   Location: {CREDENTIALS_FILE}\n")
    
    # Try to connect
    print("Testing connection to Google Calendar...\n")
    
    try:
        from kai.tools.calendar_tool import CalendarTool
        
        calendar = CalendarTool()
        
        if calendar.service:
            print("✅ Successfully connected to Google Calendar!")
            print("\nYou can now use calendar features in KAI:")
            print("  - 'what's my schedule'")
            print("  - 'show my calendar'")
            print("  - 'schedule a meeting tomorrow at 2pm'\n")
        else:
            print("⚠️  Calendar service not initialized.")
            print("   Try running KAI and asking about your schedule.")
            print("   A browser window will open for authorization.\n")
    
    except Exception as e:
        print(f"❌ Error: {e}\n")
        print("Make sure you've installed the dependencies:")
        print("  pip3 install google-auth-oauthlib google-auth-httplib2 google-api-python-client\n")

else:
    print("❌ credentials.json not found!")
    print(f"   Expected location: {CREDENTIALS_FILE}\n")
    
    print("📋 Setup Steps:\n")
    print("1. Go to: https://console.cloud.google.com/")
    print("2. Create a new project (or select existing)")
    print("3. Enable Google Calendar API")
    print("4. Create OAuth 2.0 credentials (Desktop app)")
    print("5. Download the JSON file")
    print("6. Save it as: data/credentials.json")
    print("\nSee CALENDAR_SETUP.md for detailed instructions!\n")
    
    # Offer to open the setup guide
    response = input("Would you like to open the setup guide? (y/n): ")
    if response.lower() == 'y':
        os.system("open CALENDAR_SETUP.md" if sys.platform == "darwin" else 
                  "xdg-open CALENDAR_SETUP.md" if sys.platform == "linux" else
                  "start CALENDAR_SETUP.md")

print("=" * 70)
