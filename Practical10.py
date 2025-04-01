import ply.lex as lex
import ply.yacc as yacc

# Token Definitions
tokens = ('NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EXP', 'LPAREN', 'RPAREN')

# Regular Expressions for Tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EXP = r'\^'
t_LPAREN = r'\('
t_RPAREN = r'\)'

# Token for numbers (integer & decimal)
def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)  # Convert to int or float
    return t

# Ignored characters (spaces, tabs)
t_ignore = ' \t'

# Error Handling for Invalid Characters
def t_error(t):
    print("Invalid expression")
    t.lexer.skip(1)

# Build the Lexer
lexer = lex.lex()

# Parsing Rules (Grammar & Semantic Actions)
def p_expression_plus(p):
    "E : E PLUS T"
    p[0] = p[1] + p[3]

def p_expression_minus(p):
    "E : E MINUS T"
    p[0] = p[1] - p[3]

def p_expression_term(p):
    "E : T"
    p[0] = p[1]

def p_term_times(p):
    "T : T TIMES F"
    p[0] = p[1] * p[3]

def p_term_divide(p):
    "T : T DIVIDE F"
    if p[3] == 0:
        print("Error: Division by zero")
        p[0] = 0
    else:
        p[0] = p[1] / p[3]

def p_term_factor(p):
    "T : F"
    p[0] = p[1]

def p_factor_exponent(p):
    "F : G EXP F"
    p[0] = p[1] ** p[3]

def p_factor_group(p):
    "F : G"
    p[0] = p[1]

def p_group_paren(p):
    "G : LPAREN E RPAREN"
    p[0] = p[2]

def p_group_number(p):
    "G : NUMBER"
    p[0] = p[1]

# Error Rule for Syntax Errors
def p_error(p):
    print("Invalid expression")
    return None

# Build the Parser
parser = yacc.yacc()

# Main Function to Take Input and Parse
def evaluate_expression(expression):
    try:
        result = parser.parse(expression)
        if result is not None:
            print("Result:", result)
    except:
        print("Invalid expression")

# User Input
if __name__ == "__main__":
    expr = input("Enter an arithmetic expression: ")
    evaluate_expression(expr)
