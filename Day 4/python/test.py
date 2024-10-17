import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Charger les données
file_path = '../data/airline.csv'
df = pd.read_csv(file_path)

# Afficher les informations pour identifier les colonnes et types de données
print(df.info())

# Remplir les valeurs manquantes pour les colonnes numériques
numerical_columns = ['Age', 'Flight Distance', 'Departure Delay in Minutes', 'Arrival Delay in Minutes']
for column in numerical_columns:
    if column in df.columns:
        df[column] = df[column].fillna(df[column].median())

# Remplir les valeurs manquantes pour les colonnes catégoriques
categorical_columns = ['Gender', 'Customer Type', 'Type of Travel', 'Class', 'satisfaction']
for column in categorical_columns:
    if column in df.columns:
        df[column] = df[column].fillna(df[column].mode()[0])

# Remplir les valeurs manquantes pour les colonnes avec des notes (Inflight services)
rating_columns = [
    'Inflight wifi service', 'Ease of Online booking', 'Gate location', 'Food and drink', 'Online boarding', 
    'Seat comfort', 'Inflight entertainment', 'On-board service', 'Leg room service', 'Baggage handling', 
    'Checkin service', 'Inflight service', 'Cleanliness'
]

for column in rating_columns:
    if column in df.columns:
        df[column] = df[column].fillna(df[column].median())  # On peut utiliser la médiane ou le mode

# Visualiser les valeurs manquantes après remplissage
sns.heatmap(df.isnull(), cbar=False)
plt.title('Données après remplissage')
plt.show()
