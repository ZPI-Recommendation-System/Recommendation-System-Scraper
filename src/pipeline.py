import logging
from datetime import timedelta, datetime
from timeit import default_timer as timer

import pandas as pd

from src import allegro_api, websockets, prefilter, postfilter, benchmarks, database, ml_label, set_prices


class Pipeline:
    def __init__(self, isWebsocket):
        self.status = "ready"
        self.isWebsocket = isWebsocket

    def api_auth(self):
        self.status = "running"
        logging.info("[Scraper] Scraper rozpoczął pracę")
        auth_data = allegro_api.auth()
        self.log(status="waiting_for_auth", message="Rozpoczęto operację aktualizacji bazy danych")
        self.log(status="waiting_for_auth", message="Link do autoryzacji:")
        self.log(status="waiting_for_auth", message=str(auth_data['verification_uri_complete']))
        return auth_data

    def run(self, auth_data):
        self.status = "running"
        tries = 0
        start = timer()

        access_token = None

        while access_token is None:
            try:
                self.log("auth", "Oczekiwanie na autoryzację...")
                websockets.emit_job_status("scraper", "auth", ["Oczekiwanie na autoryzację..."], payload={"link": auth_data['verification_uri_complete']})
                access_token = allegro_api.auth2(auth_data)
                if self.isWebsocket:
                    websockets.auth_link = ""
                    websockets.emit_job_status("scraper",  "authorised", [], None)
                self.log(self.status, "Gotowe!")
            except Exception as err:
                end = timer()
                time = str(timedelta(seconds=end - start))
                logging.error("Operacja autoryzacji zakończona błędem")
                logging.info("Czas trwania: " + time)
                if self.isWebsocket:
                    websockets.emit_job_status("scraper",  "running", ["Operacja autoryzacji zakończona błędem"], None)
                    websockets.emit_job_status("scraper",  "running", ["Czas trwania: " + time], None)
                    websockets.emit_job_status("scraper",  "error", [], None)
                break

        while access_token is not None:
            try:
                self.log(self.status, "Pobieranie laptopów...")
                laptops = allegro_api.scrape(access_token)
                # laptops = pd.read_csv("resources/laptops_2.csv")
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
                self.log(self.status, "Aktualizowanie bazy danych...")
                database.update(clear_laptops, cpu_benchmarks, gpu_benchmarks)
                set_prices.run()
                ml_label.run(True)
                self.log(self.status, "Gotowe!")
                end = timer()
                time = str(timedelta(seconds=end - start))
                logging.info("Operacja zakończona pomyślnie")
                logging.info("Czas trwania: " + time)
                if self.isWebsocket:
                    websockets.emit_job_status("scraper",  "finished", ["Operacja zakończona pomyślnie", "Czas trwania: " + time], None)
                break
            except Exception as err:
                self.log("running", "Wystąpił błąd: " + str(err))
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
                        websockets.emit_job_status("scraper",  "running", ["Operacja zakończona błędem"], None)
                        websockets.emit_job_status("scraper",  "running", ["Czas trwania: " + time], None)
                        websockets.emit_job_status("scraper",  "error", [], None)
                    break

        websockets.isRunning = False
        websockets.job = ""
        self.status = "ready"
        logging.info("[Scraper] Scraper jest gotowy do pracy")
        # if self.isWebsocket:
        #     websockets.emit_job_status("scraper",  "ready", [], None)

    def log(self, status, message):
        if status == "error":
            logging.error(message, exc_info=True, stack_info=True)
        else:
            logging.info(message)

        if self.isWebsocket:
            websockets.emit_job_status("scraper",  status, [message], None)


if __name__ == "__main__":
    import logging.config
    logging.basicConfig(level=logging.INFO, filename="logs/" + str(datetime.now()).replace(":", "-") + ".log", filemode="w", format="[%(levelname)s][%(asctime)s] %(message)s")
    logging.getLogger().addHandler(logging.StreamHandler())
    pipeline = Pipeline(False)
    pipeline.run(pipeline.api_auth())
