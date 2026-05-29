import random

# CITIREA GRAMATICII DIN FISIER
def load_grm(fname):
    # grm e dictionarul de baza
    grm = {'start': '', 'rules': {}}

    with open(fname, 'r') as f:
        is_rules_section = False

        for line in f:
            line = line.strip()
            if not line or line[0] == '#':
                continue  # Ignoram comentariile si liniile goale

            if line.startswith('START:'):
                grm['start'] = line.split(':')[1].strip()
            elif line.startswith('RULES:'):
                is_rules_section = True
            elif is_rules_section:
                # parsam linia de tipul "S -> 0S1"
                lhs, rhs = line.split('->')
                lhs = lhs.strip()  # Left Hand Side (ex: S)
                rhs = rhs.strip()  # Right Hand Side (ex: 0S1 sau e)

                # daca nu exista litera in dictionar ii facem o lista
                if lhs not in grm['rules']:
                    grm['rules'][lhs] = []

                grm['rules'][lhs].append(rhs)

    return grm

# 2. GENERATORUL DE CUVINTE (FABRICA)
def gen_word(grm, max_steps=20):
    # curr = cuvantul in starea curenta
    curr = grm['start']

    # tinem minte pasii
    traseu = [curr]

    step = 0
    # cat timp avem litere mari in cuvant continuam sa inlocuim
    while any(c.isupper() for c in curr) and step < max_steps:
        step += 1

        # aautam prima litera mare din cuvant
        for i, char in enumerate(curr):
            if char.isupper():
                c = char  # litera mare gasita

                # alegem random o regula disponibila pentru aceasta litera
                regula_aleasa = random.choice(grm['rules'][c])

                # daca regula e 'e' o inlocuim cu nimic
                if regula_aleasa == 'e':
                    regula_aleasa = ''

                # inlocuim litera gasita cu regula aleasa
                curr = curr[:i] + regula_aleasa + curr[i + 1:]

                # salvam pasul
                traseu.append(curr if curr != '' else 'e')
                break  # iesim din for ca sa o luam de la capat cu noul cuvant

    if step == max_steps:
        return "Gramatica face prea multi pasi", traseu

    return curr, traseu

# 3. RULAREA SCRIPTULUI
if __name__ == "__main__":
    my_grm = load_grm("gramatica.txt")
    print(f"Start={my_grm['start']}, Reguli={my_grm['rules']}\n")

    # generam 5 cuvinte diferite
    for i in range(5):
        cuvant_final, istoric = gen_word(my_grm)
        istoric_formatat = " \u21D2 ".join(istoric)  # \u21D2 e sageata dubla (=>)

        print(f"Test {i + 1}: {istoric_formatat}")