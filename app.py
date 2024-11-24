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

def send_login_notifications(user):
    location = user["location"]
    aqi_today = get_prediction(location)
    category = categorize_aqi(aqi_today, thresholds)
    message = f"Hi {user['name']}, the air quality in {location} is '{category}' (AQI: {aqi_today}). Stay informed and safe!"
    
    send_email(user["email"], "Air Quality Alert", message)
    send_whatsapp(user["phone"], message)
    st.info(f"Notification sent to {user['name']} via email and WhatsApp.")

# Home Page
if st.session_state.page == "home":
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Air Quality Monitoring</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Monitor air quality levels and receive timely notifications to stay safe and healthy.</p>", unsafe_allow_html=True)

    st.subheader("Log In")
    username_or_email = st.text_input("Username or Email", key="login_username_or_email", placeholder="Enter your username or email")
    password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Log In", use_container_width=True):
            user = authenticate_user(username_or_email, password)
            if user:
                login_user(user)
            else:
                st.error("Login failed. Please check your credentials.")
    with col2:
        if st.button("Create an Account", use_container_width=True):
            go_to_page("signup")

# Sign-Up Page
elif st.session_state.page == "signup":
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Create an Account</h1>", unsafe_allow_html=True)
    user_data = sign_up_user()

    if user_data == "exists":
        st.warning("User already exists. Please log in.")
        go_to_page("home")
    elif user_data:
        login_user(user_data)

    st.button("Back to Home", on_click=lambda: go_to_page("home"), use_container_width=True)

# Dashboard Page
elif st.session_state.page == "dashboard" and st.session_state.logged_in:
    user = st.session_state.user
    st.markdown(f"<h1 style='text-align: center;'>Welcome, {user['name']}!</h1>", unsafe_allow_html=True)

    location = st.selectbox("Select Your Location", ["Lagos", "Ilorin"], key="location_select")
    aqi_today = get_prediction(location)
    category = categorize_aqi(aqi_today, thresholds)

    st.subheader(f"Air Quality in {location}")
    st.metric(label="AQI Level", value=aqi_today, delta=None)
    st.markdown(f"<p style='font-size: 16px;'>The air quality is categorized as <b>{category}</b>. Stay cautious!</p>", unsafe_allow_html=True)

    if user["condition"] == "Respiratory Issue" or user["age"] > 60:
        personalized_message = f"Dear {user['name']}, the air quality in {location} is '{category}' (AQI: {aqi_today}). Take necessary precautions!"
        st.warning(personalized_message)

    if st.button("Logout", use_container_width=True):
        logout_user()
