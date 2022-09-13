
## **REQUISITI**

Per poter utilizzare **WIKIFILM** è necessario installare i moduli Python necessari

1. Aprire una nuova finestra terminale
2. Entrare nella cartella del progetto
3. Lanciare i comandi di seguito elencati in base al proprio sistema operativo

## *Windows* :

Lanciare il seguente comando:


python -m pip install -r requirements.txt


## **ESECUZIONE**

Dopo aver installato i requisiti per avviare **WIKIFILM**, rimanendo all'interno della cartella del progetto

Per lanciare l'applicazione basta semplicemente inserire

## *Windows*:


python wikiFilm.py

Successivamente copiare ed incollare il seguente URL `https://127.0.0.1:5000/` su Google Chrome.

## **SCRAPING**

lanciare il comando:


python3 estrazione_link.py

ed attendere il completamento che richiede all'incirca dalle 2 alle 4 ore

## **INDEXING**

Se si vuole re-indicizzare i documenti 

Lanciare il seguente comando:

python3 indexing.py


# **INTRODUZIONE E COME UTILIZZARE**

**WIKIFILM** è un motore di ricerca basato sui film,  raggruppa all'incirca 8.000 documenti contenenti titolo, riassunto della trama, data di uscita ,il direttore, i generi e il link per raggiungere la pagina. 

## **LINGUAGGIO PER FORMULARE QUERY**

Nella barra di ricerca è possibile specificare:
* queries in lingua inglese usando testo libero,
* operatori booleani e per concetti
* Di default la ricerca viene effettuata in OR
    * Per cercare una frase ed evitare che le parole vengano messe in OR bisogna specificare la frase tra virgolette
* In caso di meno di 10 risultati verranno proposte delle parole simili a quella/e digitate per aiutare nella ricerca

>ESEMPI 
>
>query testo libero: Spider-Man
>
>query per cercare una frase: "Hulk"
>
>
>query per concetti: {heroes,RT}

Il thesaurus adottato è wordnet
* La sintassi per una query è **{term, relationship-type}**
* Possono essere specificati tre tipi di relazioni:
    * BT: broader term
    * NT: narrower term
    * RT: related term

## **Contatti**

* 242802@studenti.unimore.it - Filippo Principato
* 246016@studenti.unimore.it - Jihed Fatnassi