import pandas as pd

researchers = pd.read_csv('./data/raw/researchers.csv')
print("Dataset shape (rows, columns):")
print(researchers.shape)

print("\nData types of each column:")
print(researchers.dtypes)

print("\nFirst 5 rows of the dataset:")
print(researchers.head())

print("\nLast 5 rows of the dataset:")
print(researchers.tail())

print("\nStatistical summary of numerical columns:")
print(researchers.describe())

print("\nNumber of missing values in each column:")
print(researchers.isnull().sum())


researchers_filtered= researchers[(researchers['is_active']== True) & (researchers['h_index']>15)]
print(researchers_filtered.head())

researchers_filtered = researchers_filtered.sort_values(by='joined_year', ascending=True)
print(researchers_filtered.head())

researchers_filtered['message'] = researchers_filtered['last_name'].apply(
    lambda x: f"The first is {x[0]}"
)
print(researchers_filtered[['last_name', 'message']])

# publications dataset
publications= pd.read_json('./data/raw/publications.json')
print(publications.head())
print(publications.info())

print(publications.loc[publications['citations'].idxmax(), 'title'])

def funding_clean(df):
    df = df.copy()
    # check nulls 
    if df.isnull().sum().sum()> 0 :
        df = df.dropna()
    # remove negatives if exist
    if 'amount_cad' in df.columns:
       df = df[df['amount_cad'] >= 0]
    # make sure of data types
    print(df.info())
    print(df.isnull().sum())
    print(df[df['amount_cad'] < 0])

    return df  

funding= pd.read_excel('./data/raw/funding.xlsx')
print(funding.info())
funding= funding_clean(funding)

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
 
# Answer questions:
# 1- Which researcher has the highest total citations?

# Group data by researcher_id and sum all citations per researcher
citations_per_researcher = merge_inner.groupby('researcher_id')['citations'].sum()

# Sort researchers by total citations (highest first) and take the top one
top_researcher = citations_per_researcher.sort_values(ascending=False).head(1)

# Print the researcher with the highest total citations
print(top_researcher)


# 2- Which field received the most total funding?
# Group data by field and sum total funding for each field
funding_per_field = merge_inner.groupby('field')['amount_cad'].sum()

# Sort fields by total funding (highest first) and get the top one
top_field = funding_per_field.sort_values(ascending=False).head(1)

# Print the field with the highest total funding
print(top_field)

# 3- Who joined earliest and still active?
# Filter only active researchers
active_researchers = merge_inner[merge_inner['status'] == 'active']

# Find the row with the earliest year_awarded
earliest_researcher = active_researchers.loc[active_researchers['year_awarded'].idxmin()]

# Print the researcher details
print(earliest_researcher[['researcher_id', 'year_awarded', 'status']])

# save the merged and cleaned dataframe to a new csv
merge_inner.to_csv("./data/processed/merged_data.csv", index=False)