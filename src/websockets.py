import logging
from threading import Thread

import socketio

from src.constants import BACKEND_URL, AUTH_TOKEN
from src.pipeline import Pipeline

JOB_SCRAPE = "scrapper.job.scrape"
JOB_ML_LEARN = "scrapper.job.ml_learn"
JOB_ML_LABEL = "scrapper.job.ml_label"
JOB_CLEAR_DB = "scrapper.job.clear_db"
JOB_STATUS = "scrapper.job.status"

SCRAPER_AUTH_REQUEST = 'scrapper.auth.request'
SCRAPER_WORK_STATUS = 'scrapper.work.status'
SCRAPER_STATUS_PING = 'scrapper.status.ping'
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
def scrape_request(data):
    logging.info("[Websocket] Otrzymano SCRAPER_AUTH_REQUEST")
    global isRunning, job, auth_link
    if isRunning:
        return {"status": "running", "jobName": job}
    isRunning = True
    job = data['jobName']
    if job == "scraper":
        if pipeline.status == "running":
            return {"status": "running", "auth_link": auth_link}
        auth_data = pipeline.api_auth()
        Thread(target=pipeline.run, args=[auth_data]).start()
        auth_link = auth_data['verification_uri_complete']
        emit_job_status(job, "auth", [], payload={"link": auth_link})
        return {"status": "ok", "auth_link": auth_link}
    elif job == "ml_learn":
        logging.info("[Websocket] Startowanie ML_LEARN")
        from src import ml_learn
        Thread(target=ml_learn.run(), args=[data['payload']]).start()
        return {"status": "ok"}
    elif job == "ml_label":
        logging.info("[Websocket] Startowanie ML_LABEL")
        from src import ml_label
        Thread(target=ml_label.run(), args=[data['payload']]).start()
        return {"status": "ok"}
    elif job == "clear_db":
        logging.info("[Websocket] Startowanie CLEAR_DB")
        from src import clear_db
        Thread(target=clear_db.run(), args=[data['payload']]).start()


@sio.on(SCRAPER_STATUS_PING)
def status_ping_request(data):
    logging.info("[Websocket] Otrzymano SCRAPER_STATUS_PING")
    emit_job_status(job, "running" if isRunning  else "ready", [])


@sio.on(SCRAPER_WORK_CANCEL)
def scrapping_cancel():
    logging.info("[Websocket] Otrzymano SCRAPER_WORK_CANCEL")


@sio.event
def connect():
    logging.info("[Websocket] Połączono z adresem " + BACKEND_URL)


@sio.event
def connect_error(data):
    logging.error("[Websocket] Oczekiwanie na połączenie z adresem " + BACKEND_URL)


@sio.event
def disconnect():
    logging.info("[Websocket] Odłączono od adresu " + BACKEND_URL)

def emit_job_status(job: str, status: str, logs: list[str], payload=None, estimated_time=0, callback=None):
    sio.emit(JOB_STATUS, {'jobName': job, 'workStatus': status, 'logs': logs, 'payload': payload, "estimatedTime": estimated_time}, callback=callback)


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

