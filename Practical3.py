import sys
import re

def remove_comments(src):
    src = re.sub(r'//.*', '', src)
    return re.sub(r'/\*.*?\*/', '', src, flags=re.DOTALL)

def main():
    if len(sys.argv) < 2:
        print("Usage: python lexical_analyzer.py <source_file.c>")
        sys.exit(1)
    try:
        with open(sys.argv[1]) as f:
            src = f.read()
    except FileNotFoundError:
        print(f"File '{sys.argv[1]}' not found.")
        sys.exit(1)

    src = remove_comments(src)

    keywords = {"auto", "break", "case", "char", "const", "continue", "default", "do", "double",
                "else", "enum", "extern", "float", "for", "goto", "if", "int", "long", "register",
                "return", "short", "signed", "sizeof", "static", "struct", "switch", "typedef",
                "union", "unsigned", "void", "volatile", "while"}
    type_keywords = {"int", "char", "float", "double", "void", "long", "short", "signed", "unsigned"}

    tokens = []
    errors = []
    line_no = 1
    pos = 0
    length = len(src)

    while pos < length:
        ch = src[pos]
        if ch.isspace():
            if ch == '\n':
                line_no += 1
            pos += 1
            continue

        if ch.isalpha() or ch == '_':
            start = pos
            while pos < length and (src[pos].isalnum() or src[pos] == '_'):
                pos += 1
            lexeme = src[start:pos]
            if lexeme in keywords:
                tokens.append(('Keyword', lexeme, line_no))
            else:
                tokens.append(('Identifier', lexeme, line_no))
            continue

        if ch.isdigit():
            start = pos
            while pos < length and src[pos].isdigit():
                pos += 1
            if pos < length and src[pos].isalpha():
                while pos < length and src[pos].isalnum():
                    pos += 1
                lexeme = src[start:pos]
                errors.append((lexeme, line_no))
            else:
                lexeme = src[start:pos]
                tokens.append(('Constant', lexeme, line_no))
            continue

        if ch == '"' or ch == "'":
            quote = ch
            literal = ch
            pos += 1
            while pos < length:
                c = src[pos]
                literal += c
                if c == '\\':
                    pos += 1
                    if pos < length:
                        literal += src[pos]
                elif c == quote:
                    pos += 1
                    break
                pos += 1
            tokens.append(('String', literal, line_no))
            continue

        op_multi = {"==", "!=", "<=", ">=", "++", "--", "&&", "||"}
        op_single = {"+", "-", "*", "/", "=", "<", ">"}
        punctuation_set = {"(", ")", "{", "}", "[", "]", ",", ";"}

        if pos + 1 < length and src[pos:pos+2] in op_multi:
            tokens.append(('Operator', src[pos:pos+2], line_no))
            pos += 2
            continue
        if ch in op_single:
            tokens.append(('Operator', ch, line_no))
            pos += 1
            continue
        if ch in punctuation_set:
            tokens.append(('Punctuation', ch, line_no))
            pos += 1
            continue

        errors.append((ch, line_no))
        pos += 1

    symbol_table = set()
    for i, token in enumerate(tokens):
        ttype, lexeme, lno = token
        if ttype == "Identifier":
            if i > 0 and i < len(tokens) - 1:
                prev_token = tokens[i - 1]
                next_token = tokens[i + 1]
                if (prev_token[0] == "Keyword" and prev_token[1] in type_keywords and
                    next_token[0] == "Punctuation" and next_token[1] == '('):
                    continue
            symbol_table.add(lexeme)

    print("TOKENS")
    for ttype, lexeme, lno in tokens:
        print(f"{ttype}: {lexeme}")

    print("\nLEXICAL ERRORS")
    if errors:
        for lex, lno in errors:
            print(f"{lex} invalid lexeme at line {lno}")
    else:
        print("None")

    print("\nSYMBOL TABLE ENTRIES")
    for idx, ident in enumerate(sorted(symbol_table), start=1):
        print(f"{idx}) {ident}")

if __name__ == '__main__':
    main()
