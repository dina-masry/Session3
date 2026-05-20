import pandas as pd 

researchers = pd.read_csv('./data/researchers.csv')
publications = pd.read_json('./data/publications.json')
funding = pd.read_excel('./data/funding.xlsx')

# Inner
# Keeps only rows with matching researcher_id in all datasets
merge_inner = pd.merge(researchers,publications, how='inner')
merge_inner = pd.merge(merge_inner, funding, how='inner')

# Display basic information about the merged dataset
print(merge_inner.shape)
print(merge_inner.info())
print(merge_inner.head())
print(merge_inner.isnull().sum())

# Left
# Keeps all rows from researchers dataset
# Missing matches from other datasets become NaN
merge_left = pd.merge(researchers, publications, on='researcher_id', how='left')
merge_left = pd.merge(merge_left, funding,on='researcher_id', how='left')

# Display basic information about the merged dataset
print(merge_left.shape)
print(merge_left.info())
print(merge_left.head())
print(merge_left.isnull().sum())

# Inner join keeps only matching researcher_id values across all datasets.
# This removes researchers that do not have publication or funding records.

# Left join keeps all researchers from the main dataset.
# Missing matches from publications or funding appear as NaN values.

# Rows lost in the inner join represent unmatched records
# that existed in the researchers dataset but not in all datasets.

# How many rows lost in inner join?
lost_rows = merge_left.shape[0] - merge_inner.shape[0]
print("Rows lost in inner join:", lost_rows)
