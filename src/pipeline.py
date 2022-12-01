import logging

import pandas as pd

from src import prefilter, merge_offers, postfilter, database, allegro_api, benchmarks, websockets, price_predictor
from src.constants import INPUT_OFFERS_CSV, OUTPUT_CSV
from timeit import default_timer as timer
from datetime import timedelta, datetime


class Pipeline:
    def __init__(self, isWebsocket):
        self.status = "ready"
        self.isWebsocket = isWebsocket
        # logging.info("[Scraper] Scraper jest gotowy do pracy")

    def api_auth(self):
        self.status = "running"
        logging.info("[Scraper] Scraper rozpoczął pracę")
        auth_data = allegro_api.auth()
        # TODO czy przesyłać logi z linkiem
        self.log(status="waiting_for_auth", message="Rozpoczęto operację aktualizacji bazy danych")
        self.log(status="waiting_for_auth", message="Link do autoryzacji:")
        self.log(status="waiting_for_auth", message=str(auth_data['verification_uri_complete']))
        return auth_data

    def run(self, auth_data):
        self.status = "running"
        tries = 0
        start = timer()
        while True:
            try:
                self.log("waiting_for_auth", "Oczekiwanie na autoryzację...")
                # access_token = allegro_api.auth2(auth_data)
                if self.isWebsocket:
                    websockets.emit_work_status("authorised", [], None)
                self.log(self.status, "Gotowe!")
                self.log(self.status, "Pobieranie laptopów...")
                # laptops = allegro_api.scrape(access_token)
                laptops = pd.read_csv(OUTPUT_CSV)
                self.log(self.status, "Gotowe!")
                self.log(self.status, "Wstępne filtrowanie danych...")
                prefiltered_laptops = prefilter.run_for(laptops)
                self.log(self.status, "Gotowe!")
                self.log(self.status, "Czyszczenie danych...")
                clear_laptops = postfilter.run_for(prefiltered_laptops)
                self.log(self.status, "Gotowe!")
                self.log(self.status, "Pobieranie danych benchmarków...")
                cpu_benchmarks, gpu_benchmarks = benchmarks.get()
                self.log(self.status, "Gotowe!")
                self.log(self.status, "Ustalanie cen modeli...")
                clear_laptops = price_predictor.run_for(clear_laptops)
                self.log(self.status, "Gotowe!")
                self.log(self.status, "Aktualizowanie bazy danych...")
                database.update(clear_laptops, cpu_benchmarks, gpu_benchmarks)
                self.log(self.status, "Gotowe!")
                end = timer()
                time = str(timedelta(seconds=end - start))
                logging.info("Operacja zakończona pomyślnie")
                logging.info("Czas trwania: " + time)
                if self.isWebsocket:
                    websockets.emit_work_status("finished", ["Operacja zakończona pomyślnie", "Czas trwania: " + time], None)
                break
            except Exception as err:
                self.log("error", "Wystąpił błąd: " + str(err))
                if tries < 3:
                    tries += 1
                    self.log("running", "Ponawianie (próba nr " + str(tries) + ")...")
                    continue
                else:
                    end = timer()
                    time = str(timedelta(seconds=end - start))
                    logging.error("Operacja zakończona błędem")
                    logging.info("Czas trwania: " + time)
                    if self.isWebsocket:
                        websockets.emit_work_status("error", ["Operacja zakończona błędem"], None)
                        websockets.emit_work_status("info", ["Czas trwania: " + time], None)
                        websockets.emit_work_status("finished", [], None)
                    break

        self.status = "ready"
        logging.info("[Scraper] Scraper jest gotowy do pracy")
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
