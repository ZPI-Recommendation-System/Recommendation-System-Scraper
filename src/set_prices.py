import os
from statistics import median

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.entities import ModelEntity
from src.constants import DATABASE_URL, INPUT_OFFERS_CSV


def run(offers_file=os.environ['PRICE_FILE']):
    engine = create_engine(DATABASE_URL)
    engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    entities = session.query(ModelEntity).all()
    names = list(map(lambda x: x.name, entities))
    dict = {"Name": names, "Entity": entities}
    laptops = pd.DataFrame(dict)

    offers = pd.read_csv(offers_file, quotechar='\'', on_bad_lines='skip', sep='\t',
                         names=['Name', 'Price', 'URL', 'Category'], header=None)

    offers['Price'] = offers['Price'] \
        .apply(str) \
        .apply(lambda x: x.replace(',', '.')) \
        .apply(map_to_float)

    rows_to_drop = offers[(offers['Price'] > 11000) | (offers['Price'] < 1000)]
    offers = offers.drop(rows_to_drop.index)
    laptops, _ = merge(laptops, offers)

    for index, row in laptops.iterrows():
        model_offers = offers.loc[offers['Name'] == row['Name']]
        model_price = round(median(model_offers['Price'].tolist()), 2)
        model_price_source = "allegro"
        entity = row['Entity']
        entity.price = model_price
        entity.priceSource = model_price_source

    session.commit()


def merge(laptops, offers):
    merged_data = pd.merge(laptops, offers, on='Name', how='inner')
    offers = merged_data[['Name', 'Price', 'URL', 'Category']]
    merged_data = merged_data.drop_duplicates(subset=['Name'])
    laptops = merged_data.drop(columns=['Price', 'URL', 'Category'])
    return laptops, offers


def map_to_float(x):
    try:
        result = (eval(x.split(' zł')[0].replace(' ', '')))
    except:
        result = 0

    return result


if __name__ == "__main__":
    run(INPUT_OFFERS_CSV)
