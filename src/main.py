import datetime
import os

from src import websockets


def main():
    import logging.config
    if not os.path.exists("logs"):
        os.mkdir("logs")
    if not os.path.exists("resources"):
        os.mkdir("resources")
    logging.basicConfig(encoding="utf-8", level=logging.INFO, filemode="w", filename="logs/" + str(datetime.datetime.now()).replace(":", "-") + ".log", format="[%(levelname)s][%(asctime)s] %(message)s")
    if os.environ['CLIENT_ID'] == "" or os.environ['CLIENT_SECRET'] == "":
        error = "Scraper can not start. CLIENT_ID or CLIENT_SECRET environment variable is not set. Check your app.cfg file."
        logging.error(error)
        print(error)
        return
    logging.getLogger().addHandler(logging.StreamHandler())
    websockets.start()


if __name__ == '__main__':
    main()