import os
import sys

sys.path.append(os.path.join(os.getcwd(), "src/ml_module"))


def run(while_scraping=False):
    try:
        from src.ml_module import evaluator
        evaluator.process()
    except FileNotFoundError as err:
        if while_scraping:
            return
        raise err

if __name__ == "__main__":
    run(False)
