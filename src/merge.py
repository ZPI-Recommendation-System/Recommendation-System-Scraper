import pandas as pd

OUTPUT_CLEAR_LAPTOPS_CSV = "clear-laptops.csv"
OUTPUT_CLEAR_OFFERS_CSV = "clear-laptops.csv"


def run_for(laptops, offers_file):
    offers = pd.read_csv(offers_file, quotechar='\'', on_bad_lines='skip', sep='\t', names=['Name', 'Price', 'URL', 'Category'], header=None)
    merged_data = pd.merge(laptops, offers, on='Name', how='inner')
    offers = merged_data[['Name', 'Price', 'URL', 'Category']]
    offers.to_csv(OUTPUT_CLEAR_OFFERS_CSV, index=False, header=True)
    merged_data = merged_data.drop_duplicates(subset=['Name'])
    laptops = merged_data.drop(columns=['Price', 'URL', 'Category'])
    laptops.to_csv(OUTPUT_CLEAR_LAPTOPS_CSV, index=False, header=True)
    return laptops, offers
