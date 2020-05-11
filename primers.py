#!/bin/python 3
'''
this program can be run from a terminal with a command
python primer.py QSOX ABCB10 ABCC1
In PyCharm -> edit Configurations -> in the Parameter field type QSOX ABCCB10 ABCC1
Requires an excel document Primers.xlsx to be located in the folder where is the program
change the path to your own
Additional packages: pandas
'''
# importing necessary modules
import sys
import pandas as pd
from datetime import date

# defining a function found_gene
found_gene = False

def find_gene(var, length):
    if (length < 2):
        print(var + ' is not found. Check your spelling!')
        return
    found_match_count = 0
    for index, row in df.iterrows():
        if row['Gene'].lower()[:length] == var.lower()[:length]:
            if (len(row['Gene']) != length and found_match_count == 0):
                print('Exact match not found... maybe you meant:')
            print('Gene: ', row['Gene'], '\tBox: ', row['BOX'], '\tPosition: ', row['Position'])
            found_match_count += 1
            found_gene = True
        if (found_match_count > 5):
            return
    if (found_match_count == 0):
        find_gene(var, length - 1)

# loading excel as a df
df = pd.read_excel(r'C:\Projects\Weather\py\Primers.xlsx', sheet_name='ALL')

# Cleaning the dataframe
df.drop('A', axis=1, inplace=True)
df.columns = ['Gene', 'BOX', 'Position']
df.drop(df.index[[0, 1]], inplace=True)
df.reset_index(inplace=True)
df.drop('index', axis=1, inplace=True)
# filling NaN values
df['Gene'].fillna(method='ffill', inplace=True)
df['BOX'].fillna(method='ffill', inplace=True)
df.head()

#getting an input from user
program, *parameters = sys.argv

#looking for the rows we are interested in
print('The result of your search on ', date.today(), ' is below.')
for parameter in parameters:
    output = find_gene(parameter, len(parameter))

