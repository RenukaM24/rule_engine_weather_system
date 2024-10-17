from flask import Flask, request, jsonify
from ast_engine import create_rule, evaluate_rule
import sqlite3

app = Flask(__name__)

# API to create a new rule
@app.route('/create_rule', methods=['POST'])
def create_rule_api():
    rule_str = request.json['rule']
    rule_node = create_rule(rule_str)

    # Connect to SQLite database
    conn = sqlite3.connect('C:/Users/DELL/rule_engine_weather_system/rule_storage.db')
    cursor = conn.cursor()

    # Insert the rule into the database
    cursor.execute("INSERT INTO rules (name, ast) VALUES (?, ?)",
                   (rule_str, str(rule_node)))
    conn.commit()
    conn.close()

    return jsonify({"message": "Rule created successfully"})

# API to evaluate a rule based on user-provided data
@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_api():
    data = request.json['data']
    rule_id = request.json['rule_id']

    # Fetch the rule's AST from the database
    conn = sqlite3.connect('C:/Users/DELL/rule_engine_weather_system/rule_storage.db')
    cursor = conn.cursor()
    cursor.execute("SELECT ast FROM rules WHERE id = ?", (rule_id,))
    
    row = cursor.fetchone()
    if not row:
        return jsonify({"error": "Rule not found"}), 404

    rule_node = eval(row[0])  # Warning: Use eval carefully

    conn.close()

    # Evaluate the rule against the provided data
    result = evaluate_rule(rule_node, data)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
