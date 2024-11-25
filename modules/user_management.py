# import streamlit as st
# import pandas as pd
# import hashlib

# # Function to hash passwords
# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# # Initialize session state for form fields if not set
# def initialize_sign_up_state():
#     fields = ["name", "username", "email", "phone_number", "password", "location", "age", "condition"]
#     for field in fields:
#         if field not in st.session_state:
#             st.session_state[field] = ""

# initialize_sign_up_state()  # Ensure session state fields are initialized

# # Function to check if a user with the given username or email already exists
# def user_exists(username, email, phone_number):
#     try:
#         users = pd.read_csv("data/user_data.csv", names=["name", "username", "email", "phone_number", "password", "location", "age", "condition"])
#     except FileNotFoundError:
#         return False  # If no user data file exists, no user exists yet

#     # Check if any row matches the given username, email, or phone number
#     return not users[(users["username"] == username) | (users["email"] == email) | (users["phone_number"] == phone_number)].empty

# # Sign-Up Function with session state to persist data
# def sign_up_user():
#     st.title("User Sign-Up")

#     # Input fields for user sign-up using session state to avoid refreshing prematurely
#     st.session_state["name"] = st.text_input("Name", value=st.session_state["name"], key="sign_up_name")
#     st.session_state["username"] = st.text_input("Username", value=st.session_state["username"], key="sign_up_username")
#     st.session_state["email"] = st.text_input("Email", value=st.session_state["email"], key="sign_up_email")
#     st.session_state["phone_number"] = st.text_input("Phone Number", value=st.session_state["phone_number"], key="sign_up_phone")
#     st.session_state["password"] = st.text_input("Password", type="password", value=st.session_state["password"], key="sign_up_password")
#     st.session_state["location"] = st.selectbox("Location", options=["Lagos", "Ilorin"], index=0 if st.session_state["location"] == "" else ["Lagos", "Ilorin"].index(st.session_state["location"]), key="sign_up_location")
#     st.session_state["age"] = st.number_input("Age", min_value=0, value=int(st.session_state["age"]) if st.session_state["age"] else 0, key="sign_up_age")
#     st.session_state["condition"] = st.selectbox("Health Condition", options=["None", "Respiratory Issue"], index=0 if st.session_state["condition"] == "" else ["None", "Respiratory Issue"].index(st.session_state["condition"]), key="sign_up_condition")

#     if st.button("Submit", key="sign_up_submit"):
#         # Ensure required fields are filled
#         if st.session_state["username"] and st.session_state["password"] and st.session_state["phone_number"]:
#             # Check if the user already exists
#             if user_exists(st.session_state["username"], st.session_state["email"], st.session_state["phone_number"]):
#                 st.warning("User already exists. Please log in instead.")
#                 return "exists"

#             # Hash the password for storage
#             hashed_password = hash_password(st.session_state["password"])

#             # Create a user data dictionary
#             user_data = {
#                 "name": st.session_state["name"], 
#                 "username": st.session_state["username"], 
#                 "email": st.session_state["email"], 
#                 "phone_number": st.session_state["phone_number"], 
#                 "password": hashed_password,
#                 "location": st.session_state["location"], 
#                 "age": st.session_state["age"], 
#                 "condition": st.session_state["condition"]
#             }

#             # Save the data to CSV
#             pd.DataFrame([user_data]).to_csv("data/user_data.csv", mode='a', header=False, index=False)

#             # Reset session state after successful sign-up
#             initialize_sign_up_state()
#             st.success("User signed up successfully!")
#             return user_data  # Return the new user data for automatic login
#         else:
#             st.error("Please enter all required fields, including a phone number.")
    
#     return None  # No user created

# # Login Function
# def authenticate_user(username_or_email, password):
#     # Load the user data
#     try:
#         users = pd.read_csv("data/user_data.csv", names=["name", "username", "email", "phone_number", "password", "location", "age", "condition"])
#     except FileNotFoundError:
#         st.error("User data file not found. Please sign up first.")
#         return None

#     # Hash the password entered by the user for comparison
#     hashed_password = hash_password(password)

#     # Check if there’s a matching user with the provided username/email and password
#     user = users[(users["username"] == username_or_email) | (users["email"] == username_or_email)]
#     if not user.empty and user.iloc[0]["password"] == hashed_password:
#         return user.iloc[0].to_dict()  # Return user data if authenticated
#     else:
#         st.error("Invalid username/email or password.")
#         return None


import streamlit as st
import pandas as pd
import hashlib
import os

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Initialize session state for form fields if not set
def initialize_sign_up_state():
    fields = ["name", "username", "email", "phone_number", "password", "location", "age", "condition"]
    for field in fields:
        if field not in st.session_state:
            st.session_state[field] = ""

initialize_sign_up_state()  # Ensure session state fields are initialized

# Function to check if a user with the given username or email already exists
def user_exists(username, email, phone_number):
    file_path = "data/user_data.csv"
    if not os.path.exists(file_path):  # If no user data file exists, no user exists yet
        return False

    try:
        users = pd.read_csv(file_path, names=["name", "username", "email", "phone_number", "password", "location", "age", "condition"])
    except Exception as e:
        st.error(f"Error reading user data file: {e}")
        return False

    # Check if any row matches the given username, email, or phone number
    return not users[(users["username"] == username) | (users["email"] == email) | (users["phone_number"] == phone_number)].empty

# Sign-Up Function with session state to persist data
def sign_up_user():
    st.title("User Sign-Up")

    # Input fields for user sign-up using session state to avoid refreshing prematurely
    st.session_state["name"] = st.text_input("Name", value=st.session_state["name"], key="sign_up_name")
    st.session_state["username"] = st.text_input("Username", value=st.session_state["username"], key="sign_up_username")
    st.session_state["email"] = st.text_input("Email", value=st.session_state["email"], key="sign_up_email")
    st.session_state["phone_number"] = st.text_input("Phone Number (234---)", value=st.session_state["phone_number"], key="sign_up_phone")
    st.session_state["password"] = st.text_input("Password", type="password", value=st.session_state["password"], key="sign_up_password")
    st.session_state["location"] = st.selectbox("Location", options=["Lagos", "Ilorin"], 
                                                index=0 if st.session_state["location"] == "" else ["Lagos", "Ilorin"].index(st.session_state["location"]), 
                                                key="sign_up_location")
    st.session_state["age"] = st.number_input("Age", min_value=0, 
                                              value=int(st.session_state["age"]) if st.session_state["age"] else 0, 
                                              key="sign_up_age")
    st.session_state["condition"] = st.selectbox("Health Condition", options=["None", "Respiratory Issue"], 
                                                 index=0 if st.session_state["condition"] == "" else ["None", "Respiratory Issue"].index(st.session_state["condition"]), 
                                                 key="sign_up_condition")

    if st.button("Submit", key="sign_up_submit"):
        # Ensure required fields are filled
        if st.session_state["username"] and st.session_state["password"] and st.session_state["phone_number"]:
            # Check if the user already exists
            if user_exists(st.session_state["username"], st.session_state["email"], st.session_state["phone_number"]):
                st.warning("User already exists. Please log in instead.")
                return "exists"

            # Hash the password for storage
            hashed_password = hash_password(st.session_state["password"])

            # Create a user data dictionary
            user_data = {
                "name": st.session_state["name"], 
                "username": st.session_state["username"], 
                "email": st.session_state["email"], 
                "phone_number": st.session_state["phone_number"], 
                "password": hashed_password,
                "location": st.session_state["location"], 
                "age": st.session_state["age"], 
                "condition": st.session_state["condition"]
            }

            # Ensure the data directory exists
            os.makedirs("data", exist_ok=True)

            # Save the data to CSV
            pd.DataFrame([user_data]).to_csv("data/user_data.csv", mode='a', header=not os.path.exists("data/user_data.csv"), index=False)

            # Reset session state after successful sign-up
            initialize_sign_up_state()
            st.success("User signed up successfully!")
            return user_data  # Return the new user data for automatic login
        else:
            st.error("Please enter all required fields, including a phone number.")
    
    return None  # No user created

# Login Function
def authenticate_user(username_or_email, password):
    file_path = "data/user_data.csv"
    if not os.path.exists(file_path):
        st.error("User data file not found. Please sign up first.")
        return None

    try:
        users = pd.read_csv(file_path, names=["name", "username", "email", "phone_number", "password", "location", "age", "condition"])
    except Exception as e:
        st.error(f"Error reading user data file: {e}")
        return None

    # Hash the password entered by the user for comparison
    hashed_password = hash_password(password)

    # Check if there’s a matching user with the provided username/email and password
    user = users[(users["username"] == username_or_email) | (users["email"] == username_or_email)]
    if not user.empty and user.iloc[0]["password"] == hashed_password:
        return user.iloc[0].to_dict()  # Return user data if authenticated
    else:
        st.error("Invalid username/email or password.")
        return None
