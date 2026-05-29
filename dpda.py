def parse_dpda_file(filename):
    dpda = {
        'alphabet': set(),
        'stack_alphabet': set(),
        'states': set(),
        'start_state': '',
        'stack_start': '',
        'accept_states': set(),
        'transitions': {}
    }

    with open(filename, 'r') as f:
        isParsingTransitions = False

        for line in f:
            line = line.strip()

            # Ignoram liniile goale sau comentariile
            if not line or line[0] == '#':
                continue

            if line.startswith('ALPHABET:'):
                dpda['alphabet'] = {v.strip() for v in line.split(':')[1].split(',')}
            elif line.startswith('STACK_ALPHABET:'):
                dpda['stack_alphabet'] = {v.strip() for v in line.split(':')[1].split(',')}
            elif line.startswith('STATES:'):
                dpda['states'] = {v.strip() for v in line.split(':')[1].split(',')}
                for state in dpda['states']:
                    dpda['transitions'][state] = {}
            elif line.startswith('START:'):
                dpda['start_state'] = line.split(':')[1].strip()
            elif line.startswith('STACK_START:'):
                dpda['stack_start'] = line.split(':')[1].strip()
            elif line.startswith('FINALS:'):
                dpda['accept_states'] = {v.strip() for v in line.split(':')[1].split(',')}
            elif line.startswith('TRANSITIONS:'):
                isParsingTransitions = True
            elif isParsingTransitions:
                # Parsam linia de forma: stare, simbol, top_stiva -> stare_noua, push_stiva
                left_side, right_side = line.split('->')
                current_state, symbol, stack_top = [x.strip() for x in left_side.split(',')]
                next_state, push_symbols = [x.strip() for x in right_side.split(',')]

                # Initializam sub-dictionarele daca nu exista
                if symbol not in dpda['transitions'][current_state]:
                    dpda['transitions'][current_state][symbol] = {}

                # Salvam tranzitia
                dpda['transitions'][current_state][symbol][stack_top] = (next_state, push_symbols)

    return dpda


def simulate_dpda(dpda, word):
    current_state = dpda['start_state']
    # Daca stack_start e 'e', incepem cu stiva goala, altfel punem simbolul de start
    stack = [] if dpda['stack_start'] == 'e' else [dpda['stack_start']]

    print(f"\n{'=' * 40}")
    print(f"Verificam cuvantul: '{word}'")
    print(f"-> Start: {current_state} | Stiva initiala: {stack}")

    i = 0
    step_count = 0

    # Folosim o bucla while pentru a putea evalua tranzitii 'e' (epsilon) succesive
    while step_count < 1000:  # Limita de siguranta contra buclelor infinite in trap states
        step_count += 1

        # Daca am terminat cuvantul, consideram ca primim epsilon ('e') pe input
        current_symbol = word[i] if i < len(word) else 'e'
        # Ce se afla in varful stivei (daca e goala, consideram 'e')
        stack_top = stack[-1] if stack else 'e'

        transition_found = False
        consumed_input = False
        popped_stack = False

        next_state = None
        push_symbols = None
        sym_used = None
        stack_used = None

        # SISTEMUL DE DECIZIE AL AUTOMATULUI (CUM ALEGE CE SA FACA MAI DEPARTE)

        # PRIORITATEA 1: "Am o litera pe banda si o potrivesc cu varful stivei!"
        # Explicație: Este mutarea normala a unui automat. Consumam o litera din cuvant
        # si ne uitam strict la ce se afla in varful stivei.
        # Exemplu din limbaj: q0, 0, $ -> q0, 0$ (Citeste '0', are '$' in varf)
        if current_symbol != 'e' and current_symbol in dpda['transitions'].get(current_state, {}) and stack_top in \
                dpda['transitions'][current_state][current_symbol]:
            next_state, push_symbols = dpda['transitions'][current_state][current_symbol][stack_top]
            sym_used = current_symbol
            stack_used = stack_top
            transition_found = True
            popped_stack = True  # SCOATEM elementul din varf pentru ca l-am potrivit
            consumed_input = True  # TRECEM la urmatoarea litera din cuvant!

        # PRIORITATEA 2: "Citesc litera de pe banda, dar ignor stiva complet!"
        # Explicație: Vrem sa citim litera, dar regula ne spune ca nu conteaza
        # ce avem in stiva ('e' la sectiunea top_stiva). Foarte utila pentru
        # a prinde literele gresite care apar aiurea.
        # Exemplu din limbaj: q1, 0, e -> q3, e (In q1 nu mai avem voie '0')
        elif current_symbol != 'e' and current_symbol in dpda['transitions'].get(current_state, {}) and 'e' in \
                dpda['transitions'][current_state][current_symbol]:
            next_state, push_symbols = dpda['transitions'][current_state][current_symbol]['e']
            sym_used = current_symbol
            stack_used = 'e'
            transition_found = True
            popped_stack = False  # NU scoatem nimic din stiva, pentru ca nu am folosit-o
            consumed_input = True  # TRECEM la urmatoarea litera din cuvant!

        # PRIORITATEA 3: "Nu mai am litere (sau nu se potrivesc). Fac o mutare gratuita (e) pe baza stivei!"
        # Explicație: Abia acum, daca nu am reusit sa consumam nicio litera (sau am
        # terminat cuvantul), automatul are voie sa aplice o tranzitie epsilon pe banda,
        # verificand insa varful stivei.
        # Exemplu din limbaj: q1, e, $ -> q2, $ (S-a terminat cuvantul, stiva e goala -> ACCEPTA)
        elif 'e' in dpda['transitions'].get(current_state, {}) and stack_top in dpda['transitions'][current_state]['e']:
            next_state, push_symbols = dpda['transitions'][current_state]['e'][stack_top]
            sym_used = 'e'
            stack_used = stack_top
            transition_found = True
            popped_stack = True  # SCOATEM elementul din varf
            consumed_input = False  # RAMANEM la aceeasi litera din cuvant!

        # PRIORITATEA 4: "Fac o mutare complet in gol (ignor si litera, si stiva)."
        # Explicație: Ultima solutie de avarie. Nu avem nevoie de input si nu
        # ne uitam deloc la stiva.
        # Exemplu din limbaj: q3, e, e -> q3, e (Bucla infinita/trap-state in q3)
        elif 'e' in dpda['transitions'].get(current_state, {}) and 'e' in dpda['transitions'][current_state]['e']:
            next_state, push_symbols = dpda['transitions'][current_state]['e']['e']
            sym_used = 'e'
            stack_used = 'e'
            transition_found = True
            popped_stack = False  # NU scoatem nimic din stiva
            consumed_input = False  # RAMANEM la aceeasi litera din cuvant!

        # --- DACA NU S-A GASIT NICIO TRANZITIE ---
        if not transition_found:
            if i == len(word):
                break  # Am terminat cuvantul si am facut si toate operatiile 'e' ramase
            else:
                print(
                    f"   [!] BLOCAJ: Nu exista tranzitie din '{current_state}', citind '{current_symbol}', cu '{stack_top}' in varful stivei.")
                break

        # --- EXECUTAM POP ---
        popped_val = '-'
        if popped_stack and stack:
            popped_val = stack.pop()

        # --- EXECUTAM PUSH ---
        if push_symbols != 'e':
            # Le inversam pentru ca primul caracter din string sa ramana in varf
            for char in reversed(push_symbols):
                stack.append(char)

        print(
            f"   [Citesc: '{sym_used}', Stiva_citita: '{stack_used}'] {current_state} -> {next_state} | POP '{popped_val}' | PUSH '{push_symbols}' | Stiva: {stack}")

        current_state = next_state
        if consumed_input:
            i += 1  # Avansam in cuvant doar daca am consumat o litera

        # Daca am ajuns in starea de gunoi si a inceput bucla infinita de curatare in gol, ne oprim logic
        if current_state == 'q3' and sym_used == 'e' and stack_used == 'e':
            print(f"   [!] Automatul a blocat executia in starea de esec (q3).")
            break

    # VERIFICAM CONDITIA DE ACCEPTARE
    is_accepted = (i == len(word) and current_state in dpda['accept_states'])

    if is_accepted:
        print(f"=> REZULTAT: ACCEPTAT (S-a oprit corect in {current_state})")
    else:
        print(f"=> REZULTAT: RESPINS (S-a oprit in {current_state})")

    return is_accepted


# Incarcam limbajul din fisierul creat adineauri
my_dpda = parse_dpda_file('limbaj_dpda.txt')

# Rulam testele cerute de prof
simulate_dpda(my_dpda, "0011")  # Corect -> Acceptat
simulate_dpda(my_dpda, "000111")  # Corect -> Acceptat
simulate_dpda(my_dpda, "0101")  # Intercalat -> Respins (se duce in q3)
simulate_dpda(my_dpda, "10")  # Incepe cu 1 -> Respins (se duce in q3)
simulate_dpda(my_dpda, "001")  # Mai multi de 0 -> Respins
simulate_dpda(my_dpda, "011")  # Mai multi de 1 -> Respins