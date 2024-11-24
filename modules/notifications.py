import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Function to send email notifications using Mailgun
def send_email(to_email, subject, message_content):
    MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
    MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN", "sandboxb1b17b26ad8e49c293594054bbf495ac.mailgun.org")
    
    if not MAILGUN_API_KEY:
        print("Mailgun API key is missing. Please set it in the environment variables.")
        return

    # Mailgun API URL
    mailgun_url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"

    # Send the email
    response = requests.post(
        mailgun_url,
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": f"Air Quality Monitoring <mailgun@{MAILGUN_DOMAIN}>",
            "to": to_email,
            "subject": subject,
            "text": message_content
        }
    )

    # Log the response
    if response.status_code == 200:
        print(f"Email sent successfully to {to_email}.")
    else:
        print(f"Failed to send email. Status Code: {response.status_code}")
        print("Response JSON:", response.json())

    return response

# Function to send WhatsApp notifications using CallMeBot
def send_whatsapp(phone_number, message):
    CALLMEBOT_API_KEY = os.getenv("CALLMEBOT_API_KEY")
    
    if not CALLMEBOT_API_KEY:
        print("CallMeBot API key is missing. Please set it in the environment variables.")
        return

    # CallMeBot API URL
    url = f"https://api.callmebot.com/whatsapp.php"
    params = {
        "phone": phone_number,
        "text": message,
        "apikey": CALLMEBOT_API_KEY
    }

    # Send the WhatsApp message
    response = requests.get(url, params=params)

    # Log the response
    if response.status_code == 200:
        print(f"WhatsApp message sent successfully to {phone_number}.")
    else:
        print(f"Failed to send WhatsApp message. Status Code: {response.status_code}")
        print("Response Text:", response.text)

    return response
