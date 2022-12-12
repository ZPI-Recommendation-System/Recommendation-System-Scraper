import logging
from threading import Thread

import socketio

from src import ml_learn, ml_label, clear_db
from src.constants import BACKEND_URL, AUTH_TOKEN
from src.pipeline import Pipeline

JOB_SCRAPE = "scrapper.job.scrape"
JOB_ML_LEARN = "scrapper.job.ml.learn"
JOB_ML_LABEL = "scrapper.job.ml.label"
JOB_CLEAR_DB = "scrapper.job.clear.db"
JOB_STATUS = "scrapper.job.status"

SCRAPER_AUTH_REQUEST = 'scrapper.auth.request'
SCRAPER_WORK_STATUS = 'scrapper.work.status'
SCRAPER_STATUS_PING = 'scrapper.work.ping'
SCRAPER_WORK_CANCEL = 'scrapper.work.cancel'

sio = socketio.Client()

pipeline = Pipeline(True)


# export type WorkStatus =
# | 'authorised'
# | 'running'
# | 'finished'
# | 'error'
# | 'cancelled'
# | 'ready';
#
# export interface ScrapperWorkStatusDto {
#   workStatus: WorkStatus;
#   estimatedTime: number;
#   payload: any;
#   logs: string[];
# }

auth_link = ""
isRunning = False
job = ""

@sio.on(SCRAPER_AUTH_REQUEST)
@sio.on(JOB_SCRAPE)
def scrape_request():
    global isRunning, job, auth_link
    isRunning = True
    job = "scrape"
    if pipeline.status == "running":
        return {"status": "running", "auth_link": auth_link}
    logging.info("[Websocket] Otrzymano scrapping_request")
    auth_data = pipeline.api_auth()
    Thread(target=pipeline.run, args=[auth_data]).start()
    auth_link = auth_data['verification_uri_complete']
    return {"status": "ok", "auth_link": auth_link}


@sio.on(JOB_ML_LEARN)
def ml_learn_request():
    global isRunning, job
    isRunning = True
    job = "ml_learn"
    ml_learn.run()

@sio.on(JOB_ML_LABEL)
def ml_learn_request():
    global isRunning, job
    isRunning = True
    job = "ml_label"
    ml_label.run()

@sio.on(JOB_CLEAR_DB)
def ml_learn_request():
    global isRunning, job
    isRunning = True
    job = "clear_db"
    clear_db.run()

def emit_scraper_status():
    sio.emit(SCRAPER_WORK_STATUS, {'isRunning': isRunning, 'job': job}, callback = None)


@sio.on(SCRAPER_STATUS_PING)
def scraper_status():
    logging.info("[Websocket] Otrzymano SCRAPER_STATUS_PING")
    emit_scraper_status()


@sio.on(SCRAPER_WORK_CANCEL)
def scrapping_cancel():
    logging.info("[Websocket] Otrzymano scrapping_cancel")


@sio.event
def connect():
    logging.info("[Websocket] Połączono z adresem " + BACKEND_URL)


@sio.event
def connect_error(data):
    logging.error("[Websocket] Brak połączenia z adresem " + BACKEND_URL)


@sio.event
def disconnect():
    logging.info("[Websocket] Odłączono od adresu " + BACKEND_URL)

def emit_job_status(job: str, status: str, logs: list[str], payload=None, estimated_time=0, callback=None):
    sio.emit(JOB_STATUS, {'job': job, 'status': status, 'logs': logs, 'payload': payload, "estimatedTime": estimated_time}, callback=callback)


def start():
    while True:
        try:
            sio.connect(url=BACKEND_URL, headers={"Authorization": AUTH_TOKEN}, transports="websocket", wait=True, wait_timeout=120)
            break
        except:
            sio.sleep(20)
            continue
    logging.info("[Websocket] Nasłuchiwanie...")
    sio.wait()

