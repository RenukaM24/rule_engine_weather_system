import unittest
from ast_engine import create_rule, evaluate_rule, Node

class TestRuleEngine(unittest.TestCase):

    def test_create_single_rule(self):
        """Test creation of a single rule."""
        rule = "age > 30"
        ast = create_rule(rule)
        self.assertEqual(ast.type, 'operand')
        self.assertEqual(ast.value, 'age > 30')

    def test_create_nested_rule(self):
        """Test creation of a nested rule."""
        rule = "(age > 30 AND department = 'Sales')"
        ast = create_rule(rule)
        self.assertEqual(ast.type, 'operator')
        self.assertEqual(ast.value, 'AND')
        self.assertEqual(ast.left.value, 'age > 30')
        self.assertEqual(ast.right.value, "department = 'Sales'")

    def test_evaluate_single_rule(self):
        """Test evaluating a single rule with matching data."""
        rule = "age > 30"
        data = {'age': 35}
        ast = create_rule(rule)
        result = evaluate_rule(ast, data)
        self.assertTrue(result)

    def test_evaluate_rule_with_non_matching_data(self):
        """Test evaluating a rule with non-matching data."""
        rule = "age > 30"
        data = {'age': 25}
        ast = create_rule(rule)
        result = evaluate_rule(ast, data)
        self.assertFalse(result)

    def test_evaluate_combined_rule(self):
        """Test evaluating a combined rule."""
        rule = "(age > 30 AND department = 'Sales')"
        data = {'age': 35, 'department': 'Sales'}
        ast = create_rule(rule)
        result = evaluate_rule(ast, data)
        self.assertTrue(result)

    def test_evaluate_combined_rule_false(self):
        """Test evaluating a combined rule that returns false."""
        rule = "(age > 30 AND department = 'Sales')"
        data = {'age': 25, 'department': 'Sales'}
        ast = create_rule(rule)
        result = evaluate_rule(ast, data)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
