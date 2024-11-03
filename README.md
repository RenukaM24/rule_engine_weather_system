Application 1: Rule Engine with AST

Objective:
This application determines user eligibility based on attributes such as age, department, income,
and spend, using an Abstract Syntax Tree (AST) to represent conditional rules. The system
supports dynamic creation, combination, and modification of these rules.

Features:
1. Create Rule: Parses a rule string (e.g., 'age > 30 AND department == Sales') and converts it into
an AST.
2. Combine Rules: Combines multiple rules into a single AST, optimizing for efficiency.
3. Evaluate Rule: Takes user data (e.g., age, department, salary) and evaluates the rule's AST to
determine eligibility.

Data Structure:
A node-based structure is used to represent the AST:
Node(type, left=None, right=None, value=None)
- type: Specifies if it's an 'operator' (AND/OR) or 'operand' (condition).
- left: Left child node (for operators).
- right: Right child node (for operators).
- value: The value (for conditions such as age > 30).

Sample Rules:
1. rule1: '((age > 30 AND department == Sales) OR (age < 25 AND department == Marketing)) AND
(salary > 50000 OR experience > 5)'
2. rule2: '((age > 30 AND department == Marketing)) AND (salary > 20000 OR experience > 5)'
API Endpoints:
1. POST /create_rule: Takes a rule string as input and returns its AST representation.
2. POST /combine_rules: Combines multiple rules into a single AST.
3. POST /evaluate_rule: Takes user data and a rule AST, and evaluates the rule against the data.
Database Setup:
Use MongoDB to store the rules as documents.
Installation and Setup:
1. Clone the repository.
 git clone <repository_url>
2. Install dependencies.
 pip install -r requirements.txt
3. Set up MongoDB (either local or Atlas).
4. Start the Flask server.
 python src/app.py

Testing:
1. Create and verify AST representations using the provided API.
2. Combine multiple rules and evaluate the resulting AST using test data.

Application 2: Real-Time Weather Monitoring System

Objective:
This application continuously retrieves weather data from the OpenWeatherMap API and generates
daily summaries, such as average temperature, maximum/minimum temperature, and the dominant
weather condition. Additionally, it triggers alerts when user-defined thresholds are exceeded.

Features:
1. Continuous Data Retrieval: Fetches weather data from the OpenWeatherMap API at configurable
intervals (e.g., every 5 minutes).
2. Daily Summaries: Aggregates data for daily summaries such as average temperature, max/min
temperature, and dominant weather condition.
3. Alerts: Triggers alerts if thresholds are breached (e.g., temperature > 35°C for two consecutive
updates).

Data Processing:
- main: Weather condition (e.g., Rain, Clear).
- temp: Current temperature in Celsius.
- feels_like: Perceived temperature in Celsius.
- dt: Unix timestamp for data update.

Database Setup:
Use MongoDB or any preferred time-series database to store the daily summaries.
Installation and Setup:
1. Clone the repository.
 git clone <repository_url>
2. Install dependencies.
 pip install -r requirements.txt
3. Set up your OpenWeatherMap API key in the .env file.
4. Start the weather monitoring script.
 python src/weather_monitor.py

Testing:
1. Simulate API calls to test data retrieval.
2. Verify temperature conversion from Kelvin to Celsius.
3. Simulate several days of weather updates to verify daily summaries.
4. Test alerting thresholds with custom configurations.
Bonus Features

Application 1: Rule Engine
- Error handling for invalid rule strings.
- Modifying rules dynamically by adding/removing conditions or changing operators.
Application 2: Weather Monitoring System
- Support for additional weather parameters (e.g., humidity, wind speed).
- Visualizations for daily summaries and triggered alerts.
