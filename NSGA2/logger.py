from logging import getLogger, Formatter, DEBUG, StreamHandler

def logger(name):
    logger = getLogger(name)
    logger.setLevel(DEBUG)

    handler = StreamHandler()
    formatter = Formatter('%(asctime)s  [%(name)s] %(levelname)s: %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger