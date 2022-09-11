import requests
import re
import os
import json
from bs4 import BeautifulSoup
from string import punctuation
from dateutil.parser import parse
from timeit import default_timer as timer

# Creo la directory FilesJson nella directory progetto
root = os.path.abspath(os.curdir)
if not os.path.exists(root + r"/FilesJson"):
    os.mkdir(root + r"/FilesJson")

# Liste in cui inserirò i dati
title = []
year = []
storyline = []
genre = []
director = []
link_list = []

# User agent per richiedere le pagine web (da questo link è possibile scaricare
# lo user agent adatto al proprio sistema operativo https://developers.whatismybrowser.com/useragents/explore/)
hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}

# Funzione che inizializza le liste a vuote
def inizialize_list():
    del title[:]
    del year[:]
    del storyline[:]
    del genre[:]
    del director[:]
    del link_list[:]

# Funzione che crea un dizionario
def create_dictionary(title,year,storyline,genre,director,link_list):
    dictionary = {}
    
    i = 1
    for t, y, s, g, d, l in zip(title, year, storyline, genre, director, link_list):
        if t == None or y == None or not y or s == None or g == None or g == [] or d == None:
            pass
        else:
            nasted_dictionary = {}
            nasted_dictionary.update({"title":t})
            nasted_dictionary.update({"year":y})
            nasted_dictionary.update({"storyline":s})
            nasted_dictionary.update({"genre":g})
            nasted_dictionary.update({"director":d})
            nasted_dictionary.update({"link":l})
            dictionary.update({f"{i}":nasted_dictionary})
            i = i+1
    return dictionary

# Funzione che mi controlla se ci sono duplicati
def check_duplicate(tit,y,story,ge,di,l):
    if title.count(tit) == 0 or storyline.count(story) == 0:
        title.append(tit)
        year.append(y)
        genre.append(ge)
        storyline.append(story)
        director.append(di)
        link_list.append(l)

# Funzione che recupera le informazioni dal sito ibdm
def retrive_link_imdb():

    # Richiede la pagina Web
    r = requests.get('https://www.imdb.com/feature/genre/?ref_=nv_ch_gr')
    # Parser della pagina
    soup = BeautifulSoup(r.content, 'html.parser')

    # inizializzo le liste a essere vuote
    inizialize_list()
        
    # Recupero tutti i link delle categorie
    i = soup.find('div', {'class':'full-table'})
    for link in i.find_all('div', {'class':'table-row'}):
        link = link.find('a').get('href')
        link = 'https://www.imdb.com' + link

        page_genre = requests.get(link)
        soup2 = BeautifulSoup(page_genre.content, 'html.parser')
        # Per ogni categoria navigo per 5 pagine (Ogni pagina ha 50 film e le categorie sono 24)
        for _ in range(1,10):

            # Recupero il link alla prossima pagina
            next_page = soup2.find('div', {'class':'desc'})
            if next_page is not None:
                for href in next_page.find_all('a'):
                    link_next = href.get('href')
                    button_next = href.text.split()
                    if button_next[0] == "Next":
                        next_page = 'https://www.imdb.com' + link_next
                    else:
                        next_page = None

            # Recupero il link dei film nella categoria
            for j in soup2.find_all('div', {'class':'lister-item-content'}):
                link = j.find('a').get('href')
                document_link = 'https://www.imdb.com' + link
            
                page_link = requests.get(document_link)
                soup3 = BeautifulSoup(page_link.content, 'html.parser')

                # Recupero il titolo
                tit = None
                if soup3.find_all('div', {'data-testid':'hero-title-block__original-title'}) != []:
                    j = soup3.find_all('div', {'data-testid':'hero-title-block__original-title'})
                else:
                    j = soup3.find_all('h1', {'data-testid':'hero-title-block__title'})
                for i in j:
                    if i is not None:
                        tit = i.text
                        if tit is not None:
                            tit = tit.strip()
                            # elimina eventuali date scritte tra parentesi
                            tit = tit.replace("Original title: ","")
                            tit = re.sub(r"\([^()]*\)", "", tit)
                            tit = tit.strip()
                            print(tit)

                # Raccolgo il regista
                i = soup3.find('li', {'data-testid':'title-pc-principal-credit'})
                di = None
                if i is not None:
                    dire = i.find('span')
                    if dire is not None and dire.text == "Director":
                        dire = i.find('a', {'class':'ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link'})
                        di = dire.text.strip() 

                # Raccolgo l'anno
                y = None
                i = soup3.find('li', {'data-testid':'title-details-releasedate'})
                if i is not None: 
                    y = i.find('a', {'class':'ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link'})
                    if y is not None:
                        y = y.text
                        y = re.sub(r"\([^()]*\)", "", y)
                        
                        #controllo che la data sia scritta come gg/mm/aa
                        matched = re.match(r"[A-z]{1,9}[\s][0-9]{1,2},[\s][0-9]{4}",y)
                        is_match = bool(matched)
                        if not is_match:
                            y = ""
                        else:
                        # modifico il formato della data
                            y = parse(y)
                            y= y.strftime('%d/%m/%Y')
                        y = y.strip()
                
                # Raccolgo le trame
                i = soup3.find('div', {'data-testid':'storyline-plot-summary'})
                story = None
                if i is not None:
                    story = i.text
                    story = re.sub(r"—[A-z]*\s{0,1}.*$", "", story) 
                    matched = re.match(r".*plot.*unknown.*",story.lower())
                    is_match = bool(matched)
                    if is_match:
                        story = None
                    else:
                        story = story.strip()
                            
                # Raccolgo i generi
                i = soup3.find('li', {'data-testid':'storyline-genres'})
                if i is not None:
                    ge = []
                    for gen in i.find_all('li'):
                        if gen is not None:
                            ge.append(gen.text.strip())
                else:
                    ge = None

                # Controllo se ci sono duplicati
                check_duplicate(tit,y,story,ge,di,document_link)
            
            # Vado alla prossima pagina
            if next_page is not None:
                next_page_genre = requests.get(next_page)
                soup2 = BeautifulSoup(next_page_genre.content, 'html.parser')
            else:
                break

    # Creo un dizionario
    dictionary = create_dictionary(title,year,storyline,genre,director,link_list)

    # Creo un file json contente i film
    with open(root + r"/FilesJson/imdb.json", "w", encoding="utf8") as f:
        json.dump(dictionary,f,indent=4,ensure_ascii=False)

# Funzione che recupera le informazioni dal sito themovie
def retrive_link_themovie():

    # Richiede la pagina Web 
    r = requests.get('https://www.themoviedb.org/movie', headers = hdr)
    # Parser della pagina
    soup = BeautifulSoup(r.content, 'html.parser')

    inizialize_list()

    # Navigo per 149 pagine (se esistono) (Ogni pagina ha 20 film)
    for page in range(1,250):
      
        # Recupero i link dei film all'interno della pagina
        i = soup.find('div', {'id':'page_'+str(page)})
        for link in i.find_all('div', { 'class':'card style_1'}):
            link = 'https://www.themoviedb.org' + link.find('a').get('href')
            
            # Recupero la pagina del film
            film_link = requests.get(link, headers = hdr)
            soup1 = BeautifulSoup(film_link.content, 'html.parser')

            # Header contenente tutte le informazioni che mi servono
            header = soup1.find('section', {'id':'original_header'})
            header = header.find('section', {'class':'header poster'})
            
            if header != None:
                # Recupero il titolo
                tit = header.find('a').text.strip()
                    
                # Recupero la data di uscita
                release = header.find('span', {'class':'release'})
                release = release.text.strip()
                release = re.sub(r"\([^()]*\)", "", release)
                # Modifico la data in dd/mm/yyyy
                release = release[3:5] + "/" + release[:2]   + "/" +  release[6:]
                release = release.strip()

                # Recupero i vari generi del film
                gen = header.find('span', {'class':'genres'})
                ge = []
                for all_genre in gen.find_all('a'):
                    ge.append(all_genre.text.strip())

                # Recupero la trama
                overview = header.find('div', {'class':'overview'})
                overview = overview.find('p').text
                matched = re.match(r".*plot.*unknown.*",overview.lower())
                is_match = bool(matched)
                if is_match:
                    overview = None
                else:
                    overview = overview.strip()

                # Recupero il direttore
                direct = header.find('ol', {'class':'people no_image'})
                for all_profile in direct.find_all('li', {'class':'profile'}):
                    figure = all_profile.find('p', {'class':'character'}).text
                    figure = figure.split()
                    figure = re.sub(r",$","",figure[0])
                    if figure == 'Director':
                        di = all_profile.find('p').find('a').text
                
                check_duplicate(tit,release,overview,ge,di,link)

        # Recupero il link alla pagina successiva e se esiste la apro
        next_page = soup.find('div', {'id':'pagination_page_'+str(page)})
        if next_page is not None:
            next_page = 'https://www.themoviedb.org' + next_page.find('a').get('href')
            page_link = requests.get(next_page, headers = hdr)
            soup = BeautifulSoup(page_link.content, 'html.parser')
        else:
            break

    dictionary = create_dictionary(title,year,storyline,genre,director,link_list)

    with open(root + r"/FilesJson/themovie.json", "w", encoding="utf8") as f:
        json.dump(dictionary,f,indent=4,ensure_ascii=False)

start = 0.0
print('inizio    : ' + str(start))
retrive_link_imdb()
retrive_link_themovie()
end = timer()
print('fine      : ' + str(end))
print('intervallo: ' + str((int(end - start) / 60)) + " minuti")