def parse_dfa_file(filename):
    # setam structura principala a automatului
    # folosim set() la alfabet si stari ca sa fim siguri ca nu avem duplicate
    dfa = {
        'alphabet': set(),
        'states': set(),
        'start_state': '',
        'accept_states': set(),
        'transitions': {}
    }

    with open(filename, 'r') as f:
        # un flag care ne zice cand am ajuns la sectiunea de sageti ca sa stim cum sa citim
        isParsingTransitions = False

        for line in f:
            line = line.strip()

            # ignoram liniile goale sau cele cu comentarii din fisierul text
            if not line or line[0] == '#':
                continue

            # parsam sectiunile fisierului una cate una
            if line.startswith('ALPHABET:'):
                values = line.split(':')[1].strip().split(',')
                dfa['alphabet'] = {v.strip() for v in values}

            elif line.startswith('STATES:'):
                values = line.split(':')[1].strip().split(',')
                dfa['states'] = {v.strip() for v in values}

                # pregatim dictionarul de tranzitii gol pentru fiecare stare in parte
                for state in dfa['states']:
                    dfa['transitions'][state] = {}

            elif line.startswith('START:'):
                dfa['start_state'] = line.split(':')[1].strip()

            elif line.startswith('FINALS:'):
                values = line.split(':')[1].strip().split(',')
                dfa['accept_states'] = {v.strip() for v in values}

            elif line.startswith('TRANSITIONS:'):
                # de aici incolo citim doar regulile de miscare
                isParsingTransitions = True

            elif isParsingTransitions:
                # parsam linia de tipul: q0, 0 -> q1
                # intai despartim stanga de dreapta dupa sageata
                left_side, next_state = line.split('->')

                # apoi spargem stanga in stare si litera citita
                current_state, symbol = left_side.split(',')

                # curatam spatiile inutile ca sa nu ne dea erori aiurea la stringuri
                current_state = current_state.strip()
                symbol = symbol.strip()
                next_state = next_state.strip()

                # mapam totul in dictionar: din starea X cu litera Y ajung in Z
                dfa['transitions'][current_state][symbol] = next_state

    return dfa


def simulate_dfa(dfa, word):
    # incepem curat din starea de start definita in fisier
    current_state = dfa['start_state']

    print(f"\nVerificam cuvantul: '{word}'")
    print(f"-> Start: {current_state}")

    # parcurgem cuvantul litera cu litera
    for symbol in word:

        # tratam cazul in care primim un caracter pe care automatul nu il cunoaste
        if symbol not in dfa['alphabet']:
            print(f"   [!] Eroare: Simbolul '{symbol}' nu este in alfabetul nostru")
            return False

        # intrebam dictionarul unde trebuie sa ne mutam
        next_state = dfa['transitions'][current_state][symbol]
        print(f"   [Citesc '{symbol}'] {current_state} -> {next_state}")

        # facem efectiv mutarea pentru pasul urmator
        current_state = next_state

    # cuvantul s-a terminat, vedem daca am ramas pe o stare finala
    is_accepted = current_state in dfa['accept_states']

    if is_accepted:
        print(f"=> REZULTAT: ACCEPTAT (s-a oprit in {current_state})")
    else:
        print(f"=> REZULTAT: RESPINS (s-a oprit in {current_state})")

    return is_accepted


# RULARE
# incarcam automatul din fisierul configurat
my_dfa = parse_dfa_file('limbaj_dfa.txt')

# testam regulile (automatul recunoaste cuvinte terminate in 01)
simulate_dfa(my_dfa, "1101")  # Acceptat (se termina in 01)
simulate_dfa(my_dfa, "010")  # Respins  (se termina in 10)
simulate_dfa(my_dfa, "000001")  # Acceptat (se termina in 01)