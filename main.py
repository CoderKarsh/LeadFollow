import os
from dotenv import load_dotenv
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from twilio.rest import Client
from datetime import datetime

load_dotenv()

class Notifier:
    def __init__(self):
        self.telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        self.twilio_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        self.twilio_token = os.environ.get("TWILIO_AUTH_TOKEN")
        self.twilio_number = os.environ.get("TWILIO_WHATSAPP_NUMBER")
        
        if self.twilio_sid and self.twilio_token:
            self.twilio_client = Client(self.twilio_sid, self.twilio_token)
            
        self.waba_token = os.environ.get("WABA_ACCESS_TOKEN")
        self.waba_phone_id = os.environ.get("WABA_PHONE_NUMBER_ID")

    def send_telegram(self, chat_id, message):
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"❌ Telegram Error: {str(e)}")
            return False

    def send_twilio_whatsapp(self, phone_number, message):
        try:
            formatted_number = f"whatsapp:{phone_number}" if not str(phone_number).startswith("whatsapp:") else phone_number
            msg = self.twilio_client.messages.create(
                from_=self.twilio_number, body=message, to=formatted_number
            )
            return True
        except Exception as e:
            print(f"❌ Twilio Error: {str(e)}")
            return False

    def send_official_whatsapp(self, phone_number, message):
        print("Official WABA endpoint hit. Need production keys to send.")
        return False

def run_daily_nudge():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
    g_client = gspread.authorize(creds)
    sheet = g_client.open("Leads for Bot").sheet1

    records = sheet.get_all_records()
    today = datetime.now().strftime("%Y-%m-%d")
    notifier = Notifier()

    for i, row in enumerate(records, start=2):
        status = row.get("Status")
        follow_up_date = str(row.get("Follow-up Date"))
        org_name = str(row.get("Organization Name"))
        platform = str(row.get("Lead Platform")).lower()
        contact_id = str(row.get("Lead Contact ID"))
        lead_name = row.get("Lead Name")

        if status == "Pending" and follow_up_date == today:
            message_body = (
                f"Hi {lead_name}, this is an automated follow-up from the {org_name}. \n\n"
                f"We noticed your profile is still pending. Are you still looking to secure your spot "
                f"for the upcoming event? Let us know how we can help!"
            )
            success = False
            
            if platform == "telegram":
                success = notifier.send_telegram(contact_id, message_body)
            elif platform == "twilio":
                success = notifier.send_twilio_whatsapp(contact_id, message_body)
            elif platform == "waba":
                success = notifier.send_official_whatsapp(contact_id, message_body)
            
            if success:
                print(f"Nudge sent via {platform} to {lead_name}.")
                sheet.update_cell(i, 3, "Nudged") # Assumes Status is the 2nd column

if __name__ == "__main__":
    run_daily_nudge()