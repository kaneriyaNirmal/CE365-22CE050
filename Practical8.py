import pandas as pd

grammar = {
    'S': [['A', 'B', 'C'], ['D']],
    'A': [['a'], ['ε']],
    'B': [['b'], ['ε']],
    'C': [['(', 'S', ')'], ['c']],
    'D': [['A', 'C']]
}

nonterminals = list(grammar.keys())

FIRST = {
    'S': {'a', 'b', '(', 'c'},
    'A': {'a', 'ε'},
    'B': {'b', 'ε'},
    'C': {'(', 'c'},
    'D': {'a', '('}
}

FOLLOW = {
    'S': {')', '$'},
    'A': {'b', '(', ')', '$'},
    'B': {'c', ')', '$'},
    'C': {')', '$'},
    'D': {')', '$'}
}

terminals = set()
for rules in grammar.values():
    for production in rules:
        for symbol in production:
            if symbol not in nonterminals and symbol != 'ε':
                terminals.add(symbol)
terminals.add('$')

parsing_table = {nt: {t: None for t in terminals} for nt in nonterminals}


def construct_parsing_table():
    for nt in grammar:
        for production in grammar[nt]:
            first_set = set()
            can_produce_epsilon = True

            for symbol in production:
                if symbol in nonterminals:
                    first_set.update(FIRST[symbol] - {'ε'})
                    if 'ε' not in FIRST[symbol]:
                        can_produce_epsilon = False
                        break
                else:
                    first_set.add(symbol)
                    can_produce_epsilon = False
                    break

            for terminal in first_set:
                parsing_table[nt][terminal] = production

            if can_produce_epsilon:
                for terminal in FOLLOW[nt]:
                    parsing_table[nt][terminal] = production


def print_parsing_table():
    print("\nPredictive Parsing Table:")
    df = pd.DataFrame(parsing_table).T.fillna("-")
    print(df)


def check_ll1():
    for nt in parsing_table:
        seen = set()
        for terminal in parsing_table[nt]:
            if parsing_table[nt][terminal] is not None:
                if terminal in seen:
                    return False
                seen.add(terminal)
    return True


def parse_string(input_string):
    stack = ['$', 'S']
    input_string += '$'
    pointer = 0

    while stack:
        top = stack.pop()
        current_symbol = input_string[pointer]

        if top == current_symbol:
            pointer += 1
            continue
        elif top in terminals or top == '$':
            return "Invalid string"
        elif parsing_table[top][current_symbol] is None:
            return "Invalid string"
        else:
            stack.extend(reversed(parsing_table[top][current_symbol]))

    return "Valid string" if pointer == len(input_string) else "Invalid string"


if __name__ == "__main__":
    construct_parsing_table()
    print_parsing_table()

    if check_ll1():
        print("\nThe given grammar is LL(1).")
    else:
        print("\nThe given grammar is NOT LL(1).")

    test_string = "ac"
    print(f"\nTesting input: '{test_string}'")
    print(parse_string(test_string))
