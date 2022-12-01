import random

import pandas as pd


# Mock
def run_for(laptops):
    laptops['price'] = pd.NaT
    laptops['priceSource'] = ""

    for index, row in laptops.iterrows():
        laptops.at[index, 'priceSource'] = "generated"
        laptops.at[index, 'price'] = round(random.uniform(1000.00, 11000.00), 2)

    return laptops
