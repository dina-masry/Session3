import pandas as pd

df= pd.read_excel('./data/funding.xlsx')
print(df.info())

print(df['amount_cad'].isna().sum())

df= df.dropna(subset='amount_cad')

print(df['amount_cad'].isna().sum())

print(df['amount_cad'].value_counts())

df = df[df['amount_cad'] >= 0]

print(df['amount_cad'].sum())