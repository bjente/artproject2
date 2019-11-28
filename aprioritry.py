import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from apyori import apriori

## In this program I use the apriori algorithm to find 'rules' in the art data.
## You can alter the parameters in the apriori function. It will get stuck pretty soon because of the large amount of data.
## I am still struggling with what kind of algorithm I should use to make NOVEL combinations. 
with open('data/momaoutput.txt') as f:
    artworklist = eval(f.read())

print(artworklist)
association_rules = apriori(artworklist, min_support=0.05, min_confidence=0.5, min_lift=3, max_length=15)
association_results = list(association_rules)
print(len(association_results))
print(association_results)


## This prints the rules in a more readable way, but it only prints TWO items, even if there are more items in one rule.
## I still have to change this with a for loop.
for item in association_results:

    # first index of the inner list
    # Contains base item and add item
    pair = item[0]
    items = [x for x in pair]
    print(items)
    for i in range(len(items)):
    print("Rule: " + items[0] + " -> " + items[1])

    #second index of the inner list
    print("Support: " + str(item[1]))

    #third index of the list located at 0th
    #of the third index of the inner list

    print("Confidence: " + str(item[2][0][2]))
    print("Lift: " + str(item[2][0][3]))
    print("=====================================")
