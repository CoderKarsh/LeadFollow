# LeadFollow

An automated lead follow-up notification system that sends personalized nudges to pending leads via multiple communication channels.

## Overview

LeadFollow integrates with Google Sheets to manage leads and automatically sends follow-up messages through Telegram, WhatsApp (via Twilio), or WhatsApp Business API (WABA) based on scheduled follow-up dates. Perfect for sales teams, event organizers, and business development teams that need to maintain consistent contact with leads.

## Features

- 📊 **Google Sheets Integration** - Manage leads directly from a Google Sheets spreadsheet
- 💬 **Multi-Channel Support** - Send notifications via:
  - Telegram
  - WhatsApp (Twilio)
  - WhatsApp Business API (WABA)
- ⏰ **Scheduled Follow-ups** - Automatic nudges on specified follow-up dates
- 📝 **Personalized Messages** - Customizable message templates with lead information
- ✅ **Status Tracking** - Automatically update lead status to "Nudged" after sending

## Requirements

- Python 3.7+
- Google Sheets API credentials (service account JSON)
- API tokens for notification services:
  - Telegram Bot Token
  - Twilio Account SID and Auth Token
  - WhatsApp Business API Access Token (optional)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/CoderKarsh/LeadFollow.git
cd LeadFollow
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in a `.env` file:
```env
TELEGRAM_BOT_TOKEN=your_telegram_token
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+1234567890
WABA_ACCESS_TOKEN=your_waba_token
WABA_PHONE_NUMBER_ID=your_waba_phone_id
```

4. Add your Google Sheets service account credentials:
   - Download your service account JSON key from Google Cloud Console
   - Save it as `service_account.json` in the project root

## Google Sheets Setup

Create a Google Sheet named **"Leads for Bot"** with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| Lead Name | Text | Name of the lead |
| Organization Name | Text | Organization the lead belongs to |
| Lead Contact ID | Text | Telegram Chat ID, WhatsApp number, or WABA ID |
| Lead Platform | Text | Communication platform (telegram, twilio, waba) |
| Follow-up Date | Date | Date for the follow-up (YYYY-MM-DD format) |
| Status | Text | Current status (Pending, Nudged, etc.) |

## Usage

Run the daily nudge script:
```bash
python main.py
```

### How It Works

1. Connects to your "Leads for Bot" Google Sheet
2. Reads all lead records
3. For each lead with:
   - Status = "Pending"
   - Follow-up Date = Today's date
4. Sends a personalized follow-up message via the specified platform
5. Updates the Status to "Nudged"

### Scheduling

To run this script daily, set up a cron job (Linux/Mac):
```bash
0 9 * * * cd /path/to/LeadFollow && python main.py
```

Or use Windows Task Scheduler for Windows systems.

## Project Structure

```
LeadFollow/
├── main.py              # Main application script
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create locally)
├── service_account.json # Google Sheets credentials (create locally)
└── README.md           # This file
```

## Dependencies

- **gspread** - Google Sheets API client
- **oauth2client** - OAuth2 authentication for Google Services
- **requests** - HTTP library for Telegram API
- **twilio** - WhatsApp and SMS messaging service
- **python-dotenv** - Environment variable management

## Configuration

### Telegram
1. Create a bot with BotFather on Telegram
2. Get your bot token and add to `.env`
3. Use Telegram Chat IDs as contact identifiers

### Twilio WhatsApp
1. Set up a Twilio account and WhatsApp sandbox
2. Add your Account SID, Auth Token, and WhatsApp number to `.env`
3. Use WhatsApp phone numbers (with +country code) as contact identifiers

### WhatsApp Business API (WABA)
1. Set up WhatsApp Business API through Meta
2. Add your access token and phone number ID to `.env`
3. Note: Production functionality requires full WABA setup

## Error Handling

- The application gracefully handles errors for each notification attempt
- Failed sends print error messages but continue processing other leads
- Individual platform failures don't affect other platforms

## Security Notes

⚠️ **Important:**
- Never commit `.env` or `service_account.json` files to version control
- Use `.gitignore` to exclude sensitive files (already included)
- Rotate API tokens regularly
- Use environment variables for all credentials

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## Support

For issues, questions, or feature requests, please open an issue on the GitHub repository.

---

**Built with ❤️ by [CoderKarsh](https://github.com/CoderKarsh)**
