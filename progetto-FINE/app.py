from flask import Flask, render_template, request
import query
import math

app = Flask(__name__)
data = []
headings = ("Title", "Plot", "Director", "Genre", "Data", "Link")

lista_director = []
lista_genres = []
f = open('director.txt', 'r+', encoding='utf-8')
for name in f.readlines():
    lista_director.append(name)
lista_director = list(set(lista_director))

f = open('genres.txt', 'r+', encoding='utf-8')
for name in f.readlines():
    lista_genres.append(name)
lista_genres= list(set(lista_genres))

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/advanced', methods=['GET', 'POST'])
def advanced():
    return render_template('advanced.html', data=lista_director, genres=lista_genres)


@app.route('/results', methods=['GET', 'POST'])
def results():
    ask = {'text': request.args.get('barra'), 'imdb': request.args.get('IMDB'), 'themovie': request.args.get('THEMOVIE'),
           'filmsomniac': request.args.get('FILMSOMNIAC'), 'from': request.args.get('Da'), 'to': request.args.get('a'),
           'director': request.args.get('director'), 'genres': request.args.get('genres')}

    count = request.args.get('n_res')
    if count is None:
        count = 10
    else:
        count = int(count)

    data,lunghezza = query.my_query(ask,count)
    syn = query.expansion_query(ask['text'])
    return render_template("results.html", headings=headings, data=data, syns=syn, lun=lunghezza, syn_lun=len(syn))

#     ap = [0.0 for j in range(10)]
#     mean_ap = 0  # MAP
#     mean_NDCG = 0  # NDCG
#     with open("./benchmark/test_queries.txt", "r") as file:
#         n = 0
#         for q in file.readlines():
#             ask['text'] = q

#             # Setto come siti solo imdb e themoviedb a causa di un malfunzionamento del sito filmsomniac
#             ask['imdb'] = "*www.imdb.com*"
#             ask['themovie'] = "*www.themoviedb.org*"
#             ask['filmsomniac'] = ""

#             data,lunghezza = query.my_query(ask,10)  # Processa le query
#             test_ap, NDCG = benchmark(data,n+1) # Recupera AP e NDCG 
#             ap[n] += test_ap  # Lista con le AP di tutte le queries 
#             mean_NDCG += NDCG
#             n += 1

#     print(ap)

#     mean_ap = sum(ap) / n # Calcolo della MAP
#     print(mean_ap)

#     mean_NDCG /= n  # Calcolo della mean NDCG
#     print(mean_NDCG)
	
# # Funzione usata per processare il file test_queries.txt
# def find_nth(haystack, needle, n):
#     start = haystack.find(needle)
#     while start >= 0 and n > 1:
#         start = haystack.find(needle, start + len(needle))
#         n -= 1

#     return start

# # Funzione per i benchmark
# def benchmark(film,i):

#     with open("./benchmark/relevant_documents.txt", "r") as file:
#         lines = ""
#         for row in file.readlines():
#             lines += row

#         start = find_nth(lines, '[', i) + 1
#         end = find_nth(lines, ']', i)
#         lines = lines[start:end]
#         lines = lines.replace("\'", "")
#         lines = lines.replace("\n", "")
#         lines = lines.strip()

#         relevant_docs = lines.split(',')

#         DCG_dict = {}
#         rank_rel = 6
#         c = 1
#         GT_DCG = 6

#         # Calcolo della NDCG
#         for doc in relevant_docs:
#             if c > 1:
#                 GT_DCG += rank_rel / math.log(c, 2)
#             c += 1
#             if rank_rel >= 2:
#                 DCG_dict[''.join(doc.split())] = rank_rel
#                 rank_rel -= 1
#             else:
#                 DCG_dict[''.join(doc.split())] = rank_rel

#         s = 0
#         for i in range(1, 11, 1):
#             if i > len(DCG_dict):
#                 break
#             try:
#                 if i == 1:
#                     s += DCG_dict[film[i - 1]['Fpath']]
#                 else:
#                     s += DCG_dict[film[i - 1]['Fpath']] / math.log(i, 2)
#             except KeyError:
#                 continue

#         NDCG = s / GT_DCG

#         ap = 0
#         num_trovati = 0

#         # Calcolo della AP
#         for f in range(1,len(film)+1):
#             for r in range(0,len(relevant_docs)):
#                 if film[f-1]["Fpath"] == ''.join(relevant_docs[r].split()):
#                     num_trovati += 1
#                     ap += num_trovati / f
#                     break
#         if num_trovati == 0:
#             pass
#         else:
#             ap /= num_trovati

#     return ap, NDCG

if __name__ == "__main__":
    app.run(debug=True)
