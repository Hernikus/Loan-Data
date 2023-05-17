#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 15:34:01 2023

@author: hernikusuma
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# method 1 to read json file 
json_file = open('loan_data_json.json')
data = json.load(json_file)

# method 2 to read json file
with open('loan_data_json.json') as json_file:
    data = json.load(json_file)
    
# transform to data frame
loanData = pd.DataFrame(data)

# finding unique value for the purpose column
loanData['purpose'].unique()

# describe the data
loanData.describe()

# describe the data for spesific column
loanData['int.rate'].describe()
loanData['fico'].describe()
loanData['dti'].describe()

# using EXP to get annual income 
income = np.exp(loanData['log.annual.inc'])
loanData['annualIncome'] = income

# fico range 
# fico >= 300 and < 400: 'Very Poor' 
# fico >= 400 and ficoscore < 600: 'Poor' 
# fico >= 601 and ficoscore < 660: 'Fair' 
# fico >= 660 and ficoscore < 780: 'Good' fico >=780: 'Excellent'

# create fico category column

ficocat = []
length = len(loanData)

for x in range(0, length):
    category = loanData['fico'][x]
    try:
        if category >= 300 and category < 400:
            cat = 'Very Poor' 
        elif category >= 400 and category < 600:
            cat = 'Poor' 
        elif category >= 601 and category < 660:
            cat = 'Fair'
        elif category >= 660 and category < 780:
            cat = 'Good'
        elif category >=780:
            cat = 'Excellent'
        else:
            cat = "unknown"
    except:
        cat = 'unknown'
    ficocat.append(cat)

ficocat = pd.Series(ficocat)
    
loanData['fico.category'] = ficocat

# df.loc as conditional statement
#  df.loc[df[columnname] condition, newcolumn] = 'value if condition is met'

# clasify the interest rate
loanData.loc[loanData['int.rate']> 0.12, 'int.rate.type'] = 'High'

loanData.loc[loanData['int.rate']<= 0.12, 'int.rate.type'] = 'Low'

# numbers of loans by category

catplot = loanData.groupby(['fico.category']).size()
catplot.plot.bar()
plt.show()

catpurpose = loanData.groupby(['purpose']).size()
catpurpose.plot.bar()
plt.show()

# scatter plots
xpoint = loanData['dti']
ypoint = loanData['annualIncome']
plt.scatter(xpoint, ypoint)
plt.show()

# convert to csv
loanData.to_csv('loan_clean.csv', index=True)



















