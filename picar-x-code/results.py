import json
import matplotlib.pyplot as plt

def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

def add_lists(list1, list2):
    # Assurez-vous que les listes sont de la même longueur
    if len(list1) != len(list2):
        raise ValueError("Les listes doivent avoir la même longueur")
    return [x + y for x, y in zip(list1, list2)]

def plot_list( data1,data3):
    plt.figure(figsize=(10, 5))
    plt.plot(data1, marker='x', color='blue', label="Politiques")
    plt.plot(data3, marker='_', color='red', label='Bundle service')
    plt.title('Comparison of latencies')
    plt.xlabel('Number of requests')
    plt.ylabel('Latency in ms')
    plt.grid(True)
    plt.legend()
    plt.show()


def calcule_moyenne(listes):
    flat =[x[0]for x in listes]
    l = len(flat)
    results = []
    for j in range(100):
        value = flat[j]
        results.append(value)
    return results
       

list1= load_json('Edge.json')
list2= load_json('Edge.json')
list3= load_json('Edge-P.json')
list4= load_json('Edge-P.json')

# Additionner les valeurs correspondantes des deux listes
try:
    edge=calcule_moyenne(list1)
    cloud=calcule_moyenne(list2)
    edgeP=calcule_moyenne(list3)
    cloudP=calcule_moyenne(list4)

except ValueError as e:
    print(f"Erreur : {e}")


plot_list( edge,edgeP)
#plot_list( cloud,cloudP)

print(f"La nouvelle liste est sauvegardée dans result_file.json")
