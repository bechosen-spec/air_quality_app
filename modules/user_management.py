import streamlit as st
import pandas as pd
import hashlib

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Initialize session state for form fields if not set
def initialize_sign_up_state():
    fields = ["name", "username", "email", "password", "location", "age", "condition"]
    for field in fields:
        if field not in st.session_state:
            st.session_state[field] = ""  # Default to an empty string or appropriate default value

# Call this function at the beginning to ensure keys are initialized
initialize_sign_up_state()

# Sign-Up Function with session state to persist data
def sign_up_user():
    st.title("User Sign-Up")

    # Input fields for user sign-up using session state to avoid refreshing prematurely
    st.session_state["name"] = st.text_input("Name", value=st.session_state["name"], key="sign_up_name")
    st.session_state["username"] = st.text_input("Username", value=st.session_state["username"], key="sign_up_username")
    st.session_state["email"] = st.text_input("Email", value=st.session_state["email"], key="sign_up_email")
    st.session_state["password"] = st.text_input("Password", type="password", value=st.session_state["password"], key="sign_up_password")
    st.session_state["location"] = st.selectbox("Location", options=["Lagos", "Ilorin"], index=0 if st.session_state["location"] == "" else ["Lagos", "Ilorin"].index(st.session_state["location"]), key="sign_up_location")
    st.session_state["age"] = st.number_input("Age", min_value=0, value=int(st.session_state["age"]) if st.session_state["age"] else 0, key="sign_up_age")
    st.session_state["condition"] = st.selectbox("Health Condition", options=["None", "Respiratory Issue"], index=0 if st.session_state["condition"] == "" else ["None", "Respiratory Issue"].index(st.session_state["condition"]), key="sign_up_condition")

    if st.button("Submit", key="sign_up_submit"):
        # Ensure required fields are filled
        if st.session_state["username"] and st.session_state["password"]:  
            hashed_password = hash_password(st.session_state["password"])  # Hash the password for storage
            
            # Create a user data dictionary
            user_data = {
                "name": st.session_state["name"], 
                "username": st.session_state["username"], 
                "email": st.session_state["email"], 
                "password": hashed_password,
                "location": st.session_state["location"], 
                "age": st.session_state["age"], 
                "condition": st.session_state["condition"]
            }
            
            # Save the data to CSV
            pd.DataFrame([user_data]).to_csv("data/user_data.csv", mode='a', header=False, index=False)
            
            # Reset session state after successful sign-up
            initialize_sign_up_state()
            st.success("User signed up successfully!")
        else:
            st.error("Please enter both a username and password.")
