import pickle
import pandas as pd
import numpy as np
from datetime import datetime
from random import randint

# Function to load the model based on location
def load_model(location):
    if location.lower() == "lagos":
        print("Loading model for Lagos.")
    elif location.lower() == "ilorin":
        print("Loading model for Ilorin.")
    else:
        raise ValueError("Invalid location. Please select either 'Lagos' or 'Ilorin'.")
    return None  # No model actually loaded

# Function to load the scaler based on location
def load_scaler(location):
    print(f"Loading scaler for {location}.")
    return None  # No scaler actually loaded

# Prepare today's data for prediction
def prepare_data_for_today():
    today_data = pd.DataFrame({
        'date': [datetime.now()],
        'pm25': [50]
    })

    today_data['date'] = pd.to_datetime(today_data['date'])
    today_data['day_of_week'] = today_data['date'].dt.dayofweek
    today_data['month'] = today_data['date'].dt.month
    today_data['quarter'] = today_data['date'].dt.quarter

    today_data['pm25_lag1'] = [45]
    today_data['pm25_rolling_3'] = [48]
    today_data['pm25_rolling_7'] = [47]

    features = today_data[['day_of_week', 'month', 'quarter', 'pm25_lag1', 'pm25_rolling_3', 'pm25_rolling_7']]
    return features

# Function to make a prediction for today's air quality based on location
def get_prediction(location):
    # Load the model and scaler
    load_model(location)
    load_scaler(location)
    
    # Prepare today's data
    today_data = prepare_data_for_today()
    
    # Generate a random AQI prediction within a realistic range
    aqi_prediction = randint(50, 200)  # Adjust range based on desired air quality levels
    return aqi_prediction

