import re

class SyntaxAnalyzer:
    def __init__(self, expression):
        self.tokens = re.findall(r'\d+|[()+\-*/]', expression)
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self):
        self.pos += 1

    def factor(self):
        token = self.peek()
        if token is None:
            raise SyntaxError("Unexpected end of expression")
        if token.isdigit():
            self.consume()
            return True
        elif token == '(':
            self.consume()
            if not self.expr():
                raise SyntaxError("Invalid expression inside parentheses")
            if self.peek() == ')':
                self.consume()
                return True
            else:
                raise SyntaxError("Missing closing parenthesis")
        else:
            raise SyntaxError(f"Unexpected token: {token}")

    def term(self):
        if not self.factor():
            return False
        while self.peek() in ('*', '/'):
            self.consume()
            if not self.factor():
                raise SyntaxError("Expected a number or '(' after operator")
        return True

    def expr(self):
        if not self.term():
            return False
        while self.peek() in ('+', '-'):
            self.consume()
            if not self.term():
                raise SyntaxError("Expected a number or '(' after operator")
        return True

    def analyze(self):
        if self.expr() and self.pos == len(self.tokens):
            return "Valid Expression"
        else:
            raise SyntaxError("Invalid syntax")

if __name__ == "__main__":
    while True:
        try:
            expr = input("Enter an arithmetic expression (or 'exit' to quit): ")
            if expr.lower() == 'exit':
                break
            analyzer = SyntaxAnalyzer(expr)
            print(analyzer.analyze())
        except SyntaxError as e:
            print("Syntax Error:", e)
