import re

class QuadrupleGenerator:
    def __init__(self):
        self.temp_count = 1
        self.quadruples = []

    def new_temp(self):
        temp_var = f"t{self.temp_count}"
        self.temp_count += 1
        return temp_var

    def generate_quadruples(self, expression):
        tokens = re.findall(r'\d+|\+|\-|\*|\/|\(|\)', expression)  
        postfix = self.infix_to_postfix(tokens)
        self.evaluate_postfix(postfix)

    def infix_to_postfix(self, tokens):
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        operators = []

        for token in tokens:
            if token.isdigit():  
                output.append(token)
            elif token in precedence:  
                while operators and operators[-1] != '(' and precedence[operators[-1]] >= precedence[token]:
                    output.append(operators.pop())
                operators.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    output.append(operators.pop())
                operators.pop()  

        while operators:
            output.append(operators.pop())

        return output

    def evaluate_postfix(self, postfix):
        stack = []
        for token in postfix:
            if token.isdigit():
                stack.append(token)
            else:  
                op2 = stack.pop()
                op1 = stack.pop()
                temp_var = self.new_temp()
                self.quadruples.append((token, op1, op2, temp_var))
                stack.append(temp_var)

    def display_quadruples(self):
        print(f"{'Operator':<10} {'Operand 1':<10} {'Operand 2':<10} {'Result':<10}")
        for quad in self.quadruples:
            print(f"{quad[0]:<10} {quad[1]:<10} {quad[2]:<10} {quad[3]:<10}")

if __name__ == "__main__":
    expr = input("Enter an arithmetic expression: ")
    generator = QuadrupleGenerator()
    generator.generate_quadruples(expr)
    generator.display_quadruples()
