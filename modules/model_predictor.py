import pickle
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
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
    today_data['quarter'] = (today_data['month'] - 1) // 3 + 1  # Calculate quarter manually

    today_data['pm25_lag1'] = [45]
    today_data['pm25_rolling_3'] = [48]
    today_data['pm25_rolling_7'] = [47]

    features = today_data[['day_of_week', 'month', 'quarter', 'pm25_lag1', 'pm25_rolling_3', 'pm25_rolling_7']]
    return features

# Function to generate future data for prediction (next 7 days)
def prepare_data_for_next_week():
    next_week_data = []

    for i in range(1, 8):  # Forecasting for the next 7 days
        future_date = datetime.now() + timedelta(days=i)
        future_data = {
            'date': future_date,
            'day_of_week': future_date.weekday(),
            'month': future_date.month,
            'quarter': (future_date.month - 1) // 3 + 1,  # Calculate quarter manually
            'pm25_lag1': randint(40, 55),  # Simulated value
            'pm25_rolling_3': randint(45, 55),  # Simulated value
            'pm25_rolling_7': randint(45, 55)  # Simulated value
        }
        next_week_data.append(future_data)
    
    next_week_df = pd.DataFrame(next_week_data)
    return next_week_df[['day_of_week', 'month', 'quarter', 'pm25_lag1', 'pm25_rolling_3', 'pm25_rolling_7']]

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

# Function to predict air quality for the next 7 days
def get_weekly_prediction(location):
    # Load the model and scaler
    load_model(location)
    load_scaler(location)
    
    # Prepare the data for the next 7 days
    next_week_data = prepare_data_for_next_week()
    
    # Simulate AQI predictions for the next 7 days using random values
    weekly_predictions = [randint(50, 200) for _ in range(7)]  # Random predictions for the next 7 days
    
    # Return the predictions as a dictionary
    predictions = {
        'dates': [datetime.now() + timedelta(days=i) for i in range(1, 8)],
        'predictions': weekly_predictions
    }
    
    return predictions
