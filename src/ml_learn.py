import logging
import os
import sys

from src import websockets
from src.websockets import emit_job_status

sys.path.append(os.path.join(os.getcwd(), "src/ml_module"))

from src.ml_module import tree
def run():
    emit_job_status(job='ml_learn', status='running', logs=['Rozpoczęto operację uczenia modelu'])
    logging.info("Rozpoczęto operację uczenia modelu")
    try:
        # tree.process()
        emit_job_status(job='ml_learn', status='finished', logs=['Operacja zakończona pomyślnie'])
        logging.info("Operacja zakończona pomyślnie")
    except:
        logging.error("Operacja zakończona błędem", exc_info=True, stack_info=True)
        emit_job_status(job='ml_learn', status='error', logs=['Operacja zakończona błędem'])

    websockets.isRunning = False
    websockets.job = ""

if __name__ == "__main__":
    run()