def validate_string(transitions, start_state, accept_states, input_string):
    current_state = start_state

    for char in input_string:
        if char in transitions[current_state]:
            current_state = transitions[current_state][char]  
        else:
            return False  

    return current_state in accept_states

def main():
    num_input_symbols = int(input("Number of input symbols: "))
    input_symbols = input("Input symbols: ").split()

    num_states = int(input("Enter number of states: "))
    start_state = int(input("Initial state: "))

    num_accept_states = int(input("Number of accepting states: "))
    accept_states = set(map(int, input("Accepting states: ").split()))

    transitions = {}
    print("Transition table:")
    for _ in range(num_states * num_input_symbols):
        from_state, symbol, to_state = input("Enter transition (fromState - symbol - toState): ").split()
        from_state = int(from_state)
        to_state = int(to_state)
        if from_state not in transitions:
            transitions[from_state] = {}
        transitions[from_state][symbol] = to_state

    input_string = input("Input string: ")

    if validate_string(transitions, start_state, accept_states, input_string):
        print("Valid String")
    else:
        print("Invalid String")

if __name__ == "__main__":
    main()