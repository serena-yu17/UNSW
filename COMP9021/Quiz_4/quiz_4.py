# Uses data available at http://data.worldbank.org/indicator
# on Forest area (sq. km) and Agricultural land area (sq. km).
# Prompts the user for two distinct years between 1990 and 2004
# as well as for a strictly positive integer N,
# and outputs the top N countries where:
# - agricultural land area has increased from oldest input year to most recent input year;
# - forest area has increased from oldest input year to most recent input year;
# - the ratio of increase in agricultural land area to increase in forest area determines
#   output order.
# Countries are output from those whose ratio is largest to those whose ratio is smallest.
# In the unlikely case where many countries share the same ratio, countries are output in
# lexicographic order.
# In case fewer than N countries are found, only that number of countries is output.


# Written by *** and Eric Martin for COMP9021


import sys
import os
import csv
from collections import defaultdict

agricultural_land_filename = 'API_AG.LND.AGRI.K2_DS2_en_csv_v2.csv'
if not os.path.exists(agricultural_land_filename):
    print(f'No file named {agricultural_land_filename} in working directory, giving up...')
    sys.exit()
forest_filename = 'API_AG.LND.FRST.K2_DS2_en_csv_v2.csv'
if not os.path.exists(forest_filename):
    print(f'No file named {forest_filename} in working directory, giving up...')
    sys.exit()
try:
    years = {int(year) for year in
             input('Input two distinct years in the range 1990 -- 2014: ').split('--')
             }
    if len(years) != 2 or any(year < 1990 or year > 2014 for year in years):
        raise ValueError
except ValueError:
    print('Not a valid range of years, giving up...')
    sys.exit()
try:
    top_n = int(input('Input a strictly positive integer: '))
    if top_n < 0:
        raise ValueError
except ValueError:
    print('Not a valid number, giving up...')
    sys.exit()

countries = []


# Insert your code here
#
def p_sort(lst, n):
    if n >= len(lst):
        return
    for i in range(n):
        for j in range(i + 1, len(lst)):
            if lst[j][0] > lst[i][0] or (lst[j][0] == lst[i][0] and lst[j][1] < lst[i][1]):
                lst[i], lst[j] = lst[j], lst[i]


year_1 = min(years)
year_2 = max(years)
y1 = year_1 - 1990 + 34
y2 = year_2 - 1990 + 34
agri = dict()
with open(agricultural_land_filename, 'r', encoding='utf-8') as f:
    csvdoc = csv.reader(f)
    for row in csvdoc:
        if len(row) > y2 and row[3] == "AG.LND.AGRI.K2" and row[y2] != '' and row[y1] != '':
            ag_rat = float(row[y2]) - float(row[y1])
            if ag_rat > 0:
                agri[row[1]] = ag_rat
rat = list()
with open(forest_filename, 'r', encoding='utf-8') as f:
    csvdocf = csv.reader(f)
    for rowf in csvdocf:
        if len(rowf) > y2 and rowf[3] == "AG.LND.FRST.K2":
            if rowf[y2] != '' and rowf[y1] != '' and rowf[1] in agri:
                fs_rat = float(rowf[y2]) - float(rowf[y1])
                if fs_rat > 0:
                    ratio = agri[rowf[1]] / fs_rat
                    rat.append((ratio, rowf[0]))
n = min(top_n, len(rat))
p_sort(rat, n)
for i in range(n):
    countries.append(f"{rat[i][1]} ({rat[i][0]:.2f})")

#
# end

print(f'Here are the top {top_n} countries or categories where, between {year_1} and {year_2},\n'
      '  agricultural land and forest land areas have both strictly increased,\n'
      '  listed from the countries where the ratio of agricultural land area increase\n'
      '  to forest area increase is largest, to those where that ratio is smallest:')
print('\n'.join(country for country in countries))
