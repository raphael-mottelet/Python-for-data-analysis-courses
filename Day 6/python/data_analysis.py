import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os as os

# Spécifier le chemin du fichier CSV
file_path = '../data/athlete_events.csv'

# Vérifier l'existence du fichier
if os.path.exists(file_path):
    print("\n File found, proceeding to load.\n")
else:
    print("File not found, please check the file path.")
    exit()

# Charger les données
df = pd.read_csv(file_path)

# Remplir les valeurs manquantes pour 'Age', 'Height', et 'Weight'
df['Age'] = df['Age'].fillna(df['Age'].median())
df['Height'] = df['Height'].fillna(df['Height'].median())
df['Weight'] = df['Weight'].fillna(df['Weight'].median())

# Afficher les premières lignes
print_value = 5
print(f"{print_value} lignes affichées")
print(df.head(print_value))

# Vérification des valeurs manquantes
print("\nnombre de valeurs manquantes par colonnes :\n", df.isnull().sum())
print("\nvaleurs manquantes en pourcentage par colonnes :\n", df.isnull().mean() * 100)

# Vérification des doublons
print("\nNombre de doublons avant suppression :", df.duplicated().sum())

# Supprimer les doublons
df = df.drop_duplicates()

# Vérification après suppression des doublons
print("\nNombre de doublons après suppression :", df.duplicated().sum())

# Afficher quelques lignes pour vérifier la suppression
print(df.head(print_value))

# Remplir les valeurs manquantes dans la colonne 'Medal'
df['Medal'] = df['Medal'].fillna('None')

# --- Analyses demandées et visualisations ---

# 1. Quel pays a le plus grand nombre d'athlètes ?
country_athletes_count = df.groupby('NOC')['ID'].nunique().sort_values(ascending=False).head(5)

plt.figure(figsize=(10,6))
sns.barplot(x=country_athletes_count.index, y=country_athletes_count.values, palette='viridis')
plt.title('Top 5 des pays avec le plus grand nombre d\'athlètes')
plt.xlabel('Pays (NOC)')
plt.ylabel('Nombre d\'athlètes uniques')
plt.show()

# 2. Quel athlète est le plus médaillé ?
athlete_medals_count = df[df['Medal'] != 'None'].groupby('Name')['Medal'].count().sort_values(ascending=False).head(5)

plt.figure(figsize=(10,6))
sns.barplot(x=athlete_medals_count.values, y=athlete_medals_count.index, palette='magma')
plt.title('Top 5 des athlètes les plus médaillés')
plt.xlabel('Nombre de médailles')
plt.ylabel('Athlète')
plt.show()


# 3. Quel pays a le plus de médailles ?
country_medals_count = df[df['Medal'] != 'None'].groupby('NOC')['Medal'].count().sort_values(ascending=False).head(5)

plt.figure(figsize=(10,6))
sns.barplot(x=country_medals_count.index, y=country_medals_count.values, palette='inferno')
plt.title('Top 5 des pays avec le plus de médailles')
plt.xlabel('Pays (NOC)')
plt.ylabel('Nombre de médailles')
plt.show()


# Filtrer uniquement les athlètes qui ont gagné des médailles
df_medalists = df[df['Medal'] != 'None']

# Créer un nuage de points pour la relation entre l'âge et le nombre de médailles
athlete_age_medals = df_medalists.groupby(['Name', 'Age'])['Medal'].count().reset_index()

plt.figure(figsize=(10,6))
sns.scatterplot(x='Age', y='Medal', data=athlete_age_medals, hue='Medal', palette='coolwarm', size='Medal', sizes=(20, 200))
plt.title('Relation entre l\'âge des athlètes et le nombre de médailles')
plt.xlabel('Âge de l\'athlète')
plt.ylabel('Nombre de médailles gagnées')
plt.show()