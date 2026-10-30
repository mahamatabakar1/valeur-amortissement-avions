from pathlib import Path
import pandas as pd

DOSSIER_PROJET = Path(__file__).resolve().parent.parent
DOSSIER_RAW = DOSSIER_PROJET / "data" / "raw"


def lire_faa(nom, colonnes):
    tableau = pd.read_csv(DOSSIER_RAW / nom, dtype=str, encoding="utf-8-sig", encoding_errors="replace", index_col=False)
    tableau.columns = tableau.columns.str.strip()
    tableau = tableau[colonnes]
    return tableau.apply(lambda colonne: colonne.str.strip())


master = lire_faa("MASTER.txt", ["N-NUMBER", "MFR MDL CODE", "YEAR MFR", "NAME", "STATUS CODE"])
reference = lire_faa("ACFTREF.txt", ["CODE", "MFR", "MODEL"])
avions = master.merge(reference, left_on="MFR MDL CODE", right_on="CODE", how="left")

def classer(modele):
    if modele.startswith(("A320-2", "A320-1")) and not modele.endswith("N"):
        return "A320-200"
    if modele.startswith("737-8") and modele not in ("737-8", "737-8200", "737-8-200"):
        return "737-800"
    return None


avions["famille"] = avions["MODEL"].fillna("").map(classer)
flotte = avions[(avions["famille"].notna()) & (avions["STATUS CODE"] == "V")].copy()
flotte["annee"] = pd.to_numeric(flotte["YEAR MFR"], errors="coerce")
flotte = flotte[(flotte["annee"] >= 1985) & (flotte["annee"] <= 2026)]
flotte["age"] = 2026 - flotte["annee"]
print(flotte.groupby("famille").agg(avions=("age", "size"), age_moyen=("age", "mean")).round(1))

PRIX_NEUF_MUSD = {"A320-200": 32.5, "737-800": 33.1}
DUREE_VIE_ANS = 25
VALEUR_RESIDUELLE = 0.15

flotte["prix_neuf"] = flotte["famille"].map(PRIX_NEUF_MUSD)
flotte["age_plafonne"] = flotte["age"].clip(upper=DUREE_VIE_ANS)
flotte["valeur_musd"] = flotte["prix_neuf"] * (1 - (1 - VALEUR_RESIDUELLE) * flotte["age_plafonne"] / DUREE_VIE_ANS)

print(flotte["valeur_musd"].sum().round(0), "M$ pour", len(flotte), "avions")
print(flotte.groupby("NAME").agg(avions=("valeur_musd", "size"), valeur_musd=("valeur_musd", "sum")).sort_values("valeur_musd", ascending=False).head(10).round(0))