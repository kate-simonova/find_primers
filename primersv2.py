#!/bin/python 3
'''
this program can be run from a terminal with a command
python primersv2.py QSOX ABCB10 ABCC1
In PyCharm -> edit Configurations -> in the Parameter field type QSOX ABCCB10 ABCC1
Requires an excel document Primers.xlsx to be located in the folder where is the program
Additional packages: pandas
'''
# importing necessary modules
import sys
import pandas as pd
from datetime import date
import csv

# loading excel as a df
df = pd.read_excel(r'Primers.xlsx', sheet_name='ALL')

found_gene = False

# defining function find_gene
def find_gene(var, length):
    if (length < 2):
        print(var + ' is not found. Check your spelling!', file=primers_out)
        return
    found_match_count = 0
    for index, row in df.iterrows():
        if row['Gene'].lower()[:length] == var.lower()[:length]:
            if (len(row['Gene']) != length and found_match_count == 0):
                print(f'Exact match not found for {var} ... maybe you meant:', file=primers_out)
            primers_writer.writerow(['Gene: ', row['Gene'], '\tBox: ', row['BOX'], '\tPosition: ', row['Position']])
            found_match_count += 1
            found_gene = True
        if (found_match_count > 5):
            return
    if (found_match_count == 0):
        find_gene(var, length - 1)

# Cleaning the dataframe
df.drop('A', axis=1, inplace=True)
df.columns = ['Gene', 'BOX', 'Position']
df.drop(df.index[[0, 1]], inplace=True)
df.reset_index(inplace=True)
df.drop('index', axis=1, inplace=True)
# filling NaN values
df['Gene'].fillna(method='ffill', inplace=True)
df['BOX'].fillna(method='ffill', inplace=True)

# getting an input from user
program, *parameters = sys.argv

# looking for the rows we are interested in
# writing to a file
with open('your_search.csv', 'a', newline='') as primers_out:
    primers_writer = csv.writer(primers_out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    print('\nThe result of your search on ', date.today(), ' is below.\n', file=primers_out)
    for parameter in parameters:
        find_gene(parameter, len(parameter))
