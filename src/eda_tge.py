import os
import pandas as pd
import matplotlib.pyplot as plt

# (e.g.: src/)
base_dir = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(base_dir, "..", "evaluation", "testgeneval", "data", "nume_fisier.parquet")

print(f"Caut fișierul la: {os.path.abspath(file_path)}")

if os.path.exists(file_path):
    df = pd.read_parquet(file_path)
    print("Succes! Fișier încărcat.")
else:
    print("Eroare: Fișierul nu a fost găsit. Verifică structura folderelor.")

# Load the dataset
df = pd.read_parquet(file_path)

print("--- First 5 Rows ---")
print(df.head())

print("\n--- Column Structure ---")
print(df.info())

# 2. Vedem un exemplu de cod sursă (presupunând că avem o coloană 'code' sau 'prompt')
# TestGenEval are de obicei coloane precum 'instruction', 'code', 'test_case'
if 'code' in df.columns:
    print("\n--- Exemplu de Cod Sursă ---")
    print(df['code'].iloc[0])
    
def generate_eda_charts(df):
    # 1. Code legth distribution in characters or words
    df['code_len'] = df['code'].str.len()
    
    plt.figure(figsize=(10, 6))
    plt.hist(df['code_len'], bins=50, color='skyblue', edgecolor='black')
    plt.title('Code Length Distribution (in characters)')
    plt.xlabel('Number of Characters')
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=0.75)
    plt.savefig('code_length_dist.png') # Salvează graficul pentru raport
    print("Chart saved as 'code_length_dist.png'")

generate_eda_charts(df)