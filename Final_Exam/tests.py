import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os as os

# chemin de la data stocké dans une variable que l'on va réutiliser
file_path = 'edtech_market_study_usa.csv'

# Vérifier l'existence du fichier
if os.path.exists(file_path):
    print("\n File found, proceeding to load.\n")
else:
    print("File not found, please check the file path.")
    exit()

# Chargement des données
df = pd.read_csv(file_path)
df.head()

# Affichage des 5 premières lignes de notre data
print_value = 5
print(f"{print_value} lignes affichées")
print(df.head(print_value))

#---- verifcation des données manquantes de notre fichier CSV ----

print("\nnombre de valeurs manquantes par colonnes :\n", df.isnull().sum())
print("\nvaleurs manquantes en pourcentage par colonnes :\n", df.isnull().mean() * 100)

# verification puis supression des doublons de notre csv
print("\nNombre de doublons avant suppression :\n", df.duplicated().sum())
df = df.drop_duplicates()
print("\nNombre de doublons après suppression :\n", df.duplicated().sum())

#on print quelques valeurs pour verifier la supression de doublons
print(df.head(print_value))

#on remplis les colonnes avec des données manquantes
df['LATITUDE'] = df['LATITUDE'].fillna('None')
df['LONGITUDE'] = df['LONGITUDE'].fillna('None')
df['A_DISTANCE_SEULEMENT'] = df['A_DISTANCE_SEULEMENT'].fillna('None')


# etablissement avec le plus grand nombre de défaut sur trois ans
defaut_2ans = df[df['DEFAUT_PAIEMENT_2ANNEES'] != 'None'].groupby('ETAT')['DEFAUT_PAIEMENT_2ANNEES'].count().sort_values(ascending=False).head(5)

plt.figure(figsize=(10,6))
sns.barplot(x=defaut_2ans.values, y=defaut_2ans.index, palette='magma')
plt.title('5 etablissement avec le plus fort taux de defaut sur deux ans')
plt.xlabel('nombre de defaut sur deux ans')
plt.ylabel('Académie')
plt.show()

college_cost = df[df['COUT_MOYEN_ANNEE_ACADEMIE'] != 'None'].groupby('NOM')['COUT_MOYEN_ANNEE_ACADEMIE'].count().sort_values(ascending=False).head(5)

plt.figure(figsize=(10,6))
sns.barplot(x=college_cost.values, y=college_cost.index, palette='magma')
plt.title('5 etablissement avec le plus haut coût')
plt.xlabel('coût')
plt.ylabel('Etablissement')
plt.show()

# 
defaut_3ans = df[df['DEFAUT_PAIEMENT_3ANNEES'] != 'None'].groupby('NOM')['DEFAUT_PAIEMENT_3ANNEES'].count().sort_values(ascending=False).head(5)

plt.figure(figsize=(10,6))
sns.barplot(x=defaut_3ans.values, y=defaut_3ans.index, palette='magma')
plt.title('5 etablissement avec le plus haut coût')
plt.xlabel('coût')
plt.ylabel('Etablissement')
plt.show()

#nuage de point avec relations

plt.figure(figsize=(10, 6), dpi=100)
sns.scatterplot(x="DEFAUT_PAIEMENT_3ANNEES", 
                y="COUT_MOYEN_ANNEE_ACADEMIE", 
                hue="AGE_ENTREE", 
                data=df, 
                edgecolor="black", 
                alpha=0.7)
plt.title("Relation defaut / cout academique / age")
plt.xlabel("Defaut de paiement")
plt.ylabel("cout moyen academie")
plt.legend(title='relation entre age et defaut')
plt.tight_layout()
plt.show()
