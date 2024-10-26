
# Dynamic Rule Engine Application using AST

## Overview

This project is a **Dynamic Rule Engine Application** that evaluates user eligibility based on customizable conditions. The engine is structured in a **3-tier architecture** with a UI, API, and backend to support a variety of dynamic rules, created using an **Abstract Syntax Tree (AST)**. With this rule engine, users can define complex conditions involving attributes such as age, department, income, and spend. 

The application is built with **Flask** for the API layer and **SQLite** for persistent rule storage, and it provides a flexible way to create, store, and evaluate rules dynamically.

---

## Features

- **Dynamic Rule Creation**: Rules can be created using a custom syntax that supports logical operators (`AND`, `OR`) and various comparison operators (`>`, `<`, `==`, `!=`).
- **AST Representation**: Rules are parsed and stored as an Abstract Syntax Tree (AST) to allow easy evaluation and modification.
- **Persistent Storage**: Rules are stored in an SQLite database for long-term access.
- **Custom Evaluation**: User data is evaluated against stored rules to determine eligibility based on predefined criteria.
- **Error Handling**: Robust error handling for invalid rules and data formats.

---

## Data Structure

The core of the rule engine revolves around the **Node** class, representing each component in the AST. The AST is used to parse and evaluate logical and comparison expressions.

### Node Class Structure

- **Type**: Specifies if the node is an `operator` (e.g., `AND`, `OR`) or `operand` (comparison condition).
- **Left**: Reference to the left child node.
- **Right**: Reference to the right child node.
- **Value**: Contains the specific value or comparison details for `operand` nodes.

#### Example Rule Structure
For a rule like `((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)`, the AST would contain nodes representing each condition (`age > 30`, `salary > 50000`, etc.) and logical connectors (`AND`, `OR`) between them.

---

## Database Schema

The application uses an SQLite database to store rules. Below is the schema for the `rules` table:

- **id**: Unique identifier for each rule.
- **rule_string**: Original rule string provided by the user.
- **created_at**: Timestamp for when the rule was added.

Example SQL Table:
```sql
CREATE TABLE rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_string TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## API Endpoints

The application includes two primary API endpoints:

1. **Create Rule**
   - **Endpoint**: `/create_rule`
   - **Method**: `POST`
   - **Input**: JSON body containing a `rule_string` (e.g., `"((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"`).
   - **Output**: JSON response with a success message and the AST structure.

2. **Evaluate Rule**
   - **Endpoint**: `/evaluate_rule`
   - **Method**: `POST`
   - **Input**: JSON body with `rule_id` and `data` (a dictionary of user attributes to evaluate).
   - **Output**: JSON response indicating if the user is eligible according to the rule (`true` or `false`).

### Example JSON Inputs

#### Create Rule
```json
{
  "rule_string": "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
}
```

#### Evaluate Rule
```json
{
  "rule_id": 1,
  "data": {
    "age": 35,
    "department": "Sales",
    "salary": 60000,
    "experience": 3
  }
}
```

---

## Implementation Details

### Parsing and AST Generation
The `create_ast` function parses the rule string, splitting it into tokens and constructing a tree using the `Node` class. Each condition and logical operator is represented by nodes in the AST, allowing for structured rule evaluation.

### Rule Evaluation
The `evaluate` method in the `Node` class recursively traverses the AST. For each operand node, it performs the specified comparison with user data; for each operator node, it combines results from left and right nodes based on the logical operator (`AND`, `OR`).

---

## Example Scenarios and Testing

### Test Cases
1. **Create and Verify AST Structure**: Use the `create_rule` endpoint to add new rules and check the resulting AST.
2. **Combine and Evaluate Rules**: Use the `evaluate_rule` endpoint to test various scenarios and verify that the correct eligibility result (`true` or `false`) is returned.
3. **Error Handling**: Test with incorrect rule syntax or incomplete data to verify error messages and validations.

### Sample Rule
```plaintext
Rule: ((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)
Data: {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
Expected Output: true
```

---

## Error Handling and Validation

The application provides the following validations and error handling mechanisms:
- **Rule Syntax Validation**: Ensures the rule string is valid before parsing.
- **Data Type Validation**: Checks that data types match the expected types in each rule.
- **Missing Data Handling**: Returns an error if required fields are missing from the input data.

---

## Future Enhancements

- **User-Defined Functions**: Extend support for custom functions within rules for more advanced conditions.
- **UI Layer**: Add a user-friendly interface for rule creation and evaluation.
- **Enhanced Storage**: Migrate from SQLite to a scalable database for larger datasets.
- **Rule Optimization**: Implement rule simplification to optimize performance.

---

## How to Run the Application

1. **Clone the Repository**: 
   ```bash
   git clone <repository-url>
   ```
   
2. **Set Up Environment**:
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   
3. **Initialize Database**:
   ```bash
   python app.py
   ```
   
4. **Run the Application**:
   ```bash
   python app.py
   ```
   
5. **Test with Postman**:
   - Use Postman or a similar tool to interact with the `/create_rule` and `/evaluate_rule` endpoints.

---

