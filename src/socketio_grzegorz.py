from time import sleep

import socketio

SCRAPPER_JOB_REQUEST = 'scrapper.auth.request'
SCRAPPER_WORK_STATUS = 'scrapper.work.status'
SCRAPPER_WORK_PING = 'scrapper.work.ping'
SCRAPPER_WORK_CANCEL = 'scrapper.work.cancel'

AUTH_TOKEN = "ABCDEFGHIJK"
URL = "http://localhost:3000"

sio = socketio.Client()


# export type WorkStatus =
# | 'waiting_for_job' -> Emit on job started, but waiting for any admin input
# | 'authorised' -> Emit on authorisation successful
# | 'running' -> Emit while working
# | 'finished' -> Emit while finished
# | 'error' -> Emit on error
# | 'cancelled' -> emit on cancel
# | 'ready'; -> Emit on no job pending
#
# export interface ScrapperWorkStatusDto {
#   jobName: string; <- nazwa zadania
#   workStatus: WorkStatus; <- status zadania
#   estimatedTime: number; <- ile czasu do końca zadania
#   payload: any; <- dodatkowe rzeczy, ostatni payload jest wysyłany do frontendu
#   logs: string[]; <- logi, wszystkie logi są przechowywane do następnego "waiting_for_job"
# }

@sio.on(SCRAPPER_JOB_REQUEST)
def scrapping_job_request(payload):  # payload -> backend/frontend może wysyłać tym jakieś dodatkowe argumenty
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
