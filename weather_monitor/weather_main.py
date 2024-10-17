import requests
import time
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from database import init_db, WeatherSummary

API_KEY = '74659a6ec9698d3c041f5b8fb92fc047'  # Your actual API key
CITIES = ['Delhi,in', 'Mumbai,in', 'Chennai,in', 'Bangalore,in', 'Kolkata,in', 'Hyderabad,in']
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

def check_alerts(current_temp, city):
    """Check if temperature exceeds a threshold and trigger an alert."""
    threshold_temp = 35  # Example threshold in °C
    if current_temp > threshold_temp:
        print(f"Alert: Temperature in {city} exceeds {threshold_temp}°C!")

def fetch_weather(session):
    """Fetch weather data for all cities and save daily summaries to the database."""
    daily_summary = {}  # Store aggregated data by date

    for city in CITIES:
        # Measure API request time
        start_time = time.time()
        try:
            response = requests.get(BASE_URL, params={'q': city, 'appid': API_KEY})
            end_time = time.time()
            print(f"Time taken for {city}: {end_time - start_time:.2f} seconds")

            if response.status_code == 200:
                data = response.json()
                temp_kelvin = data['main']['temp']
                temp_celsius = temp_kelvin - 273.15
                weather_condition = data['weather'][0]['description']
                
                # Print temperature and weather condition for each city
                print(f"Temperature in {city}: {temp_celsius:.2f}°C, Condition: {weather_condition}")

                # Check for alerts
                check_alerts(temp_celsius, city)

                # Collect data for rollup summaries
                date = datetime.now().date()
                if date not in daily_summary:
                    daily_summary[date] = {'temps': [], 'conditions': []}
                daily_summary[date]['temps'].append(temp_celsius)
                daily_summary[date]['conditions'].append(weather_condition)

            else:
                print(f"Failed to fetch weather data for {city}: {response.status_code}")
        
        except Exception as e:
            print(f"An error occurred while fetching data for {city}: {e}")

    # Save daily summaries to the database
    save_summaries_to_db(session, daily_summary)

def save_summaries_to_db(session, daily_summary):
    """Save or update daily summaries in the database."""
    for date, details in daily_summary.items():
        avg_temp = sum(details['temps']) / len(details['temps'])
        max_temp = max(details['temps'])
        min_temp = min(details['temps'])
        dominant_condition = max(set(details['conditions']), key=details['conditions'].count)

        try:
            # Check if a summary for the current date already exists
            existing_summary = session.query(WeatherSummary).filter_by(date=date).first()
            if existing_summary:
                # Update the existing summary
                existing_summary.avg_temp = avg_temp
                existing_summary.max_temp = max_temp
                existing_summary.min_temp = min_temp
                existing_summary.dominant_condition = dominant_condition
                print(f"Updated summary for {date}")
            else:
                # Create a new summary
                summary = WeatherSummary(
                    date=date,
                    avg_temp=avg_temp,
                    max_temp=max_temp,
                    min_temp=min_temp,
                    dominant_condition=dominant_condition
                )
                session.add(summary)
                print(f"Saved new summary for {date}")

            # Commit changes to the database
            start_time = time.time()
            session.commit()
            end_time = time.time()
            print(f"Time taken for database commit: {end_time - start_time:.2f} seconds")

        except Exception as e:
            session.rollback()  # Rollback transaction on error
            print(f"An error occurred while saving summaries: {e}")

# Initialize the database and scheduler
scheduler = BackgroundScheduler()
db_session = init_db()

# Schedule the fetch_weather function to run every 5 minutes
scheduler.add_job(fetch_weather, 'interval', minutes=5, args=[db_session])

scheduler.start()
print("Weather monitoring service started...")

# Keep the program running
try:
    while True:
        time.sleep(2)
except (KeyboardInterrupt, SystemExit):
    print("Shutting down the weather monitoring service...")
    scheduler.shutdown()
    db_session.close()
