# 📸 RetroColor Engine : Renaissance des Images Anciennes

## Le concept
Vous avez déjà vu ces vieilles plaques photographiques du début du 20ème siècle ? Elles sont souvent en noir et blanc, mais cachent en réalité une image couleur ! À l'époque, on prenait trois photos à la suite avec des filtres différents (Rouge, Vert, Bleu). 

Le problème ? En quelques secondes, le sujet a bougé, ou l'appareil a légèrement vibré. Si on superpose les trois photos bêtement, on obtient une image floue avec des arcs-en-ciel bizarres sur les bords. **RetroColor Engine utilise le code pour réaligner tout ça parfaitement et recréer la photo telle qu'on l'aurait vue en vrai.**

---

##  Le Processus Technique

### 1. Décomposition des canaux
L'image source est d'abord séparée en ses trois composantes fondamentales. C'est ici qu'on voit les décalages qui gâchent l'image finale.

| Canal Bleu | Canal Vert | Canal Rouge |
| :---: | :---: | :---: |
| ![Bleu](assets/part1.png) | ![Vert](assets/part2.png) | ![Rouge](assets/part3.png) |

### 2. Algorithme de Recalage (Matching)
Le cœur du moteur. Le script fait glisser les images les unes sur les autres au pixel près. Pour savoir quand elles sont bien alignées, j'utilise l'**Information Mutuelle**. C'est un concept mathématique qui dit : "Plus ces deux images se ressemblent statistiquement, plus on brûle !".

### 3. Fusion et Résultat Final
Une fois que le moteur a trouvé le décalage parfait, il fusionne les trois couches. Le résultat ? Une image nette, vibrante, qui semble avoir été prise hier.

![Résultat Final](assets/ImageRRecalée.png) 
*(Exemple de couche recalée au final)*

---

##  Structure du projet

*   **`src/`** : Cœur de l'application.
    *   `engine.py` : Le moteur principal de recalage.
    *   `utils.py` : Fonctions utilitaires de traitement d'image.
    *   `legacy_processor.py` : Ancienne version de l'algorithme (sauvegarde).
*   **`data/`** : Gestion des données.
    *   `raw/` : Images sources originales.
    *   `output/` : Résultats du traitement.
*   **`assets/`** : Ressources pour la documentation.

---

##  Les outils derrière le moteur
*   **Python** : Le chef d'orchestre.
*   **NumPy** : Pour manipuler les images comme des grands tableaux de chiffres.
*   **Matplotlib** : Pour la visualisation et le rendu.
*   **Scikit-Image** : Pour la précision chirurgicale des translations.

---

## 🎯 Ce que j'ai appris
Ce projet m'a permis de transformer des maths pures (statistiques, matrices) en quelque chose de visuel et d'émouvant. J'ai appris à gérer le "bruit" dans les données et à faire comprendre à un ordinateur la notion de "ressemblance" visuelle.

---
*Développé avec passion pour sauver le patrimoine visuel.*
