import pandas as pd

from src import prefilter, merge_offers, postfilter, database, allegro_api, benchmarks
from src.constants import INPUT_OFFERS_CSV, OUTPUT_CSV

if __name__ == "__main__":
    # laptops = allegro_api.scrape()
    laptops = pd.read_csv(OUTPUT_CSV)
    prefiltered_laptops = prefilter.run_for(laptops)
    clear_laptops, clear_offers = merge_offers.run_for(prefiltered_laptops, INPUT_OFFERS_CSV)
    clear_laptops, clear_offers = postfilter.run_for(clear_laptops, clear_offers)
    cpu_benchmarks, gpu_benchmarks = benchmarks.get()
    database.update(clear_laptops, clear_offers, cpu_benchmarks, gpu_benchmarks)

    # laptops = allegro_api.scrape()
    # prefiltered_laptops = prefilter.run_for(laptops)
    # clear_laptops = postfilter.run_for(prefiltered_laptops)
    # clear_laptops = price_evaluator.run_for(clear_laptops)
    # database.update(clear_laptops)
