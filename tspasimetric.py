import random

#(TSP asimetric)
# distante[i][j] = distanta de la orasul i la orasul j

distante = [
    #   A    B    C    D
    [  0,  10,  15,  20],   # A
    [  5,   0,   9,  10],   # B
    [  6,  13,   0,  12],   # C
    [  8,   8,   9,   0],   # D
]

NUMAR_ORASE = len(distante)

# REPREZENTAREA INDIVIDULUI
# Un individ = o ruta (lista cu orase in ordine)

def creeaza_ruta_random():
    """
    Genereaza o ruta aleatoare.
    Orasele sunt reprezentate prin index: 0, 1, 2, ...
    """
    ruta = list(range(NUMAR_ORASE))
    random.shuffle(ruta)
    return ruta

# CALCULUL DISTANTEI TOTALE A UNEI RUTE

def calculeaza_distanta_totala(ruta):
    """
    Calculeaza distanta totala a rutei:
    se aduna distantele dintre orasele consecutive
    + drumul de intoarcere la orasul de plecare.
    """
    total = 0
    for i in range(len(ruta) - 1):
        oras_curent = ruta[i]
        oras_urmator = ruta[i + 1]
        total += distante[oras_curent][oras_urmator]

    # intoarcere la orasul de start
    total += distante[ruta[-1]][ruta[0]]
    return total

# FUNCTIA DE FITNESS
# Fitness = 1 / distanta_totala

def fitness(ruta):
    """
    Cu cat ruta este mai scurta, cu atat fitness-ul este mai mare.
    """
    lungime = calculeaza_distanta_totala(ruta)
    return 1 / lungime

# EXEMPU DE TESTSS
if __name__ == "__main__":
    random.seed(42)

    ruta = creeaza_ruta_random()
    print("Ruta generata:", ruta)
    print("Distanta totala:", calculeaza_distanta_totala(ruta))
    print("Fitness:", fitness(ruta))
