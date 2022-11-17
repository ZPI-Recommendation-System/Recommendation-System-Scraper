import logging
from threading import Thread
from time import sleep

import socketio

from src.pipeline import Pipeline

SCRAPPER_AUTH_REQUEST = 'scrapper.auth.request'
SCRAPPER_WORK_STATUS = 'scrapper.work.status'
SCRAPPER_WORK_PING = 'scrapper.work.ping'
SCRAPPER_WORK_CANCEL = 'scrapper.work.cancel'

AUTH_TOKEN = "ABCDEFGHIJK"
URL = "http://localhost:3000"

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
    # print("Here please execute auth link logic and return allegro auth link")
    logging.info("Otrzymano scrapping_request")
    auth_data = pipeline.api_auth()
    Thread(target=pipeline.run, args=[auth_data]).run()
    return auth_data['verification_uri_complete']


@sio.on(SCRAPPER_WORK_PING)
def scrapping_ping():
    # print("Here is the logic of responding to work ping. Respond with emmiting SCRAPPER_WORK_STATUS ping")
    logging.info("Otrzymano scrapping_ping")
    emit_work_status(pipeline.status, [], None)


@sio.on(SCRAPPER_WORK_CANCEL)
def scrapping_cancel():
    logging.info("Otrzymano scrapping_cancel")
    # print("Here is the logic of cancelling scrapping. Respond with emminit SCRAPPER_WORK_STATUS with cannceled")


@sio.event
def connect():
    logging.info("Połączono z adresem " + URL)
    # print("I'm connected!")
    # sleep(2)
    # emit_work_status("ready", ["123", "123123"], "its working")


@sio.event
def connect_error(data):
    logging.error("Błąd połączenia z adresem " + URL)
    # print("The connection failed!")


@sio.event
def disconnect():
    logging.info("Odłączono od adresu " + URL)
    # print("I'm disconnected!")


def emit_work_status(status: str, logs: list[str], payload, estimated_time=0, callback=None):
    sio.emit(SCRAPPER_WORK_STATUS,
             {'workStatus': status, 'logs': logs, 'payload': payload, "estimatedTime": estimated_time},
             callback=callback)


def start():
    sio.connect(url=URL, headers={"Authorization": AUTH_TOKEN}, transports="websocket", wait_timeout=4)
    logging.info("Nasłuchiwanie...")
    sio.wait()

