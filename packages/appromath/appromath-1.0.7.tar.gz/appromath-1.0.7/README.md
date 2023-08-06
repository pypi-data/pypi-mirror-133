# Bienvenue sur le guide de Appromath !
Le but de Appromath est de donner avec la plus grande précision possible la valeur approchée du sinus de tout nombre réel (angle en radians modulo 2pi).

Cette précision théorique est de l'ordre de 10<sup>-100</sup> et utilise les formules de Taylor-Lagrange pour les développements limités et les suites de Cauchy pour en certifier la convergence donc la stabilité et la précision.

Ce module a été réalisé dans un but scolaire par Ibrahima BAH, Kévin HENTZ, Alexandre RAMDOO et Henri MACEDO GONCALVES.

## Exemple d'utilisation

### 1. Installation
```shell script
pip install appromath
``` 
ou encore
```shell script
python3 -m pip install appromath
```

### 2. Import
```python
import appromath
```
ou encore
```python
from appromath import *
```

### 3. Obtention du sinus de pi/2 rad
```python
import math
valeur = appromath.classe_General(math.sin(math.pi/2))
```

## DISCLAIMER
Ce module n'a pas vocation à remplacer le module de base math. Il est réalisé à titre scolaire et les auteurs ne sauraient en aucun cas être tenus responsables de sa mauvaise utilisation.