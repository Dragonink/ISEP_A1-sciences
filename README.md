# Simulation pour les _Sciences du Numérique_

**EVOLUTION SIMPLIFIEE DE LA TEMPERATURE EN FONCTION DES GAZ A EFFET DE SERRE**

## Installation

1. [_Téléchager_](https://github.com/Dragonink/SCIENCES/archive/master.zip) ou [_cloner_](https://github.com/Dragonink/SCIENCES.git) ce dépôt
2. Installer les packages Python suivants le cas échéant :
    - ``numpy``
    - ``matplotlib``
    ```bash
    python -m pip install --upgrade pip setuptools wheel
	python -m pip install --upgrade numpy matplotlib
    ```

## Utilisation

### Démarrage du script

Exécuter dans le dossier du dépôt :
```bash
python -i climat.py
```

Des arguments de script optionnels sont disponibles :
```bash
python -i climat.py [<SIZE> [<ITER> [<DT>]]]
```
ARGUMENT|Description|Valeur par défaut
---|---|---
``SIZE``|Dimension des matrices qui serviront d'environnement|``50``
``ITER``|Nombre d'états successifs à calculer|``10``
``DT``|Facteur de vitesse d'évolution|``10.0``

Par exemple, pour calculer 20 nouveaux états au lieu de 10 :
```bash
python -i climat.py 50 20
```

### Affichage des résultats

Après les calculs initaux, trois fonctions sont disponibles pour afficher les résultats :
- **``frame(t:int)``** affiche les matrices pour l'instant ``t`` (indexé en 0). Si ``t`` est supérieur à ``ITER``, la matrice sera mise à jour avec les états manquants nouvellement calculés.
- **``animate(fps:int=5)``** affiche une animation des matrices.
- **``stats()``** affiche diverses statistiques sur la simulation.
