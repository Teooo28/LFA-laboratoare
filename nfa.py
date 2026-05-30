def parse_nfa_file(filename):
    # setam structura de baza a automatului nfa
    nfa = {
        'alphabet': set(),
        'states': set(),
        'start_state': '',
        'accept_states': set(),
        'transitions': {}
    }

    with open(filename, 'r') as f:
        # flag ca sa stim cand incepem sa citim sagetile
        isParsingTransitions = False

        for line in f:
            line = line.strip()

            # sarim peste liniile goale sau comentarii
            if not line or line[0] == '#':
                continue

            # parsam componentele limbajului din fisier
            if line.startswith('ALPHABET:'):
                values = line.split(':')[1].strip().split(',')
                nfa['alphabet'] = {v.strip() for v in values}

            elif line.startswith('STATES:'):
                values = line.split(':')[1].strip().split(',')
                nfa['states'] = {v.strip() for v in values}

                # pregatim dictionarul gol pentru fiecare stare
                for state in nfa['states']:
                    nfa['transitions'][state] = {}

            elif line.startswith('START:'):
                nfa['start_state'] = line.split(':')[1].strip()

            elif line.startswith('FINALS:'):
                values = line.split(':')[1].strip().split(',')
                nfa['accept_states'] = {v.strip() for v in values}

            elif line.startswith('TRANSITIONS:'):
                # aici incep regulile de miscare
                isParsingTransitions = True

            elif isParsingTransitions:
                # parsam linia de tipul: q0, 0 -> q0, q1
                left_side, right_side = line.split('->')
                current_state, symbol = left_side.split(',')

                # aici e diferenta majora fata de dfa: putem avea mai multe stari destinatie
                # asa ca le punem direct intr un set
                next_states = {s.strip() for s in right_side.split(',')}

                # curatam de spatii
                current_state = current_state.strip()
                symbol = symbol.strip()

                # mapam starea si simbolul la SET-ul de stari urmatoare
                nfa['transitions'][current_state][symbol] = next_states

    return nfa


def simulate_nfa(nfa, word):
    # diferenta la nfa: in loc de o stare, pornim cu un set de stari
    # adica clonam automatul pentru fiecare drum posibil
    current_states = {nfa['start_state']}

    print(f"\nVerificam cuvantul: '{word}'")
    print(f"-> Start: {current_states}")

    # citim fiecare litera din cuvant
    for symbol in word:

        # validare ca la dfa sa nu pice pe litere necunoscute
        if symbol not in nfa['alphabet']:
            print(f"   [!] Eroare: Simbolul '{symbol}' nu este in alfabet!")
            return False

        # in setul asta vom aduna toate "clonele" noi dupa ce citesc litera
        next_current_states = set()

        # luam fiecare ramura activa la pasul curent
        for state in current_states:
            # daca starea respectiva are o ruta valida pentru litera asta
            if symbol in nfa['transitions'][state]:
                # aflam unde se duc sagetile si le adaugam la multimea viitoare (cu update)
                destinations = nfa['transitions'][state][symbol]
                next_current_states.update(destinations)

        # trecem efectiv la pasul urmator, stergand starile vechi
        current_states = next_current_states
        print(f"   [Citesc '{symbol}'] Stari active acum: {current_states}")

        # daca la un moment dat setul e gol, inseamna ca automatul s-a blocat pe toate caile
        if not current_states:
            print("   [!] Toate ramurile au murit.")
            break

    # conditia de acceptare: vedem daca macar o clona din multimea finala a ajuns in accept_states
    # pur si simplu verificam daca exista elemente comune folosind intersection
    intersectie = current_states.intersection(nfa['accept_states'])
    is_accepted = len(intersectie) > 0

    if is_accepted:
        print(f"=> REZULTAT: ACCEPTAT (S-a oprit in {current_states}, care contine starea finala)")
    else:
        print(f"=> REZULTAT: RESPINS (S-a oprit in {current_states})")

    return is_accepted


# RULARE
# incarcam automatul
my_nfa = parse_nfa_file('limbaj_nfa.txt')

# testam regulile
simulate_nfa(my_nfa, "1101")  # Acceptat (se termina in 01)
simulate_nfa(my_nfa, "010")  # Respins  (se termina in 10)
simulate_nfa(my_nfa, "000001")  # Acceptat (se termina in 01)