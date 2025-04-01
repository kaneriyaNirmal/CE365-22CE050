import re

class ConstantFoldingOptimizer:
    def __init__(self, expression):
        self.expression = expression

    def optimize(self):
        # Tokenizing the expression
        tokens = re.findall(r'\d+\.\d+|\d+|[a-zA-Z_]\w*|[+\-*/^()]', self.expression)
        optimized_expr = self.evaluate_constants(tokens)
        return "".join(optimized_expr)

    def evaluate_constants(self, tokens):
        expression_str = "".join(tokens)

        # Finding and evaluating constant expressions using regex
        while True:
            # Match a simple constant operation (e.g., 3*2 or 5+4)
            match = re.search(r'\b\d+(\.\d+)?\s*[\+\-\*/]\s*\d+(\.\d+)?\b', expression_str)
            if not match:
                break  # No more constant expressions found

            # Evaluate the constant subexpression
            result = str(eval(match.group()))
            
            # Replace the subexpression in the expression string
            expression_str = expression_str.replace(match.group(), result, 1)

        return expression_str

if __name__ == "__main__":
    expr = input("Enter an arithmetic expression: ")
    optimizer = ConstantFoldingOptimizer(expr)
    optimized_expr = optimizer.optimize()
    print("Optimized Expression:", optimized_expr)
