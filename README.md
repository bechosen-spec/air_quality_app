# Air Quality Monitoring App

## Overview

The Air Quality Monitoring App is a web-based application designed to provide real-time air quality information and personalized health alerts for users. This app predicts Air Quality Index (AQI) levels for different locations and sends personalized notifications to users based on their health conditions and selected location. The app is built with Python and Streamlit and utilizes Mailgun for sending email notifications to users.

## Features

- **User Authentication**: Secure login and sign-up for users.
- **Location-Based AQI Prediction**: Select a location (e.g., Lagos, Ilorin) and get AQI predictions.
- **Personalized Health Alerts**: Tailored warnings for users with health concerns such as respiratory issues.
- **Email Notifications**: Sends AQI alerts to users via Mailgun email notifications.
- **Interactive Dashboard**: Provides a user-friendly interface for viewing AQI and health alerts.

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python, Pandas, Scikit-Learn, TensorFlow, XGBoost
- **Machine Learning Models**: XGBoost (for Lagos AQI), ANN (for Ilorin AQI)
- **Email Notifications**: Mailgun API
- **Environment Management**: Python Dotenv for managing API keys and environment variables

## Installation

### Prerequisites

- Python 3.7 or higher
- Mailgun account for email notifications
- Git

### Clone the Repository

```bash
git clone https://github.com/yourusername/air-quality-monitoring-app.git
cd air-quality-monitoring-app
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Set Up Environment Variables

Create a `.env` file in the root directory and add the following environment variables:

```plaintext
MAILGUN_API_KEY=your_mailgun_api_key
MAILGUN_DOMAIN=sandboxb1b17b26ad8e49c293594054bbf495ac.mailgun.org  # or your custom domain
```

Make sure to replace `your_mailgun_api_key` and `MAILGUN_DOMAIN` with your actual Mailgun credentials.

### Model and Scaler Files

Place the pre-trained models and scaler files in the `models/` directory:

- `xgboost_lagos_model.pkl` for Lagos predictions
- `ann_ilorin_model.h5` for Ilorin predictions
- `scaler.pkl` for scaling features before prediction

### Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

Access the app in your browser at `http://localhost:8501`.

## Usage

1. **Sign Up or Log In**: Register or log in to access the application features.
2. **Dashboard**: After logging in, navigate to the dashboard to view AQI predictions.
3. **Select Location**: Choose between Lagos or Ilorin to see AQI predictions specific to that location.
4. **Receive Alerts**: Users with specific health conditions will receive customized alerts on the dashboard and by email.
5. **Logout**: End the session by clicking the logout button.

## Project Structure

```
air-quality-monitoring-app/
│
├── app.py                    # Main application file for Streamlit
├── requirements.txt          # Required dependencies
├── README.md                 # Project documentation
├── .env.example              # Example environment variables file
│
├── modules/                  # Core application modules
│   ├── model_predictor.py    # Functions for loading models and predicting AQI
│   ├── thresholds.py         # Functions to categorize AQI levels
│   ├── notifications.py      # Mailgun-based email notifications
│   └── user_management.py    # User authentication and management
│
├── models/                   # Pre-trained models and scaler files
│   ├── xgboost_lagos_model.pkl
│   ├── ann_ilorin_model.h5
│   └── scaler.pkl
│
└── data/                     # User data and CSV files
```

## Configuration

- **Environment Variables**: Set up the `.env` file with Mailgun API credentials.
- **Mailgun Settings**:
  - **Authorized Recipients**: If using a free sandbox account, add any recipient emails as **Authorized Recipients** in the Mailgun dashboard.
  - **Custom Domain (optional)**: If you upgrade your Mailgun account, you can use a verified custom domain to send emails without restrictions.

## Future Enhancements

- **Additional Locations**: Expand to include predictions for more locations.
- **SMS Alerts**: Integrate SMS alerts for critical AQI warnings.
- **Improved Health Customization**: Add more specific health categories for tailored notifications.
- **Advanced Models**: Train and incorporate more complex models for greater prediction accuracy.

## Troubleshooting

- **Email Not Delivered**: Check if the email address is authorized in Mailgun settings (for sandbox accounts) or if the Mailgun API key is correct.
- **API Limits**: Free Mailgun accounts are limited. Consider upgrading if you need to send a high volume of emails.
- **Environment Variables**: Ensure `.env` is properly configured with the required Mailgun credentials.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions, please reach out to:

**Emmanuel Boniface**  
Email: boniface.emmanuel.242132@unn.edu.ng
