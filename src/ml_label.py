import os
import sys

from src import websockets

sys.path.append(os.path.join(os.getcwd(), "src/ml_module"))


import logging
import os
import sys


sys.path.append(os.path.join(os.getcwd(), "src/ml_module"))


def run(while_scraping=False):
    if not while_scraping:
        websockets.emit_job_status(job='ml_label', status='running', logs=['Rozpoczęto operację estymacji cen laptopów w bazie'])
    logging.info("Rozpoczęto operację uczenia modelu")
    try:
        from src.ml_module import evaluator
        evaluator.process()
        if not while_scraping:
            websockets.emit_job_status(job='ml_label', status='finished', logs=['Operacja zakończona pomyślnie'])
        logging.info("Operacja zakończona pomyślnie")
    except FileNotFoundError as err:
        if while_scraping:
            return
        logging.error("Brak wyuczonego modelu. Operacja zakończona błędem", exc_info=True, stack_info=True)
        if not while_scraping:
            websockets.emit_job_status(job='ml_learn', status='error', logs=['Brak wyuczonego modelu', 'Operacja zakończona błędem'])
    except:
        logging.error("Operacja zakończona błędem", exc_info=True, stack_info=True)
        if not while_scraping:
            websockets.emit_job_status(job='ml_label', status='error', logs=['Operacja zakończona błędem'])


    websockets.isRunning = False
    websockets.job = ""

if __name__ == "__main__":
    run(False)
