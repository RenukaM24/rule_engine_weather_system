class Node:
    def __init__(self, node_type, value, left=None, right=None):
        self.type = node_type  # 'operand' or 'operator'
        self.value = value
        self.left = left
        self.right = right

def create_rule(rule_str):
    """Recursively create an AST from the rule string."""
    rule_str = rule_str.strip()
    
    # Remove leading and trailing parentheses if present
    if rule_str.startswith("(") and rule_str.endswith(")"):
        rule_str = rule_str[1:-1].strip()
    
    if 'AND' in rule_str or 'OR' in rule_str:
        operator = 'AND' if 'AND' in rule_str else 'OR'
        left, right = rule_str.split(f' {operator} ', 1)
        return Node('operator', operator, create_rule(left), create_rule(right))
    else:
        return Node('operand', rule_str)

def evaluate_rule(node, data):
    """Evaluate the rule represented by the AST against the provided data."""
    if node.type == 'operand':
        # Remove any leading/trailing parentheses from operand values
        attr, op, value = node.value.strip("()").split()
        
        # Handle value conversion
        if value.startswith("'") and value.endswith("'"):  # Handle string comparison
            value = value[1:-1]
        elif value.isdigit():  # Handle numeric comparison
            value = int(value)

        # Now build the evaluation expression
        if op in ['=', '==']:  # Handling equality checks
            return data[attr] == value
        elif op in ['>', '<', '>=', '<=']:  # Handle numeric comparisons
            return eval(f"{data[attr]} {op} {value}")

    elif node.type == 'operator':
        if node.value == 'AND':
            return evaluate_rule(node.left, data) and evaluate_rule(node.right, data)
        elif node.value == 'OR':
            return evaluate_rule(node.left, data) or evaluate_rule(node.right, data)
