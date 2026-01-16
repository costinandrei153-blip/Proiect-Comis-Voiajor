import random
import matplotlib.pyplot as plt

distante = [
    # 0   1   2   3   4   5   6   7
    [ 0, 12, 25, 18, 22, 30, 28, 24],
    [10,  0, 14, 20, 26, 18, 16, 22],
    [24, 13,  0, 15, 17, 28, 21, 19],
    [18, 21, 16,  0, 14, 22, 26, 20],
    [23, 27, 18, 15,  0, 16, 19, 14],
    [31, 19, 29, 23, 17,  0, 12, 15],
    [29, 17, 22, 27, 20, 13,  0, 11],
    [25, 23, 20, 21, 15, 16, 12,  0],
]

NUMAR_ORASE = len(distante)

# coordonate pentru vizualizare (fixe)
coords = {
    0: (10, 60),
    1: (30, 80),
    2: (55, 75),
    3: (70, 55),
    4: (60, 30),
    5: (35, 20),
    6: (15, 30),
    7: (25, 50),
}

# FUNCTII DE BAZA

def creeaza_ruta_random():
    ruta = list(range(NUMAR_ORASE))
    random.shuffle(ruta)
    return ruta


def calculeaza_distanta_totala(ruta):
    total = 0
    for i in range(len(ruta) - 1):
        total += distante[ruta[i]][ruta[i + 1]]
    total += distante[ruta[-1]][ruta[0]]
    return total


def creeaza_populatie_initiala(dimensiune):
    return [creeaza_ruta_random() for _ in range(dimensiune)]


# SELECTIE / CROSSOVER

def selectie_turneu(populatie, lungimi, k=3):
    candidati = random.sample(range(len(populatie)), k)
    best = min(candidati, key=lambda i: lungimi[i])
    return populatie[best][:]


def incrucisare_ox(p1, p2):
    n = len(p1)
    a, b = sorted(random.sample(range(n), 2))
    copil = [-1] * n
    copil[a:b+1] = p1[a:b+1]

    poz = (b + 1) % n
    for oras in p2[b+1:] + p2[:b+1]:
        if oras not in copil:
            copil[poz] = oras
            poz = (poz + 1) % n
    return copil

def mutatie_schimb(ruta):
    a, b = random.sample(range(len(ruta)), 2)
    ruta[a], ruta[b] = ruta[b], ruta[a]


# 2-OPT

def imbunatatire_2opt(ruta):
    best = ruta[:]
    best_dist = calculeaza_distanta_totala(best)
    n = len(ruta)

    imbunatatit = True
    while imbunatatit:
        imbunatatit = False
        for i in range(1, n - 2):
            for j in range(i + 1, n - 1):
                nou = best[:]
                nou[i:j] = reversed(nou[i:j])
                d = calculeaza_distanta_totala(nou)
                if d < best_dist:
                    best = nou
                    best_dist = d
                    imbunatatit = True
                    break
            if imbunatatit:
                break
    return best


# ALGORITM GENETIC

def ruleaza_ga_tsp(
    dimensiune_populatie=50,
    numar_generatii=200,
    rata_mutatie=0.15,
    marime_elita=1,
    foloseste_2opt=True
):
    populatie = creeaza_populatie_initiala(dimensiune_populatie)
    best_global = None
    best_dist = float("inf")

    for gen in range(numar_generatii):
        lungimi = [calculeaza_distanta_totala(r) for r in populatie]

        idx = min(range(len(populatie)), key=lambda i: lungimi[i])
        if lungimi[idx] < best_dist:
            best_dist = lungimi[idx]
            best_global = populatie[idx][:]

        if gen % (numar_generatii // 5) == 0:
            print(f"Gen {gen}: best = {best_dist}")

        elite_idx = sorted(range(len(populatie)), key=lambda i: lungimi[i])
        noua_pop = [populatie[i][:] for i in elite_idx[:marime_elita]]

        while len(noua_pop) < dimensiune_populatie:
            p1 = selectie_turneu(populatie, lungimi)
            p2 = selectie_turneu(populatie, lungimi)
            copil = incrucisare_ox(p1, p2)

            if random.random() < rata_mutatie:
                mutatie_schimb(copil)

            if foloseste_2opt:
                copil = imbunatatire_2opt(copil)

            noua_pop.append(copil)

        populatie = noua_pop

    return best_global, best_dist


def ruleaza_ga_multi_start(numar_rulari=10, **params):
    best_ruta = None
    best_dist = float("inf")

    for i in range(numar_rulari):
        random.seed()
        ruta, dist = ruleaza_ga_tsp(**params)
        print(f"[Rulare {i+1}] distanta = {dist}")
        if dist < best_dist:
            best_dist = dist
            best_ruta = ruta[:]

    return best_ruta, best_dist


# VIZUALIZARE CU MATPLOTLIB

def deseneaza_ruta(ruta, titlu):
    x = [coords[i][0] for i in ruta] + [coords[ruta[0]][0]]
    y = [coords[i][1] for i in ruta] + [coords[ruta[0]][1]]

    plt.figure(figsize=(6, 6))
    plt.plot(x, y, marker='o')
    for i, (xi, yi) in coords.items():
        plt.text(xi + 1, yi + 1, str(i))
    plt.title(titlu)
    plt.grid(True)
    plt.show()


if __name__ == "__main__":

    ruta_optima, distanta_optima = ruleaza_ga_multi_start(
        numar_rulari=10,
        dimensiune_populatie=60,
        numar_generatii=200,
        rata_mutatie=0.15,
        marime_elita=1,
        foloseste_2opt=True
    )

    print("\nCea mai buna ruta:", ruta_optima)
    print("Distanta:", distanta_optima)

    deseneaza_ruta(
        ruta_optima,
        f"Ruta optima GA (distanta = {distanta_optima})"
    )
