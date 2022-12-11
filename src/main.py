import datetime
import os

from src import websockets


def main():
    import logging.config
    logging.basicConfig(encoding="utf-8", level=logging.INFO, filemode="w", filename="logs/" + str(datetime.datetime.now()).replace(":", "-") + ".log", format="[%(levelname)s][%(asctime)s] %(message)s")
    logging.getLogger().addHandler(logging.StreamHandler())
    if os.environ['CLIENT_ID'] == "" or os.environ['CLIENT_SECRET'] == "":
        logging.error("Scraper can not start. CLIENT_ID or CLIENT_SECRET environment variable is not set. Check your app.cfg file.")
        return
    logging.getLogger().addHandler(logging.StreamHandler())
    websockets.start()


if __name__ == '__main__':
    main()