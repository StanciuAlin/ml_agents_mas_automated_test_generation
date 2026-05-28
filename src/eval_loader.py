import pandas as pd
import os


def inspect_parquet_data(file_path):
    # Verificăm dacă fișierul există
    if not os.path.exists(file_path):
        print(f"❌ Eroare: Nu am găsit fișierul la calea: {file_path}")
        return

    try:
        # Citirea fișierului
        df = pd.read_parquet(file_path)

        print("✅ Fișier încărcat cu succes!")
        print("-" * 30)
        print(f"📊 Număr total de rânduri (eșantioane): {len(df)}")
        print(f"📋 Coloane disponibile: {df.columns.tolist()}")
        print("-" * 30)

        # Afișăm primele 2 rânduri pentru a vedea structura
        print("\n🔍 Exemplu de date (primele 2 rânduri):")
        # De obicei, coloanele importante sunt 'prompt', 'reference_code' sau 'entry_point'
        print(df.head(2))

        # Dacă vrei să vezi codul sursă al primei funcții:
        if 'prompt' in df.columns:
            print("\n💻 Codul sursă al primului eșantion:")
            print(df['prompt'].iloc[0])

    except Exception as e:
        print(f"❌ A apărut o eroare la citire: {e}")


if __name__ == "__main__":
    # Calea către fișierul descărcat de tine
    DATA_PATH = "evaluation/testgeneval/data/test-00000-of-00001.parquet"
    inspect_parquet_data(DATA_PATH)
