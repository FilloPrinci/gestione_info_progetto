import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

def AP(models):
    fig, ax = plt.subplots(figsize=(20,10))
    c = 0
    for m in models:
        for k,v in results.items():
            if m in k:
                y = v[0][1:]
                plt.plot(x,y,marker='o',color=colors[c])
        c += 1

    plt.title("Avarage Precision",weight="bold")
    plt.xlabel("recall")
    plt.ylabel("precision")
    plt.xlim([0,10])
    plt.ylim([0,100])
    plt.xticks(x)
    BMF25 = mpatches.Patch(color='green', label='BMF25')
    TD_IDF = mpatches.Patch(color='blue', label='TD_IDF')
    Frequency = mpatches.Patch(color='black', label='Frequency')
    plt.legend(handles=[BMF25, TD_IDF, Frequency])
    plt.savefig(root + r"./benchmark/Avarage_Precision.png")

def bars(models, metric):
    labels = []
    y = []
    fig, ax = plt.subplots(figsize=(20,10))
    width = 0.50
    for m in models:
        for k,v in results.items():
            if m in k:
                y.append(v[metric])
                labels.append(k)

    if metric == 1:
        plt.title("MAP",weight="bold")
    else:
        plt.title("NDCG",weight="bold")

    plt.ylim([0,100])
    x = np.arange(len(labels))
    bar = []
    bar.append(ax.bar(x[0], y[0], width,color="green"))
    bar.append(ax.bar(x[1], y[1], width,color="blue"))
    bar.append(ax.bar(x[2], y[2], width,color="black"))
    ax.set_xticklabels([])
    for b in bar:
        for i in b:
            height = i.get_height()
            ax.annotate('{}'.format(height),xy=(i.get_x() + i.get_width() / 2, height),xytext=(0, 3),textcoords="offset points",ha='center', va='bottom')

    BMF25 = mpatches.Patch(color='green', label='BMF25')
    TD_IDF = mpatches.Patch(color='blue', label='TD_IDF')
    Frequency = mpatches.Patch(color='black', label='Frequency')
    plt.legend(handles=[BMF25, TD_IDF, Frequency])

    if metric == 1:
        plt.savefig(root + r"./benchmark/MAP.png")
    else:
        plt.savefig(root + r"./benchmark/NDCG.png")
    
if __name__ == "__main__":
    root = os.path.abspath(os.curdir)

    results = {
				"BM25F":
					[
						[0.0, 87.11111111111111, 84.12698412698413, 10.0, 63.33333333333333, 22.5, 50.0, 51.66666666666667, 42.063492063492064, 11.11111111111111, 69.25925925925925],
						49,
						35
					],
				"TF_IDF":
					[
						[0.0, 80.99999999999999, 84.12698412698413, 0.0, 70.00000000000001, 52.77777777777778, 16.666666666666666, 51.66666666666667, 60.95238095238095, 33.819444444444446, 65.95238095238095],
						52,
						34
					],
				"Frequency":
					[
						[0.0, 36.547619047619045, 84.12698412698413, 12.5, 62.5, 52.77777777777778, 0.0, 83.33333333333334, 37.777777777777777, 0.0, 64.48979591836734],
						44,
						33
					]
	 		}

    plt.rcParams.update({'font.size': 16})
    x = [i for i in range(1,11,1)]
    colors = ['green', 'blue', 'black']
    models = ["BM25F", "TF_IDF", "Frequency"]
    AP(models)
    bars(models,1)
    bars(models,2)

    plt.show()
