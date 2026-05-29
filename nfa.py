def parse_nfa_file(filename):
    nfa = {
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
                nfa['alphabet'] = {v.strip() for v in values}

            elif line.startswith('STATES:'):
                values = line.split(':')[1].strip().split(',')
                nfa['states'] = {v.strip() for v in values}
                for state in nfa['states']:
                    nfa['transitions'][state] = {}

            elif line.startswith('START:'):
                nfa['start_state'] = line.split(':')[1].strip()

            elif line.startswith('FINALS:'):
                values = line.split(':')[1].strip().split(',')
                nfa['accept_states'] = {v.strip() for v in values}

            elif line.startswith('TRANSITIONS:'):
                isParsingTransitions = True

            elif isParsingTransitions:
                left_side, right_side = line.split('->')
                current_state, symbol = left_side.split(',')
                next_states = {s.strip() for s in right_side.split(',')}

                current_state = current_state.strip()
                symbol = symbol.strip()

                nfa['transitions'][current_state][symbol] = next_states

    return nfa


def simulate_nfa(nfa, word):
    current_states = {nfa['start_state']}

    print(f"\nVerificam cuvantul: '{word}'")
    print(f"-> Start: {current_states}")

    for symbol in word:
        if symbol not in nfa['alphabet']:
            print(f"Eroare: Simbolul '{symbol}' nu este in alfabet!")
            return False

        next_current_states = set()

        for state in current_states:
            if symbol in nfa['transitions'][state]:
                destinations = nfa['transitions'][state][symbol]
                next_current_states.update(destinations)

        current_states = next_current_states
        print(f"   [Citesc '{symbol}'] Stari active acum: {current_states}")

        if not current_states:
            print("   [!] Toate ramurile au murit.")
            break

    intersectie = current_states.intersection(nfa['accept_states'])
    is_accepted = len(intersectie) > 0

    if is_accepted:
        print(f"=> REZULTAT: ACCEPTAT (S-a oprit in {current_states}, care contine starea finala)")
    else:
        print(f"=> REZULTAT: RESPINS (S-a oprit in {current_states})")

    return is_accepted

my_nfa = parse_nfa_file('limbaj_nfa.txt')
simulate_nfa(my_nfa, "1101")    # Acceptat (se termina in 01)
simulate_nfa(my_nfa, "010")     # Respins  (se termina in 10)
simulate_nfa(my_nfa, "000001")  # Acceptat (se termina in 01)
