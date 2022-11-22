import logging
from threading import Thread

import socketio

from src.pipeline import Pipeline

SCRAPPER_AUTH_REQUEST = 'scrapper.auth.request'
SCRAPPER_WORK_STATUS = 'scrapper.work.status'
SCRAPPER_WORK_PING = 'scrapper.work.ping'
SCRAPPER_WORK_CANCEL = 'scrapper.work.cancel'

AUTH_TOKEN = "ABCDEFGHIJK"
URL = "http://zpi.zgrate.ovh:5036"
# URL = "http://localhost:3000"

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

@sio.on(SCRAPPER_AUTH_REQUEST)
def scrapping_request(data):
    if pipeline.status == "running":
        return {"status": "running", "auth_link": ""}
    logging.info("[Websocket] Otrzymano scrapping_request")
    auth_data = pipeline.api_auth()
    Thread(target=pipeline.run, args=[auth_data]).start()
    return {"status": "ok", "auth_link": auth_data['verification_uri_complete']}


@sio.on(SCRAPPER_WORK_PING)
def scrapping_ping():
    logging.info("[Websocket] Otrzymano scrapping_ping")
    emit_work_status(pipeline.status, [], None)


@sio.on(SCRAPPER_WORK_CANCEL)
def scrapping_cancel():
    logging.info("[Websocket] Otrzymano scrapping_cancel")


@sio.event
def connect():
    logging.info("[Websocket] Połączono z adresem " + URL)


@sio.event
def connect_error(data):
    logging.error("[Websocket] Błąd połączenia z adresem " + URL)


@sio.event
def disconnect():
    logging.info("[Websocket] Odłączono od adresu " + URL)


def emit_work_status(status: str, logs: list[str], payload, estimated_time=0, callback=None):
    sio.emit(SCRAPPER_WORK_STATUS,
             {'workStatus': status, 'logs': logs, 'payload': payload, "estimatedTime": estimated_time},
             callback=callback)


def start():
    sio.connect(url=URL, headers={"Authorization": AUTH_TOKEN}, transports="websocket", wait_timeout=4)
    logging.info("[Websocket] Nasłuchiwanie...")
    sio.wait()

