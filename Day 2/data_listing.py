import pandas as pd
import os
import matplotlib.pyplot as plt

file_path = 'data/cis_bdpm.txt'

if os.path.exists(file_path):
    print("File found, proceeding to load.\n")
else:
    print("File not found, please check the file path.")
    exit()

df_spe = pd.read_csv(file_path, sep='\t', header=None, encoding='iso-8859-1')

new_headers = [
    'ID', 
    'Code CIS', 
    'Dénomination', 
    'Forme Pharmaceutique', 
    'Voies Administration', 
    'Statut Administratif', 
    'Type Procédure', 
    'Etat Commercialisation', 
    'Date AMM', 
    'Statut Bdm', 
    'Numéro Autorisation', 
    'Titulaires'
]

if len(df_spe.columns) == len(new_headers):
    df_spe.columns = new_headers

df_spe['Statut Administratif'] = df_spe['Statut Administratif'].str.strip()

active_authorizations = df_spe[df_spe['Statut Administratif'] == 'Autorisation active']

if active_authorizations.empty:
    print("No active authorizations found.")
    status_counts = df_spe['Statut Administratif'].value_counts()
    print("\nCount of each status in 'Statut Administratif':")
    print(status_counts)
    
    plt.figure(figsize=(10, 6))
    status_counts.plot(kind='bar', color='salmon')
    plt.title('Count of Each Status in Statut Administratif')
    plt.xlabel('Status')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()
else:
    titulaires_counts = active_authorizations['Titulaires'].value_counts().head(10)

    if titulaires_counts.empty:
        print("No Titulaires found with active authorizations.")
    else:
        plt.figure(figsize=(12, 6))
        titulaires_counts.plot(kind='bar', color='skyblue')
        plt.title('Top 10 Titulaires with Most Active Authorizations')
        plt.xlabel('Titulaires')
        plt.ylabel('Number of Active Authorizations')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y')
        plt.tight_layout()
        plt.show()

        print("Top 10 Titulaires with Most Active Authorizations:")
        print(titulaires_counts)
