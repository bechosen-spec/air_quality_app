from vonage import Auth, Vonage
from vonage_sms import SmsMessage, SmsResponse

def send_sms(to, message):
    """
    Sends an SMS message to the specified phone number.

    Args:
        to (str): Recipient's phone number in international format.
        message (str): Message to send.

    Returns:
        None
    """
    # Initialize the Vonage client with API credentials
    auth = Auth(api_key="3f376703", api_secret="wPRPFLn0tj1uSWsH")
    client = Vonage(auth)
    
    try:
        # Create the SMS message
        sms_message = SmsMessage(
            to=to,
            from_="Air Quality App",
            text=message,
        )

        # Send the SMS
        response: SmsResponse = client.sms.send(sms_message)

        # Handle the response
        if response["messages"][0]["status"] == "0":
            print("Message sent successfully.")
        else:
            print(f"Message failed with error: {response['messages'][0]['error-text']}")
    except Exception as e:
        print(f"Error sending SMS: {e}")

# Example usage
if __name__ == "__main__":
    recipient_number = "+2348105994390"  # Replace with actual recipient number
    text_message = "Hello! This is a test message from the Air Quality App."
    send_sms(recipient_number, text_message)
