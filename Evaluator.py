from itertools import product

class Evaluator:
    def __init__(self, root):
        self.root = root

    def evaluate_with_tracking(self, node, values, sub_results):
        # Evaluate basic logical statements or recursively process subtrees
        if node.value in {"TRUE", "FALSE"}:
            return node.value == "TRUE"
        elif node.value in {"P", "Q", "S"}:
            return values[node.value]
        elif node.value == "NOT":
            left_result = self.evaluate_with_tracking(node.left, values, sub_results)
            sub_results[f"NOT {self._node_to_string(node.left)}"] = not left_result
            return not left_result
        else:
            left_result = self.evaluate_with_tracking(node.left, values, sub_results)
            right_result = self.evaluate_with_tracking(node.right, values, sub_results)

            if node.value == "AND":
                result = left_result and right_result
            elif node.value == "OR":
                result = left_result or right_result
            elif node.value == "IMPLIES":
                result = not left_result or right_result
            elif node.value == "EQUIVALENT":
                result = left_result == right_result

            expression = f"({self._node_to_string(node.left)} {node.value} {self._node_to_string(node.right)})"
            sub_results[expression] = result
            return result

    def generate_truth_table(self, variables):
        table = []
        all_sub_results = set()
        variables = sorted(variables)  

        for combo in product([False, True], repeat=len(variables)):
            values = dict(zip(variables, combo))
            sub_results = {}
            result = self.evaluate_with_tracking(self.root, values, sub_results)
            sub_results["Result"] = result
            table.append((values, sub_results))
            all_sub_results.update(sub_results.keys())

        # Ensure intermediate columns are ordered by complexity (shorter expressions first)
        intermediate_columns = sorted(
            (col for col in all_sub_results if col != "Result"),
            key=lambda expr: (expr.count("("), len(expr))  # Order by nesting depth, then length
        )
        final_columns = variables + intermediate_columns + ["Result"]

        return table, final_columns

    def _node_to_string(self, node):
        if not node.left and not node.right:
            return node.value
        if node.value == "NOT":
            return f"NOT {self._node_to_string(node.left)}"
        return f"({self._node_to_string(node.left)} {node.value} {self._node_to_string(node.right)})"
