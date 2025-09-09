import json
import matplotlib.pyplot as plt
import numpy as np

import os

os.makedirs("images", exist_ok=True)

def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

def add_lists(list1, list2):
    if len(list1) != len(list2):
        raise ValueError("Les listes doivent avoir la même longueur")
    return [x + y for x, y in zip(list1, list2)]

def plot_list(data1, data2, title, filename):
    plt.figure(figsize=(10, 5))

    # Plot lines
    plt.plot(data1, color='darkorange', label="without Policy")
    plt.plot(data2, color='purple', label="with Policy")

    # Mean lines
    mean1 = np.mean(data1)
    mean2 = np.mean(data2)
    plt.axhline(mean1, color='darkorange', linestyle='--', alpha=0.7, label=f"mean w/o Policy ({mean1:.1f} ms)")
    plt.axhline(mean2, color='purple', linestyle='--', alpha=0.7, label=f"mean w/ Policy ({mean2:.1f} ms)")

   
    plt.title('Comparison of latencies ' + title)
    plt.xlabel('Experiment iteration')
    plt.ylabel('Latency (ms)')
    plt.grid(True, linestyle=":", alpha=0.7)
    plt.legend()
    plt.tight_layout()

    filepath = os.path.join("images", filename + ".png")
    plt.savefig(filepath)
    plt.close()


def plot_boxplot(data1, data2, title, filename):
    plt.figure(figsize=(8, 6))
    plt.boxplot([data1, data2], labels=["without Policy", "with Policy"])
    plt.title("Distribution of Latencies " + title)
    plt.ylabel("Latency (ms)")
    plt.grid(True, axis='y')
    file_path = os.path.join("images", filename + ".png")
    plt.savefig(file_path)
    plt.close()


def calcule_moyenne(listes):
    l = len(listes)
    c = len(listes[0])
    print(f"Nombre de listes: {l}, Nombre d'éléments par liste: {c}")
    results = []
    for i in range(l):
        value = 0
        for j in range(c):
           
            value += float(listes[i][j])
        value = value / c
        results.append(value)
    return results


list1= load_json('picar-x-code/Edge.json')
list2= load_json('picar-x-code/Cloud.json')
list3= load_json('picar-x-code/Edge-P.json')
list4= load_json('picar-x-code/Cloud-P.json')

try:
    edge=calcule_moyenne(list1)
    cloud=calcule_moyenne(list2)
    edgeP=calcule_moyenne(list3)
    cloudP=calcule_moyenne(list4)

except ValueError as e:
    print(f"Erreur : {e}")

def media(list):
    x=0
    for i in range(len(list)):
        x+=list[i]
    
    return x/len(list)

print("Edge sin politica",media(edge))
print("Edge con politica ",media(edgeP))
print("Cloud sin politica",media(cloud))
print("Cloud con politica",media(cloudP))



plot_list(edge, edgeP, "Edge ","Plotlist Edge")
plot_list(cloud, cloudP,"Cloud","Plotlist Cloud")

plot_boxplot(edge,edgeP," Edge ","boxplot Edge")
plot_boxplot(cloud,cloudP,"Cloud", "boxplot Cloud")