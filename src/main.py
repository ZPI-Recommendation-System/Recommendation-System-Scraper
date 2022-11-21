import datetime

from src import websockets


def main():
    import logging.config
    logging.basicConfig(encoding="utf-8", level=logging.INFO, filemode="w", filename="logs/" + str(datetime.datetime.now()).replace(":", "-") + ".log", format="[%(levelname)s][%(asctime)s] %(message)s")
    logging.getLogger().addHandler(logging.StreamHandler())
    websockets.start()


if __name__ == '__main__':
    main()