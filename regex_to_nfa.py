# Contor global pentru a genera stari unice (q0, q1, q2...)
state_id = 0

def get_next_state():
    # Functie care ne da urmatorul nume de stare disponibil
    global state_id
    state_name = f"q{state_id}"
    state_id += 1
    return state_name

# PARTEA 1: PARSAREA REGEX-ULUI
def add_explicit_concat(regex):
    # transformam concatenarea "ab" in "a.b" ca sa fie clar
    result = ""
    for i in range(len(regex)):
        result += regex[i]
        if i + 1 < len(regex):
            char1 = regex[i]
            char2 = regex[i + 1]
            # Adaugam '.' intre 2 litere sau dupa o steluta/paranteza inchisa
            if char1 not in '(|' and char2 not in ')*|':
                result += '.'
    return result


def convert_to_postfix(regex):
    # transformam "a.b|c" in "a b . c |" (forma postfixata - mai usor de citit)
    regex = add_explicit_concat(regex)
    priority = {'*': 3, '.': 2, '|': 1, '(': 0}
    output = []
    operator_stack = []

    for char in regex:
        if char.isalnum():  # daca e litera/cifra o punem direct in rezultat
            output.append(char)
        elif char == '(':
            operator_stack.append(char)
        elif char == ')':
            # Scoatem operatori din stiva pana gasim paranteza deschisa
            while operator_stack and operator_stack[-1] != '(':
                output.append(operator_stack.pop())
            operator_stack.pop() # scoatem si '('
        else:
            # e un operator (*, ., |) si respectam ordinea operatiilor matematice
            while operator_stack and priority[operator_stack[-1]] >= priority[char]:
                output.append(operator_stack.pop())
            operator_stack.append(char)

    # scoatem ce a mai ramas in stiva
    while operator_stack:
        output.append(operator_stack.pop())

    return "".join(output)

# PARTEA 2: ALGORITMUL LUI THOMPSON
def build_base_nfa(symbol):
    # NFA pentru o simpla litera (start -> [simbol] -> accept)
    start_state = get_next_state()
    accept_state = get_next_state()
    return {
        'start': start_state,
        'accept': accept_state,
        'transitions': {start_state: {symbol: [accept_state]}}
    }


def apply_concat(nfa1, nfa2):
    # lipirea a doua NFA-uri (A . B)
    transitions = nfa1['transitions']

    # copiem toate sagetile din B in A
    for state, trans_dict in nfa2['transitions'].items():
        transitions[state] = trans_dict

    # legam finalul lui A de inceputul lui B cu epsilon ('e')
    if nfa1['accept'] not in transitions:
        transitions[nfa1['accept']] = {}
    transitions[nfa1['accept']]['e'] = [nfa2['start']]

    return {'start': nfa1['start'], 'accept': nfa2['accept'], 'transitions': transitions}


def apply_union(nfa1, nfa2):
    # SAU (A | B)
    start_state = get_next_state()
    accept_state = get_next_state()

    # din noul start plecam gratuit ('e') fie in A, fie in B
    transitions = {start_state: {'e': [nfa1['start'], nfa2['start']]}}

    for nfa in [nfa1, nfa2]:
        for state, trans_dict in nfa['transitions'].items():
            transitions[state] = trans_dict

        # ambele cai (A si B) se unesc la final in noua stare de acceptare
        if nfa['accept'] not in transitions:
            transitions[nfa['accept']] = {}
        transitions[nfa['accept']]['e'] = [accept_state]

    return {'start': start_state, 'accept': accept_state, 'transitions': transitions}


def apply_star(nfa):
    # steluta (A*)
    start_state = get_next_state()
    accept_state = get_next_state()
    transitions = nfa['transitions']

    # din noul start putem intra in A sau putem sari complet peste el direct la acceptare
    transitions[start_state] = {'e': [nfa['start'], accept_state]}

    if nfa['accept'] not in transitions:
        transitions[nfa['accept']] = {}

    # De la finalul lui A, ne putem INTOARCE la inceput sau putem iesi
    transitions[nfa['accept']]['e'] = [nfa['start'], accept_state]

    return {'start': start_state, 'accept': accept_state, 'transitions': transitions}

# Partea 3: SALVAREA IN FISIER
def generate_nfa_from_regex(regex):
    # Resetam contorul de stari
    global state_id
    state_id = 0

    postfix_regex = convert_to_postfix(regex)
    nfa_stack = []

    # Citim expresia postfixata de la stanga la dreapta
    for char in postfix_regex:
        if char.isalnum():
            nfa_stack.append(build_base_nfa(char))
        elif char == '.':
            nfa2 = nfa_stack.pop()  # ultimul scos este al doilea element
            nfa1 = nfa_stack.pop()
            nfa_stack.append(apply_concat(nfa1, nfa2))
        elif char == '|':
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()
            nfa_stack.append(apply_union(nfa1, nfa2))
        elif char == '*':
            nfa_stack.append(apply_star(nfa_stack.pop()))

    # bucata ramasa in stiva este NFA ul complet
    return nfa_stack.pop()


def save_nfa_to_file(nfa, filename):
    all_states = set(nfa['transitions'].keys())
    all_states.add(nfa['accept'])

    alphabet = set()
    for state, trans_dict in nfa['transitions'].items():
        for symbol in trans_dict.keys():
            if symbol != 'e':
                alphabet.add(symbol)

    # scriem in fisier
    with open(filename, 'w') as f:
        f.write(f"ALPHABET: {', '.join(sorted(alphabet))}\n")
        f.write(f"STATES: {', '.join(sorted(all_states))}\n")
        f.write(f"START: {nfa['start']}\n")
        f.write(f"FINALS: {nfa['accept']}\n")
        f.write("\nTRANSITIONS:\n")

        # iteram prin dictionar ca sa printam de forma: q0, 0 -> q0, q1
        for state in sorted(nfa['transitions'].keys()):
            for symbol, next_states in nfa['transitions'][state].items():
                # Legam starile de destinatie cu virgula (ex: q0, q1)
                destinations = ", ".join(sorted(next_states))
                f.write(f"{state}, {symbol} -> {destinations}\n")

# RULAREA PROGRAMULUI
if __name__ == "__main__":
    input_file = "input_regex.txt"
    output_file = "output_nfa.txt"

    # citim prima linie din fisierul de intrare
    with open(input_file, 'r') as f:
        my_regex = f.readline().strip()

    # generam NFA-ul
    my_nfa = generate_nfa_from_regex(my_regex)

    # salvam in fisierul de iesire
    save_nfa_to_file(my_nfa, output_file)