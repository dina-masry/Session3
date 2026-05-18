import pandas as pd 

df= pd.read_json('./data/publications.json')
print(df.head())
print(df.info())

print(df.loc[df['citations'].idxmax(), 'title'])