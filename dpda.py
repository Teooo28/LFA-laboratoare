def parse_dpda_file(filename):
    # structura principala unde tinem tot dpda-ul
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
        # flag ca sa stim cand incepem sa citim sagetile
        isParsingTransitions = False

        for line in f:
            line = line.strip()

            # sarim peste liniile goale sau comentarii
            if not line or line[0] == '#':
                continue

            # parsam informatiile generale
            if line.startswith('ALPHABET:'):
                dpda['alphabet'] = {v.strip() for v in line.split(':')[1].split(',')}
            elif line.startswith('STACK_ALPHABET:'):
                dpda['stack_alphabet'] = {v.strip() for v in line.split(':')[1].split(',')}
            elif line.startswith('STATES:'):
                dpda['states'] = {v.strip() for v in line.split(':')[1].split(',')}

                # pregatim dictionarul gol de tranzitii pentru fiecare stare
                for state in dpda['states']:
                    dpda['transitions'][state] = {}
            elif line.startswith('START:'):
                dpda['start_state'] = line.split(':')[1].strip()
            elif line.startswith('STACK_START:'):
                dpda['stack_start'] = line.split(':')[1].strip()
            elif line.startswith('FINALS:'):
                dpda['accept_states'] = {v.strip() for v in line.split(':')[1].split(',')}
            elif line.startswith('TRANSITIONS:'):
                # de aici incep regulile de functionare
                isParsingTransitions = True

            elif isParsingTransitions:
                # parsam linia de forma: stare, simbol, top_stiva -> stare_noua, push_stiva
                left_side, right_side = line.split('->')
                current_state, symbol, stack_top = [x.strip() for x in left_side.split(',')]
                next_state, push_symbols = [x.strip() for x in right_side.split(',')]

                # daca n-am mai bagat nimic pe litera asta, ii facem un dictionar
                if symbol not in dpda['transitions'][current_state]:
                    dpda['transitions'][current_state][symbol] = {}

                # mapam starea noua si ce aruncam pe stiva in functie de ce era in varf
                dpda['transitions'][current_state][symbol][stack_top] = (next_state, push_symbols)

    return dpda


def simulate_dpda(dpda, word):
    current_state = dpda['start_state']

    # initializam stiva: ori ramane goala, ori ii punem simbolul de start (ex: $)
    stack = [] if dpda['stack_start'] == 'e' else [dpda['stack_start']]

    print(f"\n{'=' * 40}")
    print(f"Verificam cuvantul: '{word}'")
    print(f"-> Start: {current_state} | Stiva initiala: {stack}")

    i = 0
    step_count = 0

    # folosim while in loc de for pentru ca s-ar putea sa stam pe loc in cuvant (pe mutari epsilon)
    # punem o limita de 1000 de pasi ca sa evitam buclele infinite (trap states)
    while step_count < 1000:
        step_count += 1

        # daca am ramas fara litere, ne comportam ca si cum am primit un epsilon pe banda
        current_symbol = word[i] if i < len(word) else 'e'

        # aruncam un ochi in varful stivei (daca e goala consideram ca e epsilon)
        stack_top = stack[-1] if stack else 'e'

        # flaguri ca sa stim ce am facut tura asta si sa printam corect la final
        transition_found = False
        consumed_input = False
        popped_stack = False

        next_state = None
        push_symbols = None
        sym_used = None
        stack_used = None

        # PRIORITATEA 1: am litera pe banda si o potrivesc cu varful stivei
        # asta e mutarea clasica, consumam litera si ne legam de stiva
        if current_symbol != 'e' and current_symbol in dpda['transitions'].get(current_state, {}) and stack_top in \
                dpda['transitions'][current_state][current_symbol]:
            next_state, push_symbols = dpda['transitions'][current_state][current_symbol][stack_top]
            sym_used = current_symbol
            stack_used = stack_top
            transition_found = True
            popped_stack = True  # scoatem varful vechi
            consumed_input = True  # am folosit litera, trecem la urmatoarea

        # PRIORITATEA 2: citesc litera de pe banda, dar ignor stiva complet
        # perfect pentru cand primesc litere interzise si trebuie sa arunc automatul in trap-state
        elif current_symbol != 'e' and current_symbol in dpda['transitions'].get(current_state, {}) and 'e' in \
                dpda['transitions'][current_state][current_symbol]:
            next_state, push_symbols = dpda['transitions'][current_state][current_symbol]['e']
            sym_used = current_symbol
            stack_used = 'e'
            transition_found = True
            popped_stack = False  # n am atins stiva
            consumed_input = True  # am scapat de litera

        # PRIORITATEA 3: mutare epsilon pe banda, dar folosesc stiva
        # utila la final cand am terminat cuvantul si vreau sa golesc $ de pe stiva ca sa dau accept
        elif 'e' in dpda['transitions'].get(current_state, {}) and stack_top in dpda['transitions'][current_state]['e']:
            next_state, push_symbols = dpda['transitions'][current_state]['e'][stack_top]
            sym_used = 'e'
            stack_used = stack_top
            transition_found = True
            popped_stack = True  # scoatem de pe stiva
            consumed_input = False  # nu am citit litera, ramanem pe loc in cuvant

        # PRIORITATEA 4: mutare epsilon completa (ignor si banda si stiva)
        elif 'e' in dpda['transitions'].get(current_state, {}) and 'e' in dpda['transitions'][current_state]['e']:
            next_state, push_symbols = dpda['transitions'][current_state]['e']['e']
            sym_used = 'e'
            stack_used = 'e'
            transition_found = True
            popped_stack = False
            consumed_input = False

        # daca nu s-a potrivit nimic din cascada de mai sus
        if not transition_found:
            # daca am terminat si operatiile din coada, iesim
            if i == len(word):
                break
            else:
                # altfel e un blocaj
                print(
                    f"   [!] BLOCAJ: Nu exista tranzitie din '{current_state}', citind '{current_symbol}', cu '{stack_top}' in varful stivei.")
                break

        # executam pop-ul (scoatem de pe stiva daca a cerut regula)
        popped_val = '-'
        if popped_stack and stack:
            popped_val = stack.pop()

        # executam push-ul (bagam pe stiva daca ne-a dat caractere)
        if push_symbols != 'e':
            # le inversam ca primul element din sir sa ajunga fix in varful stivei la final
            for char in reversed(push_symbols):
                stack.append(char)

        print(
            f"   [Citesc: '{sym_used}', Stiva_citita: '{stack_used}'] {current_state} -> {next_state} | POP '{popped_val}' | PUSH '{push_symbols}' | Stiva: {stack}")

        current_state = next_state

        # avansam indexul literei doar daca chiar am consumat-o tura asta
        if consumed_input:
            i += 1

            # masura de siguranta: daca a picat in trap state (q3) si doar ruleaza in gol, il oprim noi fortat
        if current_state == 'q3' and sym_used == 'e' and stack_used == 'e':
            print(f"   [!] Automatul a blocat executia in starea de esec (q3).")
            break

    # conditia de victorie: am terminat literele si am ajuns unde trebuie
    is_accepted = (i == len(word) and current_state in dpda['accept_states'])

    if is_accepted:
        print(f"=> REZULTAT: ACCEPTAT (S-a oprit corect in {current_state})")
    else:
        print(f"=> REZULTAT: RESPINS (S-a oprit in {current_state})")

    return is_accepted


# RULARE
# incarcam dpda ul din fisier
my_dpda = parse_dpda_file('limbaj_dpda.txt')

# testam niste cazuri ca sa fim siguri ca numara bine 0^k 1^k
simulate_dpda(my_dpda, "0011")  # Corect -> Acceptat
simulate_dpda(my_dpda, "000111")  # Corect -> Acceptat
simulate_dpda(my_dpda, "0101")  # Intercalat -> Respins (se duce in q3)
simulate_dpda(my_dpda, "10")  # Incepe cu 1 -> Respins (se duce in q3)
simulate_dpda(my_dpda, "001")  # Mai multi de 0 -> Respins
simulate_dpda(my_dpda, "011")  # Mai multi de 1 -> Respins