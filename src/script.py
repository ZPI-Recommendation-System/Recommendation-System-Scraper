from src import prefilter, merge, postfilter, database, allegro_api

INPUT_OFFERS_CSV = "offers.csv"

if __name__ == "__main__":
    laptops = allegro_api.scrape()
    prefiltered_laptops = prefilter.run_for(laptops)
    clear_laptops, clear_offers = merge.run_for(prefiltered_laptops, INPUT_OFFERS_CSV)
    clear_laptops, clear_offers = postfilter.run_for(clear_laptops, clear_offers)
    database.update(clear_laptops, clear_offers)

