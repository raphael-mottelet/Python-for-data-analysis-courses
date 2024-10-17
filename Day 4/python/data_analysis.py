import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

# Spécifier le chemin du fichier CSV
file_path = '../data/airline.csv'

# Vérifier l'existence du fichier
if os.path.exists(file_path):
    print("\nFile found, proceeding to load.\n")
else:
    print("File not found, please check the file path.")
    exit()

# Charger les données
df = pd.read_csv(file_path)

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

# Remplir les valeurs manquantes dans la colonne 'Arrival Delay in Minutes'
df['Arrival Delay in Minutes'] = df['Arrival Delay in Minutes'].fillna(df['Arrival Delay in Minutes'].median())

# --- Analyses demandées et visualisations ---

# 1. Quelle est la classe de voyage la plus populaire ?
travel_class_count = df['Class'].value_counts().head(5)

plt.figure(figsize=(10, 6))
sns.barplot(x=travel_class_count.index, y=travel_class_count.values, palette='viridis')
plt.title('Classe de voyage la plus populaire')
plt.xlabel('Classe')
plt.ylabel('Nombre de voyageurs')
plt.show()

# 2. Quel est le type de satisfaction des clients ?
satisfaction_count = df['satisfaction'].value_counts()

plt.figure(figsize=(10, 6))
sns.barplot(x=satisfaction_count.index, y=satisfaction_count.values, palette='magma')
plt.title('Répartition du niveau de satisfaction des clients')
plt.xlabel('Satisfaction')
plt.ylabel('Nombre de clients')
plt.show()

# 3. Quel genre de clients sont les plus satisfaits ?
# Modification: barres séparées pour chaque niveau de satisfaction par genre
satisfaction_gender_count = df.groupby(['Gender', 'satisfaction']).size().unstack()

plt.figure(figsize=(10, 6))
satisfaction_gender_count.plot(kind='bar', colormap='plasma', edgecolor='black')
plt.title('Niveau de satisfaction des clients par genre')
plt.xlabel('Genre')
plt.ylabel('Nombre de clients')
plt.xticks(rotation=0)
plt.legend(title='Satisfaction')
plt.tight_layout()
plt.show()

# 4. Temps moyen de retard à l'arrivée par type de client
avg_arrival_delay = df.groupby('Customer Type')['Arrival Delay in Minutes'].mean().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x=avg_arrival_delay.index, y=avg_arrival_delay.values, palette='coolwarm')
plt.title('Temps moyen de retard à l\'arrivée par type de client')
plt.xlabel('Type de client')
plt.ylabel('Retard moyen à l\'arrivée (minutes)')
plt.show()

# --- Ajout des statistiques descriptives (médiane et quartiles) ---

# Calcul de la médiane et des quartiles pour certaines colonnes
def calculate_statistics(column):
    median = df[column].median()
    quartiles = df[column].quantile([0.25, 0.5, 0.75, 1.0])
    print(f"\nStatistiques pour '{column}':")
    print(f"Médiane: {median}")
    print(f"1er quartile: {quartiles[0.25]}")
    print(f"2ème quartile (médiane): {quartiles[0.5]}")
    print(f"3ème quartile: {quartiles[0.75]}")
    print(f"4ème quartile: {quartiles[1.0]}")

# Appliquer la fonction sur des colonnes spécifiques
calculate_statistics('Arrival Delay in Minutes')
calculate_statistics('Flight Distance')

# --- Ajout du scatter plot : Retard de départ vs Retard d'arrivée, coloré par satisfaction ---

plt.figure(figsize=(10, 6), dpi=100)
sns.scatterplot(x="Departure Delay in Minutes", 
                y="Arrival Delay in Minutes", 
                hue="satisfaction", 
                data=df, 
                edgecolor="black", 
                alpha=0.7)
plt.title("Relation entre le retard de départ et le retard d'arrivée")
plt.xlabel("Retard de départ (minutes)")
plt.ylabel("Retard d'arrivée (minutes)")
plt.legend(title='Satisfaction')
plt.tight_layout()
plt.show()

# --- Ajout des violin plots : Distribution des retards par satisfaction ---

num_vars = ['Departure Delay in Minutes', 'Arrival Delay in Minutes']

fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(20, 8))
axs = axs.flatten()

for i, var in enumerate(num_vars):
    sns.violinplot(x='satisfaction', y=var, data=df, ax=axs[i])
    axs[i].set_title(f'Distribution de {var} par niveau de satisfaction')
    axs[i].set_xlabel('Satisfaction')
    axs[i].set_ylabel(var)

plt.tight_layout()
plt.show()

# --- Ajout du nuage de points avec jittering pour éviter l'alignement des points ---

# Filtrer uniquement les clients satisfaits
df_satisfied = df[df['satisfaction'] == 'satisfied']

# Relation entre la distance de vol et le service Wifi en vol (clients satisfaits)
plt.figure(figsize=(10, 6))

# Utilisation de 'stripplot' avec jittering pour disperser les points
sns.stripplot(x='Flight Distance', 
               y='Inflight wifi service', 
               data=df_satisfied, 
               color="blue", 
               alpha=0.5, 
               jitter=True,  # Ajout du jitter pour disperser les points
               size=5)

plt.title('Relation entre la distance de vol et le service Wifi en vol (clients satisfaits)')
plt.xlabel('Distance de vol')
plt.ylabel('Service Wifi en vol')
plt.tight_layout()
plt.show()
