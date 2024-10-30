import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def send_email(to_email, subject, message_content):
    MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
    MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN", "sandboxb1b17b26ad8e49c293594054bbf495ac.mailgun.org")
    
    # Check if Mailgun API key is set
    if not MAILGUN_API_KEY:
        print("Mailgun API key is missing. Please set it in the environment variables.")
        return
    
    # Mailgun API URL
    mailgun_url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"
    
    # Send the email using the Mailgun API
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
    
    # Log the response details
    if response.status_code == 200:
        print(f"Email sent successfully to {to_email}.")
    else:
        print(f"Failed to send email. Status Code: {response.status_code}")
        print("Response JSON:", response.json())

    return response  # Return the response for further inspection if needed
