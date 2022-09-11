import os.path
import json
import datetime
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID, DATETIME
from whoosh.analysis import StemmingAnalyzer

def main(root):

    # Lo schema dell'index (Data di uscita del film, link al film, titolo del film, trama del film)
    schema = Schema(Atitle=TEXT(stored=True, field_boost=3.0, analyzer=StemmingAnalyzer()),
                    date=DATETIME(stored=True, sortable=True),
                    Bcontent=TEXT(stored=True, analyzer=StemmingAnalyzer()),
                    Dgenre=TEXT(stored=True),
                    Cdirector=TEXT(stored=True),
                    Fpath=ID(stored=True)
                    )

    # Crea la directory che conterrà l'index
    if not os.path.exists(root + r'/indexdir'):
        os.mkdir(root + r'/indexdir')

    # Crea un index writer per aggiungere i documenti per schema
    ix = create_in(r"./indexdir", schema)
    writer = ix.writer()
      
    filepaths = [os.path.join(root + r'/FilesJson',i) for i in os.listdir(root + r'/FilesJson')]
    
    # Creo un file.txt contenente tutti i direttori (utile nella gui)
    with open("director.txt", "w", encoding='utf-8') as f: 
        with open("genres.txt","w",encoding='utf-8') as g:
        
            # Per ogni file nella directory FilesJson -->
            for filename in filepaths:
                with open(filename, encoding='utf-8') as file:
                    data = json.loads(file.read())

                    # estraggo titolo, anno, storia, genere, direttore e link
                    for v in data.values():
                        title = v["title"]
                        Edate = v["year"]
                        try:
                            Edate = datetime.datetime.strptime(Edate, "%d/%m/%Y")     # convert the string in a date obj
                        except (ValueError):
                            Edate = datetime.datetime.strptime("1970-01-02", "%d/%m/%Y")
                        content = v["storyline"]

                        genre = v["genre"]
                        list_genre = ""
                        for gen in genre:
                            # Creo un genre.txt contenente tutti i generi (utile nella gui)
                            g.write(gen + "\n")
                            list_genre += f" {gen}" 
                        genre = list_genre
                        director = v["director"]
                        path = v["link"]

                        # Creo un director.txt contenente tutti i direttori (utile nella gui)
                        director_txt = v["director"].split()
                        for word in director_txt:
                            if word != "|":
                                f.write(word + " ")
                            else:
                                f.write("\n")
                        f.write("\n")
                                    
                        # Aggiunge i film con i loro campi all'index
                        writer.add_document(Atitle=title, date=Edate, Bcontent=content, Dgenre=genre, Cdirector=director, Fpath=path)

    # Salva i documenti aggiunti nell'index
    writer.commit()

if __name__ == '__main__':
    root = os.path.abspath(os.curdir)
    main(root)