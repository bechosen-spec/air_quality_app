import streamlit as st
import pandas as pd
from modules.model_predictor import get_prediction
from modules.thresholds import load_thresholds, categorize_aqi
from modules.notifications import send_email
from modules.user_management import sign_up_user, authenticate_user, user_exists

# Load AQI thresholds
thresholds = load_thresholds()

# Initialize session state for navigation and login status
if "page" not in st.session_state:
    st.session_state.page = "home"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None

# Navigation functions
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

# Home Page (Login Form and Platform Details)
if st.session_state.page == "home":
    st.title("Welcome to Air Quality Monitoring")
    st.write("Monitor real-time air quality levels and receive personalized warnings based on your location and health conditions.")

    st.header("Log In")
    username_or_email = st.text_input("Username or Email", key="login_username_or_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log In"):
        user = authenticate_user(username_or_email, password)
        if user:
            login_user(user)
        else:
            st.error("Login failed. Please check your username/email and password.")

    # Link to Sign-Up Page
    if st.button("Create an Account"):
        go_to_page("signup")

# Sign-Up Page
elif st.session_state.page == "signup":
    st.title("Create an Account")
    user_data = sign_up_user()  # Sign-up function that returns the new user's data if created, or None if existing

    # Check if user data exists
    if user_data == "exists":
        st.warning("User already exists. Please log in.")
        go_to_page("home")
    elif user_data:  # Successful sign-up
        login_user(user_data)  # Redirect to dashboard after successful sign-up

    st.button("Back to Home", on_click=lambda: go_to_page("home"))

# Dashboard Page
elif st.session_state.page == "dashboard" and st.session_state.logged_in:
    user = st.session_state.user
    st.title(f"Welcome, {user['name']}!")
    
    # Location selection and AQI display
    location = st.selectbox("Select Location", options=["Lagos", "Ilorin"], key="location_select")
    aqi_today = get_prediction(location)
    category = categorize_aqi(aqi_today, thresholds)

    st.subheader(f"Tomorrow's Air Quality in {location}")
    st.metric(label="AQI Level", value=aqi_today)
    st.write(f"Category: {category}")

    # Display personalized warning
    if user["condition"] == "Respiratory Issue" or user["age"] > 60:
        personalized_message = f"Warning for {user['name']}: Air quality is {category}. Take necessary precautions."
        st.warning(personalized_message)
        
        # Define subject and content, and call `send_email` with Mailgun
        email_subject = "Air Quality Warning"
        send_email(user["email"], email_subject, personalized_message)

    # Logout Button
    if st.button("Logout"):
        logout_user()
