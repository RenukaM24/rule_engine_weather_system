# C:\Users\DELL\rule_engine_weather_system\weather_monitor\visualization.py
import matplotlib.pyplot as plt
from database import init_db, WeatherSummary  # Import WeatherSummary

def plot_weather_summary():
    session = init_db()
    summaries = session.query(WeatherSummary).all()
    
    # Ensure we handle empty data gracefully
    if not summaries:
        print("No weather data available to plot.")
        return
    
    dates = [summary.date for summary in summaries]
    avg_temps = [summary.avg_temp for summary in summaries]
    
    plt.figure(figsize=(10, 5))  # Set the figure size for better readability
    plt.plot(dates, avg_temps, label='Avg Temperature', marker='o')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.title('Daily Average Temperature')
    plt.xticks(rotation=45)  # Rotate date labels for better readability
    plt.legend()
    plt.tight_layout()  # Adjust layout to prevent clipping
    plt.show()
