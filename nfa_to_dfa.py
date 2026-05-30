# 1. parsarea nfa-ului (acelasi cod de la simulator ca sa citim datele de baza)
def load_nfa(filename):
    nfa = {'alphabet': set(), 'states': set(), 'start': '', 'accept': set(), 'trans': {}}
    with open(filename, 'r') as f:
        is_trans = False
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue

            if line.startswith('ALPHABET:'):
                nfa['alphabet'] = {x.strip() for x in line.split(':')[1].split(',')}
            elif line.startswith('STATES:'):
                nfa['states'] = {x.strip() for x in line.split(':')[1].split(',')}
            elif line.startswith('START:'):
                nfa['start'] = line.split(':')[1].strip()
            elif line.startswith('FINALS:'):
                nfa['accept'] = {x.strip() for x in line.split(':')[1].split(',')}
            elif line.startswith('TRANSITIONS:'):
                is_trans = True
            elif is_trans:
                left, right = line.split('->')
                st, sym = [x.strip() for x in left.split(',')]
                next_sts = {x.strip() for x in right.split(',')}
                if st not in nfa['trans']: nfa['trans'][st] = {}
                nfa['trans'][st][sym] = next_sts
    return nfa


# 2. functia de inchidere epsilon (epsilon closure)
# asta gaseste toate starile in care putem ajunge "gratuit" (fara sa citim litere) dintr o stare data
def get_e_closure(states, nfa_trans):
    closure = set(states)
    stack = list(states)  # folosim o stiva ca sa exploram in adancime (dfs)

    while stack:
        current = stack.pop()
        # daca din starea curenta avem sageti 'e'
        if current in nfa_trans and 'e' in nfa_trans[current]:
            for next_st in nfa_trans[current]['e']:
                if next_st not in closure:
                    closure.add(next_st)
                    stack.append(next_st)  # il bagam in stiva ca sa cautam mai departe si din el
    return closure


# o functie pt generarea numelor noilor super-stari
def get_state_name(state_set):
    # daca setul e gol, inseamna ca drumul a murit, deci mergem in trap state
    if not state_set: return "TRAP"
    # sortam alfabetic ca sa fim siguri ca {q1, q2} e mereu la fel cu {q2, q1}
    return "_".join(sorted(list(state_set)))


# 3. algoritmul powerset construction
def convert_nfa_to_dfa(nfa):
    print("\n--- INCEPEM CONVERSIA NFA -> DFA ---")

    # alfabetul dfa ului e acelasi, dar FARA epsilon ('e')
    dfa_alphabet = {sym for sym in nfa['alphabet'] if sym != 'e'}

    # starea de start din dfa e inchiderea epsilon a starii de start din nfa
    start_closure = get_e_closure({nfa['start']}, nfa['trans'])
    dfa_start_name = get_state_name(start_closure)

    # coada cu stari noi pe care inca nu le-am explorat
    unprocessed = [start_closure]
    # dictionar ca sa tinem minte ce am procesat deja (nume -> set de stari nfa)
    processed_dict = {}

    dfa_transitions = {}
    dfa_accept_states = set()

    # cat timp mai avem super-stari de explorat
    while unprocessed:
        curr_set = unprocessed.pop(0)
        curr_name = get_state_name(curr_set)

        # daca am mai trecut pe aici, sarim
        if curr_name in processed_dict: continue

        processed_dict[curr_name] = curr_set
        dfa_transitions[curr_name] = {}

        print(f"Explorez super-starea: {curr_name}")

        # vedem daca starea asta noua contine vreo stare finala din nfa ul vechi
        if any(st in nfa['accept'] for st in curr_set):
            dfa_accept_states.add(curr_name)

        # luam fiecare litera din alfabet ca sa vedem unde ne duce
        for sym in dfa_alphabet:
            next_nfa_states = set()

            # strangem toate destinatiile de la toate "clonele" din setul curent
            for nfa_st in curr_set:
                if nfa_st in nfa['trans'] and sym in nfa['trans'][nfa_st]:
                    next_nfa_states.update(nfa['trans'][nfa_st][sym])

            # aplicam iar inchiderea epsilon ca sa luam si tranzitiile gratuite de dupa mutare
            next_dfa_set = get_e_closure(next_nfa_states, nfa['trans'])
            next_name = get_state_name(next_dfa_set)

            # mapam sageata pt noul dfa
            dfa_transitions[curr_name][sym] = next_name

            # daca am dat de o super-stare complet noua, o bagam la rand
            if next_name not in processed_dict and next_dfa_set not in unprocessed:
                if next_name != "TRAP":  # trap-ul il tratam separat mai jos
                    unprocessed.append(next_dfa_set)

    # adaugam starea TRAP daca a fost folosita undeva, ca sa fie DFA complet
    trap_used = any("TRAP" in dest.values() for dest in dfa_transitions.values())
    if trap_used:
        dfa_transitions["TRAP"] = {sym: "TRAP" for sym in dfa_alphabet}
        print("Explorez super-starea: TRAP")

    # ambalam totul in structura noastra clasica
    dfa = {
        'alphabet': dfa_alphabet,
        'states': set(dfa_transitions.keys()),
        'start': dfa_start_name,
        'accept': dfa_accept_states,
        'trans': dfa_transitions
    }

    print("=> CONVERSIE TERMINATA CU SUCCES!\n")
    return dfa


# 4. salvarea in fisier
def save_dfa(dfa, filename="limbaj_dfa_generat.txt"):
    with open(filename, 'w') as f:
        f.write(f"ALPHABET: {', '.join(sorted(dfa['alphabet']))}\n")
        f.write(f"STATES: {', '.join(sorted(dfa['states']))}\n")
        f.write(f"START: {dfa['start']}\n")
        f.write(f"FINALS: {', '.join(sorted(dfa['accept']))}\n")
        f.write("\nTRANSITIONS:\n")

        for st in sorted(dfa['states']):
            for sym, next_st in dfa['trans'][st].items():
                f.write(f"{st}, {sym} -> {next_st}\n")


# RULARE
if __name__ == "__main__":
    # convertim nfa-ul generat anterior din regex in dfa perfect determinist
    my_nfa = load_nfa("limbaj_nfa.txt")
    my_dfa = convert_nfa_to_dfa(my_nfa)
    save_dfa(my_dfa)