def parse_dfa_file(filename):
    dfa = {
        'alphabet': set(),
        'states': set(),
        'start_state': '',
        'accept_states': set(),
        'transitions': {}
    }

    with open(filename, 'r') as f:
        isParsingTransitions = False

        for line in f:
            line = line.strip()

            # ignoram liniile goale sau liniile cu comentarii
            if not line or line[0] == '#':
                continue

            # parsing
            if line.startswith('ALPHABET:'):
                values = line.split(':')[1].strip().split(',')
                dfa['alphabet'] = {v.strip() for v in values}

            elif line.startswith('STATES:'):
                values = line.split(':')[1].strip().split(',')
                dfa['states'] = {v.strip() for v in values}
                for state in dfa['states']:
                    dfa['transitions'][state] = {}

            elif line.startswith('START:'):
                dfa['start_state'] = line.split(':')[1].strip()

            elif line.startswith('FINALS:'):
                values = line.split(':')[1].strip().split(',')
                dfa['accept_states'] = {v.strip() for v in values}

            elif line.startswith('TRANSITIONS:'):
                isParsingTransitions = True

            elif isParsingTransitions:
                left_side, next_state = line.split('->')
                current_state, symbol = left_side.split(',')

                current_state = current_state.strip()
                symbol = symbol.strip()
                next_state = next_state.strip()

                dfa['transitions'][current_state][symbol] = next_state

    return dfa


def simulate_dfa(dfa, word):
    current_state = dfa['start_state']
    print(f"\nVerificam cuvantul: '{word}'")
    print(f"-> Start: {current_state}")

    for symbol in word:
        if symbol not in dfa['alphabet']:
            print(f"Eroare: Simbolul '{symbol}' nu este in alfabet!")
            return False

        next_state = dfa['transitions'][current_state][symbol]
        print(f"   [Citesc '{symbol}'] {current_state} -> {next_state}")
        current_state = next_state

    is_accepted = current_state in dfa['accept_states']

    if is_accepted:
        print(f"=> REZULTAT: ACCEPTAT (s-a oprit in {current_state})")
    else:
        print(f"=> REZULTAT: RESPINS (s-a oprit in {current_state})")

    return is_accepted

my_dfa = parse_dfa_file('limbaj_dfa.txt')
simulate_dfa(my_dfa, "1101")    # Acceptat (se termina in 01)
simulate_dfa(my_dfa, "010")     # Respins  (se termina in 10)
simulate_dfa(my_dfa, "000001")  # Acceptat (se termina in 01)
