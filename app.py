import streamlit as st
import pandas as pd
from modules.model_predictor import get_prediction
from modules.thresholds import load_thresholds, categorize_aqi
from modules.notifications import send_email, send_whatsapp
from modules.user_management import sign_up_user, authenticate_user, user_exists
from datetime import datetime, timedelta
import threading

# Load AQI thresholds
thresholds = load_thresholds()

# Initialize session state for navigation and login status
if "page" not in st.session_state:
    st.session_state.page = "home"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None

# Periodic Notifications Function
def send_periodic_notifications():
    while True:
        try:
            users = pd.read_csv("data/user_data.csv", names=["name", "username", "email", "phone", "password", "location", "age", "condition"])
            for _, user in users.iterrows():
                location = user["location"]
                aqi_today = get_prediction(location)
                category = categorize_aqi(aqi_today, thresholds)
                message = f"Hi {user['name']}, the air quality in {location} is '{category}' (AQI: {aqi_today}). Stay safe!"
                
                send_email(user["email"], "Air Quality Alert", message)
                send_whatsapp(user["phone"], message)

            print(f"Notifications sent at {datetime.now()}.")
        except Exception as e:
            print(f"Error during notifications: {e}")
        threading.Event().wait(36000)  # Wait 10 hours

# Start periodic notifications thread
if "notification_thread_started" not in st.session_state:
    notification_thread = threading.Thread(target=send_periodic_notifications, daemon=True)
    notification_thread.start()
    st.session_state.notification_thread_started = True

# Navigation Functions
def go_to_page(page):
    st.session_state.page = page

def login_user(user):
    st.session_state.logged_in = True
    st.session_state.user = user
    send_login_notifications(user)
    go_to_page("dashboard")

def logout_user():
    st.session_state.logged_in = False
    st.session_state.user = None
    go_to_page("home")

# Function to send notifications when the user logs in
def send_login_notifications(user):
    location = user["location"]
    aqi_today = get_prediction(location)
    category = categorize_aqi(aqi_today, thresholds)
    message = f"Hi {user['name']}, the air quality in {location} is '{category}' (AQI: {aqi_today}). Stay informed and safe!"
    
    send_email(user["email"], "Air Quality Alert", message)
    send_whatsapp(user["phone"], message)
    st.info(f"Notification sent to {user['name']} via email and WhatsApp.")

# Sidebar Navigation
st.sidebar.title("Navigation")
if st.session_state.logged_in:
    st.sidebar.button("Dashboard", on_click=lambda: go_to_page("dashboard"))
    st.sidebar.button("Logout", on_click=logout_user)
else:
    st.sidebar.button("Home", on_click=lambda: go_to_page("home"))
    st.sidebar.button("Sign Up", on_click=lambda: go_to_page("signup"))

# Home Page (Login Form and Platform Details)
if st.session_state.page == "home":
    st.title("🌎 Welcome to Air Quality Monitoring")
    st.write("Keep track of air quality levels and receive personalized alerts based on your health and location.")
    
    st.subheader("Log In")
    username_or_email = st.text_input("Username or Email", key="login_username_or_email", placeholder="Enter your username or email")
    password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
    
    # Login and Create Account Buttons
    if st.button("Log In"):
        user = authenticate_user(username_or_email, password)
        if user:
            login_user(user)
        else:
            st.error("Invalid login details. Please try again.")

    st.write("---")  # Divider for better visual separation

    if st.button("Create an Account"):
        go_to_page("signup")

# Sign-Up Page
elif st.session_state.page == "signup":
    st.title("🌱 Create an Account")
    st.write("Join us to start monitoring air quality tailored to your needs.")
    user_data = sign_up_user()  # Sign-up function that returns the new user's data if created, or None if existing

    if user_data == "exists":
        st.warning("User already exists. Please log in.")
        go_to_page("home")
    elif user_data:
        login_user(user_data)

    st.button("Back to Home", on_click=lambda: go_to_page("home"), use_container_width=True)

# Dashboard Page
elif st.session_state.page == "dashboard" and st.session_state.logged_in:
    user = st.session_state.user
    st.title(f"👋 Welcome, {user['name']}!")
    st.write("Monitor air quality updates and receive warnings tailored for you.")

    # Location selection and AQI display
    st.selectbox("Select Your Location", options=["Lagos", "Ilorin"], key="location_select")
    aqi_today = get_prediction(st.session_state.location_select)
    category = categorize_aqi(aqi_today, thresholds)

    st.subheader(f"🌤 Air Quality Forecast for {st.session_state.location_select}")
    st.metric(label="AQI Level", value=aqi_today)
    st.write(f"**Category:** {category}")
    
    # Display personalized warning
    if user.get("condition") == "Respiratory Issue" or user.get("age", 0) > 60:
        personalized_message = f"⚠️ Warning for {user['name']}: Air quality is categorized as {category}. Please take necessary precautions."
        st.warning(personalized_message)

        # Send email notification
        send_email(user["email"], "Air Quality Warning", personalized_message)
