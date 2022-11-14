from time import sleep

import socketio

SCRAPPER_AUTH_REQUEST = 'scrapper.auth.request'
SCRAPPER_WORK_STATUS = 'scrapper.work.status'
SCRAPPER_WORK_PING = 'scrapper.work.ping'
SCRAPPER_WORK_CANCEL = 'scrapper.work.cancel'

AUTH_TOKEN = "ABCDEFGHIJK"
URL = "http://localhost:3000"

sio = socketio.Client()


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
    print("Here please execute auth link logic and return allegro auth link")
    return "allegro_link"


@sio.on(SCRAPPER_WORK_PING)
def scrapping_ping():
    print("Here is the logic of responding to work ping. Respond with emmiting SCRAPPER_WORK_STATUS ping")


@sio.on(SCRAPPER_WORK_CANCEL)
def scrapping_cancel():
    print("Here is the logic of cancelling scrapping. Respond with emminit SCRAPPER_WORK_STATUS with cannceled")


@sio.event
def connect():
    print("I'm connected!")
    sleep(2)
    emit_work_status("ready", ["123", "123123"], "its working")


@sio.event
def connect_error(data):
    print("The connection failed!")


@sio.event
def disconnect():
    print("I'm disconnected!")


def emit_work_status(status: str, logs: list[str], payload, estimated_time=0, callback=None):
    sio.emit(SCRAPPER_WORK_STATUS,
             {'workStatus': status, 'logs': logs, 'payload': payload, "estimatedTime": estimated_time},
             callback=callback)


sio.connect(url=URL, headers={"Authorization": AUTH_TOKEN}, transports="websocket", wait_timeout=4)
sio.wait()
