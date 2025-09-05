import json
import matplotlib.pyplot as plt

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

def plot_list(data1, data2):
    plt.figure(figsize=(10, 5))
    plt.plot(data1, marker='o', color='green', label="Edge")
    plt.plot(data2, marker='x', color='blue', label="Cloud")
    plt.title('Comparison of latencies')
    plt.xlabel('Number of requests')
    plt.ylabel('Latency in ms')
    plt.grid(True)
    plt.legend()
    plt.show()

def calcule_moyenne(listes):
    l = len(listes)
    c = len(listes[0])
    print(f"Nombre de listes: {l}, Nombre d'éléments par liste: {c}")
    results = []
    for i in range(l-1):
        value = 0
        for j in range(c-1):
           
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



plot_list(edge, edgeP)
plot_list(cloud, cloudP)

print(f"La nouvelle liste est sauvegardée dans result_file.json")
