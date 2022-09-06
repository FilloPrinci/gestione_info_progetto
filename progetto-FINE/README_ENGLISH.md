![Movienet Logo](/static/img/Logofinale.png)

## **ADVICE**

For the right functioning of the program you need to have [**python3**](https://www.python.org/downloads/) and [**Google Chrome**](https://www.google.it/intl/it/chrome/) installed on your pc

## **REQUIREMENTS**

In order to use **MOVIENET** you need to install the necessary Python modules

1. Open a new terminal window
2. Go to the project folder 
3. Launch the commands listed below according to your operating system

## *Windows* :

Launch the following command:

```bash
python -m pip install -r requirements.txt
```

## *Linux* :

Launch the following commands:

```bash
python3 -m pip install -r requirements.txt
sudo apt install python3-flask
```

## *macOS* :

Launch the following command:

```bash
python3 -m pip install -r requirements.txt
```

## **EXECUTION**

After installing the requirements to launch **MOVIENET**, staying inside the project folder

To launch the application simply enter:

## *Windows*:

The following command:

```bash
.\start.bat
```

## *Linux*:

The following command:

```bash
bash start.sh
```

## *macOS*:

The following command:

```bash
bash start_mac.sh
```
### *`TIP OF`* :

In case of malfunction of the automation process, launch the following command:

## *Windows*:

```bash
python app.py
```

## *Linux*/macOS: 

```bash
python3 app.py
```

Then copy and paste the following URL `https://127.0.0.1:5000/` on Google Chrome and that's it!

## **SCRAPING**

If you want to perform the scraping you need to identify the user agent suitable for your operating system and the version of your Google Chrome and insert it in the `estrazione_link.py` file on line 25

![GitHub Logo](/HDR.png)

>[**Click here to identify the suitable user agent**](https://developers.whatismybrowser.com/useragents/explore/)

Then launch the command:

```bash
python3 estrazione_link.py
```
and waiting for the completion which takes approximately thath 4 to 6 hour

`ATTENTION: at the moment due to down of the filmsomniac.com site it is not possible to carry out the scraping phase of the latter`

## **INDEXING**

If you want to re-index the document

Launch the following command:

```bash
python3 indexing.py
```

# **INTRODUCTION AND HOW TO USE**

**MOVIENET** is a search engine based on film, it groups approximately 10.000 documents that contain title, relase date, plot summary, genre(s), director and the link to reach the reference page

Once the application has been launched, the search bar is in the foreground on the home page with an advanced button underneath with which access to the advanced search where is possible to set filters to queries

## **LANGUAGE FOR FORMULATING QUERY**

In the search bar is possible to specify queries in english language using free text, boolean operators and for concept
* By default the search is performed in OR
    * To search for a phrase and avoid that the words are set in OR you need to specify the phrase in quotation marks 
* In case of less than 10 results, words similar to the one(s) typed will be proposed to help in the search

>EXEMPLES 
>
>free text query: avenger
>
>query for find a phrase: "Harry Potter"
>
>query with booleans operators: "The lord of the ring" AND "Peter Jackson"
>
>query for concept: {heroes,RT}

The thesaurus adopted is wordnet
* The syntax for a query is **{term, relationship-type}**
* Can be specify three relationship-type:
    * BT: broader term
    * NT: narrower term
    * RT: related term

## **FILTERS**

In the advanced search as mentioned previously is possible to set filters and much more:

* Set a filter for the date
    * By specifying via the calendar
        * Both parameters "Da" and "A"
        * Just one of the two parameters
* Set a filter for the director
* Set a filter for the genre
* Choose the maximum number of results to show
    * Having a range that goes from min 1 to max 100
* Set a filter for the source
    * More than one source can be selected at the same time
* Use the top bar to automatically formulate AND and OR queries

## **SUPPORT**

For each problem use the following contacts:
* 243470@studenti.unimore.it - Davis Innangi
* 243895@studenti.unimore.it - Enzo Rotonda