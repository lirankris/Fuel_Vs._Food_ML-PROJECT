import logging


def Log(LogName, LogPath, ToDay):

    logger = logging.getLogger(LogName)
    logger.setLevel(logging.DEBUG)  # the level should be the lowest level set in handlers
    log_format = logging.Formatter('%(asctime)s: \t --> [%(levelname)s] \t %(message)s')

    streamLog = logging.StreamHandler()
    streamLog.setFormatter(log_format)
    streamLog.setLevel(logging.DEBUG)
    logger.addHandler(streamLog)

    MainLog = logging.FileHandler(LogPath)
    MainLog.setFormatter(log_format)
    MainLog.setLevel(logging.DEBUG)
    logger.addHandler(MainLog)

    return logger
