# Valeur et amortissement des avions

Projet Python d'estimation de la valeur et de l'amortissement d'un avion commercial. Deuxième projet d'un portefeuille orienté aviation et leasing d'avions.a

## Méthode

Trois approches sont comparées pour l'A320-200 et le 737-800 :

- Valeur comptable : amortissement linéaire sur 25 ans jusqu'à une valeur résiduelle de 15 % du prix neuf (règle appliquée aux avions de ligne par un bailleur coté, document déposé auprès de la SEC pour l'exercice clos le 28 février 2025).
- Valeur de marché 2020 : estimations de l'évaluateur AVAC, publiées par Aviation Strategy (octobre 2020), à 0, 5, 10 et 20 ans.
- Valeur de marché 2026 : fourchettes indicatives d'Avialinker (3e trimestre 2026).

## Résultats

La valeur de marché de 2020 est inférieure à la valeur comptable à tous les âges : pour l'A320-200, de 7 % à 5 ans, de 18 % à 10 ans et de 24 % à 20 ans ; pour le 737-800, de 5 %, 32 % et 22 %. Les fourchettes de 2026 sont plus élevées que les valeurs de 2020 à 10 ans, et la valeur comptable y tombe à l'intérieur.

Graphique : output/comptable_vs_marche.png
Script : src/amortissement.py

## Limites

- Les valeurs AVAC sont des estimations d'évaluateur saisies à la main depuis un tableau publié, pas des prix de transaction.
- Avialinker précise que ses valeurs sont orientatives, qu'elles ne constituent pas une évaluation ISTAT et qu'elles ne sont pas destinées au financement. Ses sources ne sont pas détaillées.
- Le prix neuf utilisé est la valeur « neuf » d'AVAC 2020, pas un prix catalogue.
- Les deux sources sont de nature différente : la comparaison entre 2020 et 2026 reste indicative.
- Seuls deux modèles sont couverts.