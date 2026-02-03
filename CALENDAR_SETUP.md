# Google Calendar Setup for KAI

## Quick Setup (5 minutes)

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"Create Project"** or select existing project
3. Name it "KAI Assistant" (or anything you want)
4. Click **Create**

### Step 2: Enable Google Calendar API

1. In the Google Cloud Console, go to **APIs & Services** > **Library**
2. Search for **"Google Calendar API"**
3. Click on it and press **Enable**

### Step 3: Create OAuth Credentials

1. Go to **APIs & Services** > **Credentials**
2. Click **"+ CREATE CREDENTIALS"** > **OAuth client ID**
3. If prompted, configure the OAuth consent screen:
   - User Type: **External**
   - App name: **KAI Assistant**
   - User support email: **Your email**
   - Developer contact: **Your email**
   - Click **Save and Continue** through the scopes (leave default)
   - Add yourself as a test user
   - Click **Save and Continue**

4. Create OAuth Client ID:
   - Application type: **Desktop app**
   - Name: **KAI Desktop Client**
   - Click **Create**

5. **Download** the credentials JSON file
6. Rename it to `credentials.json`
7. Move it to: `/Users/rakesholanda/Downloads/KAI/data/credentials.json`

### Step 4: Test the Connection

```bash
cd /Users/rakesholanda/Downloads/KAI
python3 main.py
```

Then type:
```
what's my schedule
```

or
```
show my calendar
```

The first time, a browser window will open asking you to:
1. Sign in to your Google account
2. Grant KAI access to your calendar
3. Click **Allow**

After that, KAI can access your calendar anytime!

## What You Can Ask

Once connected:

```
what's my schedule
show my calendar
what's upcoming
schedule a meeting tomorrow at 2pm
add dentist appointment on Friday
remove that meeting
list my events
```

All work conversationally - no `/` commands needed!

## Files Created

After setup, you'll have:
- `data/credentials.json` - Your OAuth credentials (keep private!)
- `data/google_token.json` - Access token (auto-generated)

## Troubleshooting

### "Calendar feature requires Google Calendar setup"
- Make sure `data/credentials.json` exists
- Run KAI and try "show my calendar" - it will prompt for authorization

### "Module not found: google"
```bash
pip3 install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Browser doesn't open for authorization
- Check that port 8080 is available
- Try running from a terminal with browser access

### "Access denied" error
- Make sure you added yourself as a test user in OAuth consent screen
- Try removing `data/google_token.json` and re-authorizing

## Privacy & Security

- ✅ Credentials stored locally on your machine
- ✅ OAuth token expires and refreshes automatically
- ✅ Only accesses your calendar (no other Google services)
- ✅ You can revoke access anytime from [Google Account Settings](https://myaccount.google.com/permissions)

## Disconnect Calendar

To disconnect:
```bash
rm data/google_token.json
rm data/credentials.json
```

Or revoke access from your [Google Account](https://myaccount.google.com/permissions).
