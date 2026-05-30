# Laboratoare LFA (Limbaje Formale și Automate) 🚀

Acest repository conține proiectele realizate pentru laboratorul de Limbaje Formale și Automate. Codul este scris în Python și urmărește implementarea conceptelor de bază ale materiei: generarea cuvintelor (Gramatici), expresiile regulate (Regex) și validarea acestora prin diverse modele de calcul (Automate și Mașina Turing).

## 📌 Structura Proiectelor și Logica Algoritmilor

### 1. Simulator DFA (Automat Finit Determinist)
Verifică apartenența unui cuvânt la un limbaj folosind un automat cu un singur drum de execuție.
* **Logica:** Pentru fiecare stare și literă citită, există o singură tranziție posibilă. 
* **Mecanism:** Programul parcurge cuvântul literă cu literă. Dacă se întâlnește un simbol care nu este în alfabet sau pentru care nu există o tranziție definită, execuția se oprește, iar cuvântul este respins. Acceptarea are loc doar dacă întregul cuvânt a fost citit, iar automatul s-a oprit într-o stare finală.

### 2. Simulator NFA (Automat Finit Nedeterminist)
Un model care poate explora mai multe căi de execuție simultan și care acceptă tranziții spontane ($\epsilon$-tranziții).
* **Logica:** În loc să mențină o singură stare curentă, algoritmul folosește un set de stări active, simulând astfel parcurgerea tuturor rutelor valide în paralel.
* **Mecanism:** La fiecare pas, setul de stări se actualizează pe baza destinațiilor posibile pentru simbolul citit. La finalul cuvântului, se realizează intersecția dintre setul stărilor active și mulțimea stărilor finale. Dacă intersecția nu este vidă, înseamnă că cel puțin o ramură a ajuns la succes, iar cuvântul este acceptat.

### 3. Simulator DPDA (Deterministic Pushdown Automaton)
Un automat determinist extins cu o memorie de tip stivă (LIFO), necesar pentru recunoașterea limbajelor independente de context (ex: `0^k 1^k`).
* **Logica:** Utilizarea stivei permite automatului să „numere” caractere, adăugând sau extrăgând simboluri în funcție de regulile definite.
* **Mecanism:** Pentru a păstra determinismul în prezența tranzițiilor $\epsilon$, codul implementează un sistem de priorități strict. Tranzițiile care consumă o literă de pe bandă și interacționează cu stiva sunt evaluate primele, în timp ce mutările complet în gol (fără citire de pe bandă) sunt ultimele. Lipsa unei tranziții valide forțează automatul să se oprească sau să intre într-o stare de eroare (trap state).

### 4. Convertor Regex în NFA (Algoritmul lui Thompson)
Transformă o expresie regulată într-un graf orientat capabil să evalueze cuvinte.
* **Logica:** Orice expresie regulată poate fi descompusă în operații elementare (Litere, Reuniune, Concatenare, Kleene Star), fiecare corespunzând unui șablon NFA specific.
* **Mecanism:** Expresia este prelucrată mai întâi prin adăugarea explicită a operatorilor de concatenare (`.`). Ulterior, este convertită în forma postfixată prin algoritmul Shunting Yard pentru a elimina necesitatea parantezelor. Programul citește această formă cu ajutorul unei stive și asamblează automatul prin Algoritmul lui Thompson, legând sub-grafurile exclusiv prin $\epsilon$-tranziții. Rezultatul este exportat într-un format text standardizat.

### 5. Simulator Mașină Turing (Turing Machine) 🏆
Un model teoretic avansat, capabil să se deplaseze bidirecțional pe o bandă și să rescrie informația.
* **Logica:** Spre deosebire de automatele clasice, capul de citire/scriere își poate schimba direcția și poate modifica simbolurile existente, simulând memoria unui calculator real.
* **Mecanism:** Deoarece memoria fizică nu permite o listă cu adevărat infinită, banda este implementată ca o structură de date marginită inițial de simboluri goale (`#`). Dacă pointer-ul de citire atinge oricare dintre limite, lista este extinsă dinamic (`insert` sau `append`) doar atât cât este necesar. Rularea include o afișare vizuală în consolă pentru a urmări deplasarea capului de citire în timp real.

### 6. Convertor NFA în DFA (Powerset Construction) 💎
Elimină nedeterminismul dintr-un NFA, transformându-l într-un DFA echivalent matematic.
* **Logica:** Toate stările paralele în care se poate afla un NFA la un moment dat sunt grupate într-o singură „super-stare” pentru noul DFA (de ex: `q1_q2`).
* **Mecanism:** Se calculează mai întâi $\epsilon$-închiderile (folosind o parcurgere de tip DFS) pentru a găsi toate stările accesibile fără a consuma simboluri. Noile super-stări sunt procesate iterativ printr-o coadă, urmărind destinațiile posibile pentru fiecare literă din alfabet. Pentru a genera un DFA complet, rutele fără destinație sunt direcționate către o stare de eroare creată explicit (`TRAP`).

### 7. Generator de Gramatici (Derivare Stângă)
Generează cuvinte aparținând unui limbaj definit prin reguli de producție.
* **Logica:** Demonstrează funcția generativă a unui limbaj formal (spre deosebire de funcția de validare a automatelor), pornind de la o axiomă (litera de start) și înlocuind variabilele.
* **Mecanism:** Programul implementează o derivare de stânga (Leftmost Derivation). Parcurge șirul curent de la stânga la dreapta, identifică primul neterminal (variabila) și îl înlocuiește alegând aleator o regulă validă din fișier. Procesul se repetă până când șirul conține doar terminale (litere finale). Întregul traseu al derivării este reținut și afișat pas cu pas.
