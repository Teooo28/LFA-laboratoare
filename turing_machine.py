# 1. PARSAREA FISIERULUI
def parse_tm_file(filename):
    # Acelasi tip de dictionar ca la DFA/DPDA, doar ca adaugam 'blank' (simbolul gol)
    tm = {'states': set(), 'start': '', 'accept': set(), 'blank': '#', 'trans': {}}

    with open(filename, 'r') as f:
        is_trans = False
        for line in f:
            line = line.strip()
            # Ignoram liniile goale sau cele care incep cu # (comentarii in fisierul text)
            if not line or line.startswith('#'): continue

            # Citim datele de baza
            if line.startswith('STATES:'):
                tm['states'] = {x.strip() for x in line.split(':')[1].split(',')}
            elif line.startswith('START:'):
                tm['start'] = line.split(':')[1].strip()
            elif line.startswith('FINALS:'):
                tm['accept'] = {x.strip() for x in line.split(':')[1].split(',')}
            elif line.startswith('BLANK:'):
                tm['blank'] = line.split(':')[1].strip()
            elif line.startswith('TRANSITIONS:'):
                is_trans = True
            elif is_trans:
                # Parsam linia de tranzitie. Ex: q0, 0 -> q0, 1, R
                # Stanga sagetii: ce stiu acum. Dreapta: ce fac mai departe.
                left, right = line.split('->')
                curr_st, read_sym = [x.strip() for x in left.split(',')]
                next_st, write_sym, move_dir = [x.strip() for x in right.split(',')]

                # Initializam dictionarul pentru starea curenta daca nu exista
                if curr_st not in tm['trans']: tm['trans'][curr_st] = {}

                # Salvam instructiunea completa (Stare_Noua, Simbol_de_scris, Directia_R_sau_L)
                tm['trans'][curr_st][read_sym] = (next_st, write_sym, move_dir)

    return tm

# 2. SIMULAREA BENZII INFINITE (Magia Turing)
def run_turing_machine(tm, input_word):
    state = tm['start']
    blank = tm['blank']

    # punem cuvantul intr-o lista si lipim 5 blank-uri (#) in stanga si 5 in dreapta.
    # Daca masina iese din spatiul asta, mai adaugam blank-uri pe parcurs
    tape = [blank] * 5 + list(input_word) + [blank] * 5

    # indexul 5 este exact unde incepe prima litera a cuvantului
    head = 5

    print(f"\n{'=' * 40}")
    print(f"PORNIM MASINA TURING | Input: '{input_word}'")
    print(f"{'=' * 40}\n")

    step = 0
    # Masina Turing ruleaza INCONTINUU pana ajunge intr-o stare de 'accept'
    while state not in tm['accept']:
        step += 1
        curr_sym = tape[head]  # Citim ce se afla pe banda sub capul de citire

        # PARTEA DE VIZUALIZARE (Printam banda pe ecran la fiecare pas)
        vizualizare_banda = ""
        for i, char in enumerate(tape):
            if i == head:
                vizualizare_banda += f"[{char}]"  # Evidentiem pozitia curenta
            else:
                vizualizare_banda += f" {char} "

        print(f"Pas {step:02d} | Stare: {state} | Banda: {vizualizare_banda}")

        # EXECUTAM TRANZITIA
        # Verificam daca masina stie ce sa faca cand e in starea 'state' si citeste 'curr_sym'
        if state in tm['trans'] and curr_sym in tm['trans'][state]:
            next_st, write_sym, move_dir = tm['trans'][state][curr_sym]

            # 1. SCRIEM pe banda simbolul nou
            tape[head] = write_sym

            # 2. SCHIMBAM starea
            state = next_st

            # 3. MUTAM capul de citire (R = dreapta, L = stanga)
            if move_dir == 'R':
                head += 1
            elif move_dir == 'L':
                head -= 1

            # ASIGURAM "INFINITATEA" BENZII
            # Daca capul se duce prea mult in dreapta si iese din lista, adaugam un blank
            if head >= len(tape):
                tape.append(blank)
            # Daca se duce prea mult in stanga si iese din indexul 0, adaugam un blank in fata
            if head < 0:
                tape.insert(0, blank)
                head = 0  # Capul ramane pe pozitia 0 (care e noul blank tocmai adaugat)

        else:
            # Daca nu exista o sageata desenata pentru situatia asta, masina pica
            print(f"\n[!] CRASH: Masina s-a blocat in starea '{state}' citind simbolul '{curr_sym}'.")
            return False

    # Daca a iesit din while, inseamna ca a dat de starea de acceptare
    print(f"\n=> SUCCES! Masina s-a oprit corect in starea de acceptare '{state}'.")

    # Curatam banda de blank-uri ca sa ii afisam doar rezultatul calculat
    rezultat_final = "".join(tape).replace(blank, "")
    print(f"=> REZULTAT FINAL PE BANDA: {rezultat_final}")
    return True

# 3. RULARE TEST
if __name__ == "__main__":
    # Incarcam instructiunile (ex: inversarea bitilor)
    my_tm = parse_tm_file("limbaj_turing.txt")

    # Rulam cuvantul
    run_turing_machine(my_tm, "10110")