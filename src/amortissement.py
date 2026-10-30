from pathlib import Path
import pandas as pd

DOSSIER_PROJET = Path(__file__).resolve().parent.parent
DOSSIER_DATA = DOSSIER_PROJET / "data"

DUREE_VIE_ANS = 25
VALEUR_RESIDUELLE = 0.15
PRIX_NEUF_MUSD = {"A320-200": 32.5, "737-800": 33.1}


def valeur_comptable(prix_neuf, age):
    age = min(age, DUREE_VIE_ANS)
    return prix_neuf * (1 - (1 - VALEUR_RESIDUELLE) * age / DUREE_VIE_ANS)

marche = pd.read_csv(DOSSIER_DATA / "valeurs_marche.csv")
marche["prix_neuf"] = marche["modele"].map(PRIX_NEUF_MUSD)
marche["comptable"] = marche["prix_neuf"] * (1 - (1 - VALEUR_RESIDUELLE) * marche["age_ans"].clip(upper=DUREE_VIE_ANS) / DUREE_VIE_ANS)
marche["ecart_pct"] = (marche["valeur_musd"] / marche["comptable"] - 1) * 100
print(marche.round(1).to_string(index=False))

import matplotlib.pyplot as plt

DOSSIER_SORTIE = DOSSIER_PROJET / "output"
ages = list(range(0, 26))

fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
for axe, modele in zip(axes, PRIX_NEUF_MUSD):
    prix = PRIX_NEUF_MUSD[modele]
    axe.plot(ages, [valeur_comptable(prix, a) for a in ages], color="#1f77b4", label="Valeur comptable (25 ans, 15 %)")
    points = marche[marche["modele"] == modele]
    axe.plot(points["age_ans"], points["valeur_musd"], "o-", color="#d95f02", label="Valeur de marché (AVAC 2020)")
    axe.set_title(modele)
    axe.set_xlabel("Âge (ans)")
axes[0].set_ylabel("Valeur (M$)")
axes[0].legend()
plt.tight_layout()
plt.savefig(DOSSIER_SORTIE / "comptable_vs_marche.png", dpi=150)