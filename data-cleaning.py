import pandas as pd

df = pd.read_csv('https://gist.githubusercontent.com/armgilles/194bcff35001e7eb53a2a8b441e8b2c6/raw/92200bc0a673d5ce2110aaad4544ed6c4010f687/pokemon.csv')
df.rename(columns={'#':'Id', 'Type 1':'Type1', 'Type 2':'Type2', 'Sp. Atk':'Sp.Atk', 'Sp. Def': 'Sp.Def'}, inplace=True)
df = df[~df['Name'].str.contains('Mega')]
df.to_csv('pokemon.csv', index=False)