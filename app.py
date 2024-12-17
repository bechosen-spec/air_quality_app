import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import threading

from modules.model_predictor import get_prediction, get_weekly_prediction
from modules.thresholds import load_thresholds, categorize_aqi
from modules.user_management import sign_up_user, authenticate_user

from vonage import Auth, Vonage
from vonage_sms import SmsMessage, SmsResponse

# -------------------- Load AQI thresholds --------------------
thresholds = load_thresholds()

# -------------------- Session State Initialization --------------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "notification_thread_started" not in st.session_state:
    st.session_state.notification_thread_started = False

# -------------------- SMS Sending Function --------------------
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
    api_key = "76a587fb"  # Replace with your actual API key
    api_secret = "WXIjygq7rXkIwoQD"  # Replace with your actual API secret

    auth = Auth(api_key=api_key, api_secret=api_secret)
    client = Vonage(auth)

    try:
        # Debug: Print the phone number before sending
        print(f"Sending SMS to: {to}")

        # Create the SMS message
        sms_message = SmsMessage(
            to=to,
            from_="Air Quality App",  # Replace with approved Sender ID if necessary
            text=message,
        )

        # Send the SMS
        response: SmsResponse = client.sms.send(sms_message)

        # Debug: Print the full response
        print("Response:", response)

        if response["messages"][0]["status"] == "0":
            print("Message sent successfully.")
        else:
            print(f"Message failed with error: {response['messages'][0]['error-text']}")
    except Exception as e:
        print(f"Error sending SMS: {e}")

# -------------------- Validate Phone Number --------------------
def validate_phone_number(phone_number):
    """Validates and formats the phone number."""
    if pd.isna(phone_number) or not phone_number:
        return None
    phone_number = str(phone_number).strip()
    if phone_number.startswith("+") and phone_number[1:].isdigit():
        return phone_number
    elif phone_number.startswith("234") and phone_number[3:].isdigit():
        return f"+{phone_number}"
    elif phone_number.isdigit() and len(phone_number) >= 10:
        return f"+{phone_number}"
    return None

# -------------------- Periodic Notifications --------------------
def send_periodic_notifications():
    """Sends periodic AQI notifications to all registered users."""
    while True:
        try:
            users = pd.read_csv(
                "data/user_data.csv",
                names=["name", "username", "email", "phone", "password", "location", "age", "condition"],
            )
            for _, user in users.iterrows():
                phone_number = validate_phone_number(user.get("phone"))
                if not phone_number:
                    print(f"Invalid phone for user {user['name']}")
                    continue

                location = user["location"]
                aqi_today = get_prediction(location)
                category = categorize_aqi(aqi_today, thresholds)
                message = f"Hi {user['name']}, the air quality in {location} is '{category}' (AQI: {aqi_today}). Stay safe!"
                
                send_sms(phone_number, message)
        except Exception as e:
            print(f"Error in notifications: {e}")
        threading.Event().wait(36000)  # Wait for 10 hours

if not st.session_state.notification_thread_started:
    threading.Thread(target=send_periodic_notifications, daemon=True).start()
    st.session_state.notification_thread_started = True

# -------------------- Navigation --------------------
def go_to_page(page):
    st.session_state.page = page

def login_user(user):
    st.session_state.logged_in = True
    st.session_state.user = user
    go_to_page("dashboard")

def logout_user():
    st.session_state.logged_in = False
    st.session_state.user = None
    go_to_page("home")

# -------------------- Pages --------------------
def home_page():
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Air Quality Monitoring</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Track air quality and receive real-time notifications.</p>", unsafe_allow_html=True)
    
    st.subheader("Log In")
    username_or_email = st.text_input("Username or Email", placeholder="Enter your username or email")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Log In"):
            user = authenticate_user(username_or_email, password)
            if user:
                login_user(user)
            else:
                st.error("Invalid credentials.")
    with col2:
        if st.button("Create Account"):
            go_to_page("signup")

def signup_page():
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Create an Account</h1>", unsafe_allow_html=True)
    user_data = sign_up_user()
    if user_data == "exists":
        st.warning("User already exists. Please log in.")
        go_to_page("home")
    elif user_data:
        login_user(user_data)
    st.button("Back to Home", on_click=lambda: go_to_page("home"))

def dashboard_page():
    user = st.session_state.user
    st.markdown(f"<h1 style='text-align: center;'>Welcome, {user['name']}!</h1>", unsafe_allow_html=True)

    location = st.selectbox("Select Your Location", ["Lagos", "Ilorin"], index=0)
    aqi_today = get_prediction(location)
    category = categorize_aqi(aqi_today, thresholds)

    st.metric(label=f"AQI Level in {location}", value=aqi_today)
    st.info(f"The air quality is '{category}'. Take necessary precautions!" if user["condition"] else "")

    st.subheader("Weekly AQI Forecast")
    weekly_predictions = get_weekly_prediction(location)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(weekly_predictions["dates"], weekly_predictions["predictions"], marker='o')
    ax.set_xlabel("Date")
    ax.set_ylabel("AQI")
    ax.set_title(f"Air Quality Forecast for {location}")
    st.pyplot(fig)

    st.button("Logout", on_click=logout_user)

# -------------------- Page Routing --------------------
if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "signup":
    signup_page()
elif st.session_state.page == "dashboard" and st.session_state.logged_in:
    dashboard_page()
else:
    st.error("Please log in to access this page.")
