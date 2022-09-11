
## **RACCOMANDAZIONI**

Per il corretto funzionamento del programma bisogna aver installato sul proprio pc [**python3**](https://www.python.org/downloads/) e [**Google Chrome**](https://www.google.it/intl/it/chrome/)

## **REQUISITI**

Per poter utilizzare **WIKIFILM** è necessario installare i moduli Python necessari

1. Aprire una nuova finestra terminale
2. Entrare nella cartella del progetto
3. Lanciare i comandi di seguito elencati in base al proprio sistema operativo

## *Windows* :

Lanciare il seguente comando:

```bash
python -m pip install -r requirements.txt
```

## **ESECUZIONE**

Dopo aver installato i requisiti per avviare **MOVIENET**, rimanendo all'interno della cartella del progetto

Per lanciare l'applicazione basta semplicemente inserire

## *Windows*:

Il seguente comando:

```bash
.\start.bat
```
### *`TIP OF`* :
In caso di mal funzionamento del processo di automazione lanciare il comando riportato di seguito:

## *Windows*:

```bash
python app.py
```

## *Linux*/macOS: 

```bash
python3 app.py
```

Successivamente copiare ed incollare il seguente URL `https://127.0.0.1:5000/` su Google Chrome.

## **SCRAPING**

Se si vuole eseguire lo scraping bisogna identificare lo user agent adatto al proprio sistema operativo e alla versione del proprio Google Chrome ed inserirlo nel file `estrazione_link.py` alla riga 25

![GitHub Logo](/HDR.png)

>[**Clicca qui per identificare lo user agent adatto**](https://developers.whatismybrowser.com/useragents/explore/)

Successivamente lanciare il comando:

```bash
python3 estrazione_link.py
```
ed attendere il completamento che richiede all'incirca dalle 4 alle 6 ore

## **INDEXING**

Se si vuole re-indicizzare i documenti 

Lanciare il seguente comando:

```bash
python3 indexing.py
```

# **INTRODUZIONE E COME UTILIZZARE**

**WIKIFILM** è un motore di ricerca basato sui film, esso raggruppa all'incirca 10.000 documenti contenenti titolo, data di uscita, riassunto della trama, il/i genere/i, il direttore ed il link per raggiungere la pagina di riferimento 

Una volta lanciata l'applicazione, nella home page si trova in primo piano la barra di ricerca con al di sotto un tasto advanced con cui accedere alla ricerca avanzata dove è possibile impostare dei filtri alle queries

## **LINGUAGGIO PER FORMULARE QUERY**

Nella barra di ricerca è possibile specificare queries in lingua inglese usando testo libero, operatori booleani e per concetti
* Di default la ricerca viene effettuata in OR
    * Per cercare una frase ed evitare che le parole vengano messe in OR bisogna specificare la frase tra virgolette
* In caso di meno di 10 risultati verranno proposte delle parole simili a quella/e digitate per aiutare nella ricerca

>ESEMPI 
>
>query testo libero: avenger
>
>query per cercare una frase: "Harry Potter"
>
>query che utilizza i booleani: "The lord of the ring" AND "Peter Jackson"
>
>query per concetti: {heroes,RT}

Il thesauro adottato è wordnet
* La sintassi per una query è **{term, relationship-type}**
* Possono essere specificati tre tipi di relazioni:
    * BT: broader term
    * NT: narrower term
    * RT: related term

## **FILTRI**

Nella ricerca avanzata come accennato precedentemente è possibile impostare filtri e molto altro:

* Impostare un filtro per la data
    * Specificando tramite il calendario
        * Entrambi i parametri "Da" e "A"
        * Solo uno dei due parametri
* Impostare un filtro per il direttore
* Impostare un filtro per il genere
* Scegliere il numero massimo di risultati da mostrare
    * Avendo un range che va da min 1 a max 100
* Impostare un filtro per la sorgente di riferimento
    * È possibile selezionare più di una sorgente contemporaneamente
* Utilizzare la barra superiore per formulare automaticamente query in AND e OR

## **SUPPORTO**

Per ogni problema utilizzare i seguenti contatti:
* 243470@studenti.unimore.it - Davis Innangi
* 243895@studenti.unimore.it - Enzo Rotonda