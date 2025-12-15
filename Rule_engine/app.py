from flask import Flask, request, jsonify
import sqlite3
import re

app = Flask(__name__)

# Node class for AST representation
class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # "operator" or "operand"
        self.left = left  # Reference to left child Node
        self.right = right  # Reference to right child Node
        self.value = value  # Optional value for operand nodes

    def evaluate(self, data):
        if self.type == "operand":
            attr, operator, val = self.value
            if isinstance(val, str) and val.isdigit():
                val = int(val)  # Convert numeric strings to integers
            
            # Comparison operations
            if operator == "==":
                return data.get(attr) == val
            elif operator == "!=":
                return data.get(attr) != val
            elif operator == "<":
                return data.get(attr) < val
            elif operator == "<=":
                return data.get(attr) <= val
            elif operator == ">":
                return data.get(attr) > val
            elif operator == ">=":
                return data.get(attr) >= val
            return False

        elif self.type == "operator":
            left_result = self.left.evaluate(data) if self.left else False
            right_result = self.right.evaluate(data) if self.right else False

            if self.value == "AND":
                return left_result and right_result
            elif self.value == "OR":
                return left_result or right_result

        return False

    def to_dict(self):
        if self.type == "operand":
            return {
                "type": self.type,
                "value": self.value
            }
        else:
            return {
                "type": self.type,
                "value": self.value,
                "left": self.left.to_dict() if self.left else None,
                "right": self.right.to_dict() if self.right else None
            }

# Function to create AST from rule string
def create_ast(rule_string):
    tokens = re.split(r'(\s+|\(|\)|AND|OR)', rule_string)
    tokens = [token.strip() for token in tokens if token.strip()]

    def parse_expression(index):
        if index >= len(tokens):
            return None, index
        
        token = tokens[index]
        if token == '(':
            left, index = parse_expression(index + 1)
            operator = tokens[index]
            right, index = parse_expression(index + 1)
            index += 1  # skip the closing parenthesis
            return Node("operator", left, right, operator), index
        elif token == ')':
            return None, index + 1
        else:
            match = re.match(r'(\w+)\s*([<>]=?|==|!=)\s*(.+)', token)
            if match:
                attribute, operator, value = match.groups()
                if value.isdigit():
                    value = int(value)  # Convert to int if it’s a number
                return Node("operand", value=(attribute, operator, value)), index + 1

        return None, index

    ast, _ = parse_expression(0)
    return ast

# API to create a rule
@app.route('/create_rule', methods=['POST'])
def create_rule():
    rule_string = request.json.get('rule_string')
    ast = create_ast(rule_string)

    # Check if the AST was created successfully
    if ast is None:
        return jsonify({"error": "Invalid rule syntax"}), 400

    try:
        # Insert rule into the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO rules (rule_string) VALUES (?)', (rule_string,))
        rule_id = cursor.lastrowid  # Get the ID of the newly created rule
        conn.commit()
        conn.close()
        
        # Return success response with the AST and rule ID
        return jsonify({"message": "Rule created", "rule_id": rule_id, "ast": ast.to_dict()}), 201

    except Exception as e:
        # If an error occurs, log it and return a failure response
        print(f"Error inserting rule: {e}")
        return jsonify({"error": "Failed to create rule in the database"}), 500


# API to evaluate rule
@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule():
    rule_id = request.json.get('rule_id')
    user_data = request.json.get('data')

    # Fetch rule from the database
    conn = get_db_connection()
    rule = conn.execute('SELECT rule_string FROM rules WHERE id = ?', (rule_id,)).fetchone()
    conn.close()

    if rule is None:
        return jsonify({"error": "Rule not found"}), 404

    # Create AST from the rule string
    ast = create_ast(rule['rule_string'])

    # Evaluate the AST against user data
    result = ast.evaluate(user_data)
    return jsonify({"eligible": result}), 200

# Helper function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('rules.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to initialize the database
def init_db():
    conn = sqlite3.connect('rules.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_string TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
    conn.commit()
    conn.close()

#I have added this line to test the merging concept
#THis is main
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
