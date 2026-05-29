# Laboratoare LFA (Limbaje Formale și Automate) 🚀

Acest repository conține proiectele și implementările realizate pentru laboratorul de Limbaje Formale și Automate. Toate scripturile sunt scrise în Python și se bazează pe algoritmi standard din teoria automatelor, fără a folosi biblioteci externe complexe.

## 📌 Structura Proiectelor

### 1. Simulator DFA (Automat Finit Determinist)
Program care verifică dacă un cuvânt aparține unui limbaj dat.
* **Cum funcționează:** Citește cuvântul literă cu literă. Pentru fiecare stare și caracter citit, există o singură acțiune permisă. Execuția urmează un singur traseu strict și acceptă cuvântul doar dacă la finalizarea citirii se află într-o stare finală.

### 2. Simulator NFA (Automat Finit Nedeterminist)
O versiune extinsă a DFA-ului, capabilă să gestioneze ambiguități.
* **Cum funcționează:** Permite mai multe tranziții pentru același caracter și poate schimba starea fără a citi litere de pe bandă (epsilon-tranziții). Execuția explorează toate traseele posibile simultan. Cuvântul este acceptat dacă cel puțin unul dintre aceste trasee ajunge într-o stare finală.

### 3. Simulator DPDA (Deterministic Pushdown Automaton)
O evoluție a DFA-ului, capabilă să rețină date folosind o memorie de tip stivă. 
* **Caracteristici:** Implementează prioritizarea riguroasă a tranzițiilor gratuite (epsilon-tranziții pe bandă și/sau stivă) pentru a menține determinismul. 
* **Logica:** Include gestionarea stărilor de eroare (trap states) și curățarea stivei la final. Testat pe recunoașterea limbajelor care necesită numărare (ex: prelucrarea de tip `0^k 1^k` sau paranteze echilibrate).

### 4. Convertor Regex în NFA (Algoritmul lui Thompson)
Un compilator de expresii regulate care transformă matematic un string într-un automat NFA.
* **Mecanism:** 1. Adaugă explicit operatorii de concatenare (`.`).
  2. Convertește expresia din forma Infixată în forma Postfixată folosind algoritmul **Shunting Yard**.
  3. Aplică **Algoritmul lui Thompson** pentru a asambla NFA-ul din blocuri de bază (litere, reuniune `|`, concatenare `.`, și Kleene Star `*`).
* **Output:** Automatul generat este salvat automat într-un fișier text valid (ce poate fi citit direct de simulatorul NFA de la punctul 2).

### 5. Generator de Gramatici (Derivare Stângă)
Un script care generează cuvinte pe baza unui set de reguli de producție de tipul `S -> 0S1 | e`.
* **Cum funcționează:** Aplică o derivare de stânga (Leftmost Derivation). Caută mereu primul neterminal (litera mare) și îl înlocuiește alegând aleator o regulă validă. Afișează în consolă tot traseul cuvântului, pas cu pas (ex: `S ⇒ 0S1 ⇒ 00S11 ⇒ 0011`).

### 6. Simulator Mașină Turing (Turing Machine) 🏆
Implementarea completă a celui mai puternic model teoretic de calcul.
* **Cum funcționează:** Simulează o bandă infinită prin extinderea dinamică a listei în memorie, ori de câte ori capul de citire atinge marginile. Spre deosebire de automatele clasice, capul de citire se poate deplasa în ambele direcții (Stânga/Dreapta) și poate suprascrie datele existente.
* **Vizualizare:** Include o afișare animată în consolă, evidențiind mișcarea capului de citire/scriere (`[ ]`) pe bandă în timp real.

---

## 🛠️ Cum se rulează codul

Asigurați-vă că aveți [Python 3.x](https://www.python.org/) instalat pe sistem.
Nu sunt necesare dependențe externe (`pip install`). 

Fiecare script poate fi rulat independent din terminal. Exemple:

```bash
python dpda_simulator.py
python regex_to_nfa.py
python generator_gramatici.py
python turing_machine.py
