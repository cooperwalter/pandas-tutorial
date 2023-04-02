import pandas as pd
import re

### Data Analysis with Pandas ###
#### from https://www.youtube.com/watch?v=vmEHCJofslg ####

## Load data into pandas
poke = pd.read_csv('pokemon_data.csv')
# poke_excel = pd.read_excel('pokemon_data.xlsx')
# poke_tsv = pd.read_csv('pokemon_data.txt', delimiter='\t')

## read columns
# poke.columns

## Read first 5 row Names
# print(poke['Name'][0:5])

## Iterate through rows
# for index, row in poke.iterrows():
#   print(index, row["Name"])

## Get only Grass type Pokemon
# print(poke.loc[poke['Type 1'] == "Grass"])

## Get stats on dataset
# print(poke.describe())

## Sort by alphabetical name order
# print(poke.sort_values('Name', ascending=False))

## Sort by multiple columns (ascending for Type 1, descending for HP)
# print(poke.sort_values(['Type 1', 'HP'], ascending=[1,0]))

## Add a StatsTotal column
poke["StatsTotal"] = poke['HP'] + poke['Attack'] + poke['Defense'] + poke['Sp. Atk'] + poke['Sp. Def'] + poke['Speed']
# OR
# axis=1 means sum across columns, axis=0 means sum across rows
# poke["StatsTotal"] = poke.loc[:, "HP":"Speed"].sum(axis=1)
# print(poke[['Name', 'StatsTotal']])

## Move a column
cols = list(poke.columns.values)
# be careful when using hardcoded indices
poke = poke[cols[0:4] + [cols[-1]] + cols[4:12]]

## Drop a column
# print(poke.columns)
# poke = poke.drop(columns=['StatsTotal'])
# print(poke.columns)

## Write to csv
# Do not write index column to csv
# poke.to_csv('modified.csv', index=False)

## Write to excel
# poke.to_excel('modified.xlsx', index=False)

## Write to tsv
# poke.to_csv('modified.txt', index=False, sep='\t')

### Filtering Data
# print(poke[poke['Type 1'] == "Grass"])
# Must separate conditions with parentheses
# use & instead of and for multiple conditions
new_poke = poke[(poke['Type 1'] == 'Grass') & (poke['Type 2'] == 'Poison') & (poke['HP'] > 70)]
print(new_poke)
new_poke.to_csv('grass-poison.csv', index=False)

# Old index remains in play unless reset
new_poke = new_poke.reset_index(drop=True)

# Remove all megas
megas_mask = poke['Name'].str.contains('Mega')
# print(megas_mask)
no_megas = poke[~megas_mask]
print(no_megas)

# Get only grass and fire pokemon
fire_and_grass = poke[poke['Type 1'].str.contains('Fire|Grass', flags=re.I, regex=True) | poke['Type 2'].str.contains('Fire|Grass', flags=re.I, regex=True)]
print(fire_and_grass)

### Conditional Changes
## Rename "Fire" type to "Flamer" type
now_flamer = poke.loc[poke['Type 1'] == 'Fire', 'Type 1'] = 'Flamer'
print(poke)

## Modify multiple columns at once
poke.loc[poke['StatsTotal'] > 500, ['Generation', 'Legendary']] = ['Test 1', 'Test 2']

### Aggregate Statistics (groupby)
## Highest defense by type
print(poke.groupby(['Type 1']).mean().sort_values('Defense', ascending=False))
## Highest total stats by type
print(poke.groupby(['Type 1']).mean().sort_values('StatsTotal', ascending=False))

## Count number of each type
poke['count'] = 1
print(poke.groupby(['Type 1']).count()['count'].sort_values(ascending=False))

### Working with large amounts of data
## You can read in a large file chunks at a time
# you'll need to do some math/guesswork if you want to read in a 
# general memory size worth of rows
# read in 100 rows at a time
for df in pd.read_csv('pokemon_data.csv', chunksize=100):
  print(df.head(1))

# can read chunks then shrink dataframe then save to a new dataframe
my_df = pd.DataFrame()
for df in pd.read_csv('pokemon_data.csv', chunksize=100):
  # initialize my_df on first iteration
  if (my_df.empty):
    my_df = pd.DataFrame(columns=df.columns)
  results = df.groupby(['Type 1']).count()
  my_df = pd.concat([my_df, results])
  
print(results)