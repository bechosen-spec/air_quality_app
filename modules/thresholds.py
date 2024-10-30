import yaml

def load_thresholds():
    with open('config/thresholds.yaml') as file:
        thresholds = yaml.safe_load(file)
    return thresholds

def categorize_aqi(aqi, thresholds):
    for category, range_ in thresholds['AQI_levels'].items():
        min_val, max_val = map(int, range_.split('-'))
        if min_val <= aqi <= max_val:
            return category
    return "Unknown"
