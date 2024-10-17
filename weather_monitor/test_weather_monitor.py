# C:\Users\DELL\rule_engine_weather_system\weather_monitor\test_weather_monitor.py
import pytest
from weather_main import fetch_weather, check_alerts

# Define the temperature conversion function for testing purposes
def convert_kelvin_to_celsius(temp_kelvin):
    return temp_kelvin - 273.15

def test_temperature_conversion():
    assert convert_kelvin_to_celsius(273.15) == 0
    assert convert_kelvin_to_celsius(300) == 26.85  # Additional test case

def test_alerts(capsys):  # Use capsys to capture printed output
    check_alerts(36)  # Should trigger the alert
    captured = capsys.readouterr()
    assert captured.out.strip() == "Alert: Temperature exceeds 35°C!"
    
    check_alerts(34)  # Should not trigger the alert
    captured = capsys.readouterr()
    assert captured.out.strip() == ""  # No output expected
