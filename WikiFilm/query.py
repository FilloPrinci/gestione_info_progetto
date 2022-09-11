from whoosh.qparser import MultifieldParser, OrGroup, QueryParser, WildcardPlugin
from whoosh.qparser.dateparse import DateParserPlugin
from whoosh.index import open_dir
from whoosh.query import Variations
from whoosh import scoring, sorting
import os.path
import re
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import nltk
nltk.download("wordnet")
from nltk.corpus import wordnet

# Funzione filtro che seleziona la sorgente delle informazioni 
def source_filter(query, ix):
    
    # Parserizzo solo i link
    qparser = QueryParser("Fpath", ix.schema)
    # Utilizzo il WildcardPlugin per metchare le sorgenti nei link
    qparser.add_plugin(WildcardPlugin()) 

    imdb = ""
    themovie = ""


    # Se l'utente seleziona IMDB imposto la variabile imdb a contenere tutti i link che contengono www.imdb.com
    if query['imdb']:  # if the user wants articles from ESA
        imdb = "*www.imdb.com*"

    # Se l'utente seleziona THE MOVIE imposto la variabile themovie a contenere tutti i link che contengono www.themovie.org
    if query['themovie']:
        themovie = "*www.themoviedb.org*"

   

    # Se non viene fatta alcuna scelta imposto tutte e tre le sorgenti di default 
    if (not query['imdb']) and (not query['themovie']):
        return qparser.parse("*www.imdb.com* OR *www.themoviedb.org* ")    
    # Altrimenti parserizzo in OR le sorgenti scelte
    else:
        return qparser.parse(f"({imdb} OR {themovie}) ")

# Funzione filtro che seleziona il regista
def director_filter(query, ix):
    
    # Parserizzo solo i direttori
    qparser = QueryParser("Cdirector", ix.schema)

    # Recupero il direttore dal campo della gui
    director = query['director']

    # Se director contiene None o è una stringa vuota imposto director a None
    if director is None or director == '':
        return None   
    # Altrimenti parserizzo in AND il direttore
    else:
        return qparser.parse(f"({director}")

# Funzione filtro che seleziona il genere
def genre_filter(query, ix):
    
    # Parserizzo solo i generi
    qparser = QueryParser("Dgenre", ix.schema)

    # Recupero il genere dal campo della gui
    genre = query['genres']

    # Se genre contiene None o è una stringa vuota imposto genre a None
    if genre is None or genre == '':
        return None   
    # Altrimenti parserizzo in AND il genere
    else:
        return qparser.parse(f"({genre}")

# Funzione filtro che seleziona la data o un range di date
def date_filter(query):

    # Modifico le date dal formato YYYY-MM-DD al formato YYYYMMDD(senza spazi)
    from_date = str.replace(query['from'], '-', '')
    to_date = str.replace(query['to'], '-', '')

    # Inizializzo il range con le date recuperate dalla gui
    date_range = f"date:[{from_date} to {to_date}]"

    # Se è settata solo la data di fine imposto data_range a "to to_date"
    if not from_date and to_date is not None:
        date_range = f"date:[to {to_date}]"
    # Altrimenti se è settata solo la data di inizio imposto data_range a "from_date to today"
    elif from_date is not None and not to_date:  # if just the ending date is unset
        date_range = f"date:[{from_date} to today]"

    return date_range

# Funzione che risolve la query restituendo i risultati 
def my_query(query, count):

    # Apro l'index
    root = os.path.abspath(os.curdir)
    ix = open_dir(root + r'/indexdir')

    # Creo un parser su più campi (titolo e contenuto) raggruppati in OR e con la ricerca automatica sulla variazione morfologica delle parole
    qp = MultifieldParser(["Atitle","Bcontent","Cdirector","Dgenre"],schema=ix.schema,group=OrGroup,termclass=Variations)
    
    # Aggiungo il pluggin per il parsing della data
    qp.add_plugin(DateParserPlugin(free=True))

    # Recupero il filtro delle sorgenti da passare alla query
    sources = source_filter(query, ix)

    #Recupero il filtro del regista da passare alla query
    director = director_filter(query, ix)

    #Recupero il filtro del genere da passare alla query
    genre = genre_filter(query, ix)
    
    # Recupero la query dalla gui
    query_text = query['text']

    # Controllo se è una query per concetti
    query_text = concept_query(query_text)

    # Se non abbiamo impostato una data imposto il range a None
    if query['from'] is None or query['from'] == '' and query['to'] == '':
        date_range = None
    # Altrimenti chiamo il filtro e aggiungo la ricerca per data (in AND)
    else:
        date_range = date_filter(query)
        query_text += " AND " + date_range
    
    # Se non imposto nessun parametro mi ritorna una lista di dizionari vuota (Controllo utile per advanced)
    if query_text == "" and director is None and query['imdb'] is None and query['themovie'] is None and date_range is None and genre is None:
        return [{}],0 

    # Se abbiamo settato un regista aggiungo la ricerca per regista (in AND)   
    if director is not None:
        query_text = "(" + query_text + ") AND " + str(director)

    # Se abbiamo settato un genere aggiungo la ricerca per genere (in AND)   
    if genre is not None:
        query_text = "(" + query_text + ") AND " + str(genre)

    print("our query " + query_text)

    # Parserizzo la query
    q = qp.parse(query_text)
    print("parsed query " + str(q))

    # Se ho settato una data o un range di date ordino i risultati prima per data e poi per score
    if date_range is not None:
        return search(ix,sources,q,count,True)
    # Altrimenti ordino i risultati per score
    else:
        return search(ix,sources,q,count,False)

# Funzione che restituisce i risultati
def search(ix,sources,q,count,bool):
    lista = []
    lunghezza = 0

    # Variabile per fare il sorting sugli score
    scores = sorting.ScoreFacet()

    # Variabile per fare il sorting sulla data
    date = sorting.FieldFacet("date")

    # Se ho settato la data il filtro sarà per data e per score
    if bool:
        lista_sort = [date,scores]
    else:
        lista_sort = [scores]

    # Cerco i match, li aggiungo per chiave ad un dizionario, e poi aggiungo il dizionario a una lista per poi ritornarla alla gui
    with ix.searcher(weighting=scoring.BM25F()) as searcher:
        results = searcher.search(q, limit=count, filter=sources, terms=True, sortedby=lista_sort)
        results.fragmenter.charlimit = None
        results.fragmenter.maxchars = 300
        results.fragmenter.surround = 10000
        lunghezza = len(results)
        for result in results:
            dicto = {}
            for f in result.fields():
                if f == "date":
                    data =  result[f]
                    data = data.date()
                    dicto.update({f"{f}":data})
                else:
                    dicto.update({f"{f}":result[f]})
            dicto["Contenthighlights"] = result.highlights("Bcontent")
            dicto["Titlehighlights"] = result.highlights("Atitle")
            dicto["Directorhighlights"] = result.highlights("Cdirector")
            lista.append(dicto)
    return lista,lunghezza

# Funzione che implementa il dym
def expansion_query(querys):
    synonyms = []
    
    querys = querys.replace("OR", '')
    querys = querys.split()

    for query in querys:
        s = wordnet.synsets(query)

        for syn in wordnet.synsets(query):
            for l in syn.lemmas():
                synonyms.append(l.name())
    return list(set(synonyms))

# Funzione che elabora le query per concetti
def concept_query(query):
    exp = re.compile("\{.*?\}")  # R.E. da cercare

    for e in exp.findall(query):  # cerco tutti i match con la mia R.E.
        e = e.replace("{", '')
        e = e.replace("}", '')
        e = e.split(",")
        final_string = ""
        expansion = []
        try:    # Se non ci sono errori controllo nel thesaurus altrimenti skippo
            term = e[0]
            rel = e[1].upper()
            
        except IndexError:
            term = ""
            rel = ""
        
        for s in wordnet.synsets(term):
            if rel == "BT":                     # Broader term (termine più generale)
                for hyp in s.hypernyms():
                    for lemma in hyp.lemmas():
                        expansion.append(lemma.name())
                
            if rel == "NT":                     # Narrower term (termine più specifico)
                for hyp in s.hyponyms():
                    for lemma in hyp.lemmas():
                        expansion.append(lemma.name())

            if rel == "RT":                     # Related term (termine correlato)
                for lemma in s.lemmas():
                    expansion.append(lemma.name())

        for exp in set(expansion):
            final_string += '"' + exp + '" '
        
        query = query.replace("{" + term + "," + e[1] + "}","(" + final_string + ")")  # Sostituisce il termine e la relazione con i concetti
    return query

if __name__ == '__main__':
    my_query()