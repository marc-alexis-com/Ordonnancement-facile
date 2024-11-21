# -*- coding: utf-8 -*-
import pprint
import pandas as pd

def creeGraphe(fichier):
    """
    Lit le fichier 'fichier' et crée un graphe sous forme de dictionnaire.
    Ajoute les noeuds 'alpha' et 'omega' au graphe.
    Retourne le graphe construit.
    """
    # Initialisation du dictionnaire
    graphe = {}

    # Lecture et traitement du fichier
    with open(fichier, 'r') as file:
        for ligne in file:
            # Suppression des espaces en début/fin et séparation par espaces
            elements = ligne.strip().split()

            if not elements:
                continue  # Ignorer les lignes vides

            # Conversion des éléments en entiers
            try:
                numeros = list(map(int, elements))
            except ValueError:
                print(f"Avertissement : La ligne '{ligne.strip()}' contient des valeurs non entières et sera ignorée.")
                continue

            # Extraction des informations
            noeud = numeros[0]
            temps = numeros[1]
            predecesseurs = numeros[2:] if len(numeros) > 2 else []

            # Initialisation du noeud dans le dictionnaire
            graphe[noeud] = {
                'temps': temps,
                'predecesseurs': predecesseurs,
                'sucesseurs': []  # À remplir par la suite
            }

    # Ajout des successeurs
    for noeud, data in graphe.items():
        for pred in data['predecesseurs']:
            if pred in graphe:
                graphe[pred]['sucesseurs'].append(noeud)
            else:
                print(f"Avertissement : Le noeud prédecesseur {pred} n'existe pas dans le graphe.")

    # Détermination des noeuds de départ (sans prédecesseurs) et de fin (sans successeurs)
    noeuds_depart = [noeud for noeud, data in graphe.items() if not data['predecesseurs']]
    noeuds_fin = [noeud for noeud, data in graphe.items() if not data['sucesseurs']]

    # Ajout du noeud 'alpha' (départ)
    graphe['alpha'] = {
        'temps': 0,
        'predecesseurs': [],
        'sucesseurs': noeuds_depart
    }

    # Mise à jour des noeuds de départ pour inclure 'alpha' comme prédecesseur
    for noeud in noeuds_depart:
        graphe[noeud]['predecesseurs'].append('alpha')

    # Ajout du noeud 'omega' (fin)
    graphe['omega'] = {
        'temps': 0,
        'predecesseurs': noeuds_fin,
        'sucesseurs': []
    }

    # Mise à jour des noeuds de fin pour inclure 'omega' comme successeur
    for noeud in noeuds_fin:
        graphe[noeud]['sucesseurs'].append('omega')

    # Affichage du dictionnaire complet
    print("Dictionnaire du graphe avec 'alpha' et 'omega' :")
    pprint.pprint(graphe)

    return graphe

def circuit(graphe):
    """
    Vérifie si le graphe contient un cycle.
    Retourne True s'il y a un cycle, sinon False.
    """
    visited = set()
    rec_stack = set()

    def dfs(noeud):
        visited.add(noeud)
        rec_stack.add(noeud)
        try:
            for succ in graphe[noeud]['sucesseurs']:
                if succ not in graphe:
                    continue  # Ignorer les successeurs inexistants
                if succ not in visited:
                    if dfs(succ):
                        return True
                elif succ in rec_stack:
                    return True
        finally:
            rec_stack.remove(noeud)
        return False

    for noeud in graphe:
        if noeud not in visited:
            if dfs(noeud):
                return True
    return False

def arcNegatifs(graphe):
    """
    Vérifie qu'aucun noeud n'a un temps négatif.
    Retourne True s'il y a des temps négatifs, sinon False.
    """
    negatifs = [noeud for noeud, data in graphe.items() if isinstance(data['temps'], (int, float)) and data['temps'] < 0]
    if negatifs:
        print(f"Le graphe contient des noeuds avec des temps négatifs : {negatifs}")
        return True
    return False

def afficher_matrice_adjacence(graphe):
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    noeuds = sorted(graphe.keys(), key=lambda x: (isinstance(x, str), x))

    # Création d'un DataFrame pandas pour la matrice d'adjacence
    matrice = pd.DataFrame(0, index=noeuds, columns=noeuds)

    # Remplissage de la matrice
    for noeud, data in graphe.items():
        for succ in data['sucesseurs']:
            if succ in graphe:  # Vérifier que le successeur existe dans le graphe
                matrice.loc[noeud, succ] = 1
            else:
                print(f"Avertissement : Le successeur '{succ}' du noeud '{noeud}' n'existe pas dans le graphe.")

    # Affichage de la matrice
    print("\nMatrice d'adjacence :\n")
    print(matrice)

def compute_ranks(graphe):
    """
    Calcule les rangs de chaque noeud dans le graphe.
    Retourne True si réussi, False s'il y a un cycle.
    """
    # Initialisation des rangs
    for noeud in graphe:
        graphe[noeud]['rang'] = None
    graphe['alpha']['rang'] = 0

    assigned_nodes = ['alpha']
    while len(assigned_nodes) < len(graphe):
        progress = False
        for noeud in graphe:
            if graphe[noeud]['rang'] is None:
                preds = graphe[noeud]['predecesseurs']
                if all(graphe[pred]['rang'] is not None for pred in preds):
                    graphe[noeud]['rang'] = max([graphe[pred]['rang'] for pred in preds]) + 1 if preds else 0
                    assigned_nodes.append(noeud)
                    progress = True
        if not progress:
            print("Impossible de calculer les rangs, il y a un cycle dans le graphe.")
            return False

    print("\nRangs des sommets :")
    for noeud in graphe:
        print(f"Noeud {noeud}: Rang {graphe[noeud]['rang']}")
    return True

def compute_earliest_dates(graphe):
    """
    Calcule les dates au plus tôt pour chaque noeud.
    """
    for noeud in graphe:
        graphe[noeud]['date_plus_tot'] = None
    graphe['alpha']['date_plus_tot'] = 0

    max_rang = max(graphe[noeud]['rang'] for noeud in graphe)
    for r in range(max_rang + 1):
        noeuds_rang = [noeud for noeud in graphe if graphe[noeud]['rang'] == r]
        for noeud in noeuds_rang:
            preds = graphe[noeud]['predecesseurs']
            if preds:
                graphe[noeud]['date_plus_tot'] = max([graphe[pred]['date_plus_tot'] + graphe[pred]['temps'] for pred in preds])
            else:
                graphe[noeud]['date_plus_tot'] = 0

    print("\nDates au plus tôt :")
    for noeud in graphe:
        print(f"Noeud {noeud}: Date au plus tôt {graphe[noeud]['date_plus_tot']}")

def compute_latest_dates(graphe):
    """
    Calcule les dates au plus tard pour chaque noeud.
    """
    for noeud in graphe:
        graphe[noeud]['date_plus_tard'] = None
    graphe['omega']['date_plus_tard'] = graphe['omega']['date_plus_tot']

    max_rang = max(graphe[noeud]['rang'] for noeud in graphe)
    for r in range(max_rang, -1, -1):
        noeuds_rang = [noeud for noeud in graphe if graphe[noeud]['rang'] == r]
        for noeud in noeuds_rang:
            if noeud != 'omega':
                succs = graphe[noeud]['sucesseurs']
                if succs:
                    graphe[noeud]['date_plus_tard'] = min([graphe[succ]['date_plus_tard'] - graphe[noeud]['temps'] for succ in succs])
                else:
                    graphe[noeud]['date_plus_tard'] = graphe['omega']['date_plus_tard'] - graphe[noeud]['temps']

    print("\nDates au plus tard :")
    for noeud in graphe:
        print(f"Noeud {noeud}: Date au plus tard {graphe[noeud]['date_plus_tard']}")

def compute_margins(graphe):
    """
    Calcule les marges totales pour chaque noeud.
    """
    for noeud in graphe:
        graphe[noeud]['marge_totale'] = graphe[noeud]['date_plus_tard'] - graphe[noeud]['date_plus_tot']

    print("\nMarges totales :")
    for noeud in graphe:
        print(f"Noeud {noeud}: Marge Totale {graphe[noeud]['marge_totale']}")

def find_critical_paths(graphe):
    """
    Trouve et affiche le(s) chemin(s) critique(s) dans le graphe.
    """
    critical_nodes = [noeud for noeud in graphe if graphe[noeud]['marge_totale'] == 0]

    paths = []
    def dfs(current_node, path):
        if current_node == 'omega':
            paths.append(path.copy())
            return
        for succ in graphe[current_node]['sucesseurs']:
            if succ in critical_nodes:
                dfs(succ, path + [succ])

    dfs('alpha', ['alpha'])

    print("\nChemin(s) critique(s) :")
    for path in paths:
        print(" -> ".join(map(str, path)))

def main():
    graphe = creeGraphe("graphe.txt")

    # Affichage de la matrice d'adjacence
    afficher_matrice_adjacence(graphe)

    # Vérification des circuits
    if circuit(graphe):
        print("\nLe graphe contient au moins un circuit (cycle).")
    else:
        print("\nLe graphe ne contient pas de circuit (cycle).")

    # Vérification des arcs à valeurs négatives
    if arcNegatifs(graphe):
        print("\nLe graphe contient des temps négatifs, il n'est pas valide pour l'ordonnancement.")
    else:
        print("\nAucun noeud du graphe n'a de temps négatif.")

    # Si le graphe est valide, effectuer les calculs
    if not circuit(graphe) and not arcNegatifs(graphe):
        if compute_ranks(graphe):
            compute_earliest_dates(graphe)
            compute_latest_dates(graphe)
            compute_margins(graphe)
            find_critical_paths(graphe)
    else:
        print("\nLe graphe n'est pas valide pour l'ordonnancement.")

if __name__ == "__main__":
    main()
