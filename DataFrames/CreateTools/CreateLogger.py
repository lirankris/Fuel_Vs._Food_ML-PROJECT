import logging
import datetime
import os
from pathlib import Path


def getDate():
    return str(datetime.date.today().strftime("%d_%m_%Y"))


def Log(LogName):
    cwd = os.getcwd()
    filePath = rf'{Path(cwd)}\Log'

    LogPath = CreateNewLogFile(date=getDate(),
                               filename=LogName, file_path=filePath)

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


def CreateNewLogFile(date, filename, file_path):
    ToDay = date
    fullPath = os.path.join(file_path, f'{filename} {ToDay}.log')
    try:
        if not os.path.exists(fullPath):
            open(fullPath, 'w+').close()
        else:
            raise FileExistsError

    except FileExistsError:
        print(f"{filename} {ToDay}.log already exists")
    except OSError as oerr:
        print(f"Creation of the {filename} {ToDay}.log failed \n got this error: {oerr}")
    except TypeError as terr:
        print(f"Creation of the file {filename} {ToDay}.log failed \n got this error: {terr}")
    else:
        print(f"Successfully created the {filename} {ToDay}.log ")

    return fullPath
