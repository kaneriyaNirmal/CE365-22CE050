grammar = {
    'S': [['A', 'B', 'C'], ['D']],
    'A': [['a'], ['ε']],
    'B': [['b'], ['ε']],
    'C': [['(', 'S', ')'], ['c']],
    'D': [['A', 'C']]
}

nonterminals = list(grammar.keys())

FIRST = {nt: set() for nt in nonterminals}
FOLLOW = {nt: set() for nt in nonterminals}

def is_nonterminal(symbol):
    return symbol in nonterminals

def compute_first_sets():
    changed = True
    while changed:
        changed = False
        for nt in nonterminals:
            for production in grammar[nt]:
                can_produce_epsilon = True  
                for symbol in production:
                    if not is_nonterminal(symbol):  
                        before_size = len(FIRST[nt])
                        FIRST[nt].add(symbol)
                        after_size = len(FIRST[nt])
                        if after_size > before_size:
                            changed = True
                        can_produce_epsilon = False
                        break  
                    else:  
                        before_size = len(FIRST[nt])
                        FIRST[nt].update(FIRST[symbol] - {'ε'})  
                        after_size = len(FIRST[nt])
                        if after_size > before_size:
                            changed = True
                        if 'ε' not in FIRST[symbol]:  
                            can_produce_epsilon = False
                            break
                
                if can_produce_epsilon:
                    before_size = len(FIRST[nt])
                    FIRST[nt].add('ε')
                    after_size = len(FIRST[nt])
                    if after_size > before_size:
                        changed = True

def compute_follow_sets():
    start_symbol = 'S'
    FOLLOW[start_symbol].add('$')

    changed = True
    while changed:
        changed = False
        for nt in nonterminals:
            for production in grammar[nt]:
                length = len(production)
                for i, symbol in enumerate(production):
                    if is_nonterminal(symbol):  
                        follow_before = len(FOLLOW[symbol])

                        if i + 1 < length:
                            beta = production[i+1:]  
                            first_beta = set()
                            can_all_epsilon = True

                            for beta_sym in beta:
                                if not is_nonterminal(beta_sym):  
                                    first_beta.add(beta_sym)
                                    can_all_epsilon = False
                                    break
                                else:  
                                    first_beta.update(FIRST[beta_sym] - {'ε'})
                                    if 'ε' not in FIRST[beta_sym]:
                                        can_all_epsilon = False
                                        break
                            
                            FOLLOW[symbol].update(first_beta)

                            if can_all_epsilon:  
                                FOLLOW[symbol].update(FOLLOW[nt])

                        else:  
                            FOLLOW[symbol].update(FOLLOW[nt])

                        follow_after = len(FOLLOW[symbol])
                        if follow_after > follow_before:
                            changed = True

compute_first_sets()
compute_follow_sets()

def print_sets():
    print("\nFirst Sets:")
    for nt in nonterminals:
        print(f"FIRST({nt}) = {{{', '.join(sorted(FIRST[nt], key=lambda x: (x!='ε', x)))}}}")

    print("\nFollow Sets:")
    for nt in nonterminals:
        print(f"FOLLOW({nt}) = {{{', '.join(sorted(FOLLOW[nt]))}}}")

if __name__ == "__main__":
    print_sets()
