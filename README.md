# Ordonnancement facile !

## Programme d'Ordonnancement

### Description

Permet de réaliser l'ordonnancement de projets en se basant sur un tableau de contraintes. Il lit un fichier contenant les contraintes, construit un graphe associé, vérifie la validité du graphe (absence de circuits et d'arcs à valeurs négatives), et calcule les calendriers au plus tôt et au plus tard, les marges, ainsi que les chemins critiques du projet.

### Fonctionnalités

1. **Lecture et Importation des Contraintes**  
   Le programme lit un fichier `.txt` contenant un tableau de contraintes, le stocke en mémoire et affiche le tableau sous forme de graphe matriciel.

2. **Construction du Graphe**  
   À partir des contraintes, le programme construit un graphe représentant les dépendances entre les tâches, incluant les nœuds fictifs `alpha` (début) et `omega` (fin).

3. **Vérification de la Validité du Graphe**  
   - **Absence de Circuit** : Vérifie que le graphe ne contient pas de cycles.
   - **Absence d'Arcs à Valeurs Négatives** : Assure qu'aucune tâche n'a une durée négative.

4. **Calcul des Calendriers et Marges**  
   Si le graphe est valide, le programme calcule :
   - Les rangs des sommets via un tri topologique.
   - Le calendrier au plus tôt.
   - Le calendrier au plus tard, en utilisant la convention que la date au plus tard de fin de projet est égale à sa date au plus tôt.
   - Les marges pour chaque tâche.

5. **Identification des Chemins Critiques**  
   Détecte et affiche les chemins critiques du projet, c'est-à-dire les séquences de tâches sans marge.

6. **Bouclage sur une Série de Tableaux de Contraintes**  
   Le programme peut traiter une série de tableaux de contraintes sans nécessiter de redémarrage entre chaque traitement.

### Prérequis

- **Langage de Programmation** : Python 3.x
- **Bibliothèques Python** :
  - `pandas` pour la manipulation des matrices d'adjacence.
  
  Vous pouvez installer les dépendances nécessaires en utilisant pip :

  ```bash
  pip install pandas
  ```

### Structure du Projet

- `main.py` : Fichier principal contenant le code source du programme.
- `graphe.txt` : Exemple de fichier contenant un tableau de contraintes.
- `README.md` : Ce fichier de documentation.

### Utilisation

1. **Préparation des Fichiers de Contraintes**  
   Créez des fichiers `.txt` contenant les tableaux de contraintes selon le format spécifié. Chaque ligne doit représenter une tâche avec le numéro de tâche, sa durée, et ses prédécesseurs si applicable.

   **Exemple de `graphe.txt`** :
   ```
   1 9 
   2 2 
   3 3 2
   4 5 1
   5 2 1 4
   6 2 5
   7 2 4
   8 4 4 5
   9 5 4
   10 1 2 3
   11 2 1 5 6 7 8
   ```

2. **Exécution du Programme**  
   Assurez-vous que tous les fichiers de contraintes sont dans le même répertoire que le script `main.py`. Exécutez le programme via la ligne de commande :

   ```bash
   python main.py
   ```

   Le programme affichera :
   - Le dictionnaire du graphe avec `alpha` et `omega`.
   - La matrice d'adjacence.
   - La vérification de l'absence de circuits et d'arcs à valeurs négatives.
   - Les rangs des sommets.
   - Les dates au plus tôt et au plus tard.
   - Les marges totales.
   - Les chemins critiques.

3. **Traitement de Plusieurs Tableaux de Contraintes**  
   Pour traiter plusieurs fichiers de contraintes, assurez-vous que tous les fichiers sont listés et modifiez la fonction `main()` pour boucler sur ces fichiers. Actuellement, le programme traite uniquement `graphe.txt`. Vous pouvez adapter le programme pour qu'il demande à l'utilisateur de choisir le fichier à traiter ou pour qu'il parcoure un répertoire contenant plusieurs fichiers `.txt`.

### Exemple d'Exécution

Lors de l'exécution avec l'exemple de `graphe.txt`, le programme affichera :

1. **Dictionnaire du Graphe** :
   ```python
   {'1': {'temps': 9, 'predecesseurs': ['alpha'], 'sucesseurs': [4, 5, 11]},
    '2': {'temps': 2, 'predecesseurs': ['alpha'], 'sucesseurs': [3, 10, 11]},
    '3': {'temps': 3, 'predecesseurs': [2], 'sucesseurs': [10]},
    ...
    'alpha': {'temps': 0, 'predecesseurs': [], 'sucesseurs': [1, 2]},
    'omega': {'temps': 0, 'predecesseurs': [9, 10, 11], 'sucesseurs': []}}
   ```

2. **Matrice d'Adjacence** :
   ```
           0 1 2 3 4 5 6 7 8 9 10 11
   alpha    0 1 1 0 0 0 0 0 0 0  0   0
   1        0 0 0 1 1 0 0 0 0 0  0   1
   2        0 0 0 1 0 1 0 0 0 0  1   1
   3        0 0 0 0 0 0 0 0 0 0  1   0
   ...
   omega    0 0 0 0 0 0 0 0 0 1  1   0
   ```

3. **Vérifications et Calculs** :
   ```
   Le graphe ne contient pas de circuit (cycle).
   Aucun noeud du graphe n'a de temps négatif.
   
   Rangs des sommets :
   Noeud alpha: Rang 0
   Noeud 1: Rang 1
   Noeud 2: Rang 1
   Noeud 3: Rang 2
   ...

   Dates au plus tôt :
   Noeud alpha: Date au plus tôt 0
   Noeud 1: Date au plus tôt 0
   Noeud 2: Date au plus tôt 0
   Noeud 3: Date au plus tôt 2
   ...

   Dates au plus tard :
   Noeud alpha: Date au plus tard 0
   Noeud 1: Date au plus tard 0
   Noeud 2: Date au plus tard 0
   Noeud 3: Date au plus tard 2
   ...

   Marges totales :
   Noeud alpha: Marge Totale 0
   Noeud 1: Marge Totale 0
   Noeud 2: Marge Totale 0
   Noeud 3: Marge Totale 0
   ...

   Chemin(s) critique(s) :
   alpha -> 1 -> 4 -> 5 -> 8 -> omega
   alpha -> 2 -> 5 -> 8 -> omega
   alpha -> 2 -> 11 -> omega
   ```

### Remarques

- **Format des Fichiers de Contraintes** : Assurez-vous que chaque ligne du fichier `.txt` suit le format `[numéro_tâche] [durée] [prédécesseurs...]`. Les nœuds fictifs `alpha` (0) et `omega` (N+1) sont ajoutés automatiquement par le programme.

- **Gestion des Erreurs** : Le programme affiche des avertissements si des prédécesseurs référencés n'existent pas ou si des lignes contiennent des valeurs non entières.
