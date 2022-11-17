import logging

import pandas as pd

from src import prefilter, merge_offers, postfilter, database, allegro_api, benchmarks, websockets
from src.constants import INPUT_OFFERS_CSV, OUTPUT_CSV
from timeit import default_timer as timer
from datetime import timedelta, datetime


class Pipeline:
    def __init__(self, isWebsocket):
        self.status = "ready"
        self.isWebsocket = isWebsocket

    def api_auth(self):
        self.status = "running"
        auth_data = allegro_api.auth()
        self.log(status=self.status, message=str(auth_data['verification_uri_complete']))
        return auth_data

    def run(self, auth_data):
        self.status = "running"
        try:
            start = timer()
            self.log(self.status, "Pobieranie laptopów...")
            laptops = allegro_api.scrape(auth_data)
            self.log(self.status, "Gotowe!")
            # laptops = pd.read_csv(OUTPUT_CSV)
            # print("Done!\nPrefilter")
            self.log(self.status, "Wstępne filtrowanie danych...")
            prefiltered_laptops = prefilter.run_for(laptops)
            self.log(self.status, "Gotowe!")
            self.log(self.status, "Łączenie modeli z ofertami...")
            # print("Done!\nMerge with offers")
            clear_laptops, clear_offers = merge_offers.run_for(prefiltered_laptops, INPUT_OFFERS_CSV)
            self.log(self.status, "Gotowe!")
            self.log(self.status, "Czyszczenie danych...")
            # print("Done!\nPosttfilter")
            clear_laptops, clear_offers = postfilter.run_for(clear_laptops, clear_offers)
            self.log(self.status, "Gotowe!")
            # print("Done!\nPobieranie benchmarków")
            self.log(self.status, "Pobieranie danych benchmarków...")
            cpu_benchmarks, gpu_benchmarks = benchmarks.get()
            self.log(self.status, "Gotowe!")
            # print("Done!\nAktualizacja bazy danych")
            self.log(self.status, "Aktualizowanie bazy danych...")
            database.update(clear_laptops, clear_offers, cpu_benchmarks, gpu_benchmarks)
            self.log(self.status, "Gotowe!")
            end = timer()
            # print("Czas wykonywania: " + str(timedelta(seconds=end - start)))
            time = str(timedelta(seconds=end - start))
            self.status = "ready"
            logging.info("Operacja aktualizacji bazy danych zakończona")
            logging.info("Czas trwania: " + time)
            if self.isWebsocket:
                websockets.emit_work_status("finished", ["Operacja aktualizacji bazy danych zakończona", "Czas trwania: " + time], None)
        except Exception as err:
            self.log("error", "Wystąpił błąd: " + str(err))
        finally:
            if self.isWebsocket:
                websockets.emit_work_status("ready", [], None)

    def log(self, status, message):
        if status == "error":
            logging.error(message)
        else:
            logging.info(message)

        if self.isWebsocket:
            websockets.emit_work_status(status, [message], None)






if __name__ == "__main__":
    import logging.config

    # stream_handler = logging.StreamHandler()
    # stream_handler.setLevel(logging.INFO)
    # logging.basicConfig(handlers=[stream_handler, logging.FileHandler(filename="logs/" + str(datetime.now()).replace(":", "-") + ".log", mode="w")], format="[%(levelname)s][%(asctime)s] %(message)s"),
    logging.basicConfig(level=logging.INFO, filename="logs/" + str(datetime.now()).replace(":", "-") + ".log", filemode="w", format="[%(levelname)s][%(asctime)s] %(message)s")
    logging.getLogger().addHandler(logging.StreamHandler())
    pipeline = Pipeline(False)
    pipeline.run(pipeline.api_auth())



# if __name__ == "__main__":
#     start = timer()
#     print("Pobieranie laptopów")
#     auth_data = allegro_api.auth()
#     laptops = allegro_api.scrape(auth_data)
#     # laptops = pd.read_csv(OUTPUT_CSV)
#     print("Done!\nPrefilter")
#     prefiltered_laptops = prefilter.run_for(laptops)
#     print("Done!\nMerge with offers")
#     clear_laptops, clear_offers = merge_offers.run_for(prefiltered_laptops, INPUT_OFFERS_CSV)
#     print("Done!\nPosttfilter")
#     clear_laptops, clear_offers = postfilter.run_for(clear_laptops, clear_offers)
#     print("Done!\nPobieranie benchmarków")
#     cpu_benchmarks, gpu_benchmarks = benchmarks.get()
#     print("Done!\nAktualizacja bazy danych")
#     database.update(clear_laptops, clear_offers, cpu_benchmarks, gpu_benchmarks)
#     print("Done!")
#     end = timer()
#     print("Czas wykonywania: " + str(timedelta(seconds=end - start)))

    # laptops = allegro_api.scrape()
    # prefiltered_laptops = prefilter.run_for(laptops)
    # clear_laptops = postfilter.run_for(prefiltered_laptops)
    # clear_laptops = price_evaluator.run_for(clear_laptops)
    # database.update(clear_laptops)
