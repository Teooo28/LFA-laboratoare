# Laboratoare LFA (Limbaje Formale și Automate) 🚀

Acest repository conține proiectele și implementările realizate pentru laboratorul de Limbaje Formale și Automate. Toate scripturile sunt scrise în Python și se bazează pe algoritmi standard din teoria automatelor, fără a folosi biblioteci externe complexe.

## 📌 Structura Proiectelor

### 1. Simulatoare Automate Finite (DFA & NFA)
Program care parsează configurația unui automat dintr-un fișier text (`ALPHABET`, `STATES`, `TRANSITIONS` etc.) și simulează rularea unui cuvânt pas cu pas, verificând dacă este acceptat sau respins de limbaj.

### 2. Simulator DPDA (Deterministic Pushdown Automaton)
O evoluție a DFA-ului, capabilă să "numere" folosind o stivă. 
* **Caracteristici:** Implementează prioritizarea riguroasă a tranzițiilor gratuite (epsilon-tranziții pe bandă și/sau stivă) pentru a menține determinismul. 
* **Logica:** Include gestionarea stărilor de "trap" (eșec) și curățarea stivei la final. Testat pe recunoașterea limbajelor care necesită memorie (ex: prelucrarea de tip `0^k 1^k` sau paranteze echilibrate).

### 3. Convertor Regex în NFA (Algoritmul lui Thompson)
Un "compilator" de expresii regulate care transformă matematic un string într-un automat NFA.
* **Mecanism:**
  * 1. Adaugă explicit operatorii de concatenare (`.`).
  * 2. Convertește expresia din forma Infixată în forma Postfixată folosind algoritmul **Shunting Yard**.
  * 3. Aplică **Algoritmul lui Thompson** pentru a asambla NFA-ul din blocuri de bază (litere, reuniune `|`, concatenare `.`, și Kleene Star `*`).
* **Output:** Automatul generat este exportat automat într-un fișier text valid (ce poate fi citit direct de simulatorul NFA de la punctul 1).

### 4. Generator de Gramatici (Derivare Stângă)
Un script care "fabrică" cuvinte pe baza unui set de reguli de producție de tipul `S -> 0S1 | e`.
* Funcționează ca un generator de derivări de stânga (Leftmost Derivation).
* Selectează dinamic regulile și afișează în consolă tot traseul cuvântului, de la litera de start până la șirul final de terminale (ex: `S ⇒ 0S1 ⇒ 00S11 ⇒ 0011`).

---

## 🛠️ Cum se rulează codul

Asigurați-vă că aveți [Python 3.x](https://www.python.org/) instalat pe sistem.
Nu sunt necesare dependențe externe (`pip install`). 

Fiecare script poate fi rulat independent din terminal. Exemple:

```bash
python dpda_simulator.py
python regex_to_nfa.py
python generator_gramatici.py
