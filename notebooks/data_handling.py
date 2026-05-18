import pandas as pd

df = pd.read_csv('./data/researchers.csv')
print("Dataset shape (rows, columns):")
print(df.shape)

print("\nData types of each column:")
print(df.dtypes)

print("\nFirst 5 rows of the dataset:")
print(df.head())

print("\nLast 5 rows of the dataset:")
print(df.tail())

print("\nStatistical summary of numerical columns:")
print(df.describe())

print("\nNumber of missing values in each column:")
print(df.isnull().sum())


df_filtered= df[(df['is_active']== True) & (df['h_index']>15)]
print(df_filtered.head())

df_filtered = df_filtered.sort_values(by='joined_year', ascending=True)
print(df_filtered.head())

df_filtered['message'] = df_filtered['last_name'].apply(
    lambda x: f"The first is {x[0]}"
)
print(df_filtered[['last_name', 'message']].head())