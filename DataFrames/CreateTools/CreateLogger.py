import logging
import datetime
import os

#
# def getDate():
#     return str(datetime.date.today().strftime("%d_%m_%Y"))


def Log(LogName, LogPath=None):

    logger = logging.getLogger(LogName)
    logger.setLevel(logging.DEBUG)  # the level should be the lowest level set in handlers
    log_format = logging.Formatter('%(asctime)s: \t --> [%(levelname)s] \t %(message)s')

    streamLog = logging.StreamHandler()
    streamLog.setFormatter(log_format)
    streamLog.setLevel(logging.DEBUG)
    logger.addHandler(streamLog)

    # MainLog = logging.FileHandler(LogPath)
    # MainLog.setFormatter(log_format)
    # MainLog.setLevel(logging.DEBUG)
    # logger.addHandler(MainLog)

    # CreateNewFile(date=current_date, path=LogPath, filename=LogName)

    return logger


# def CreateNewFile(date, path, filename=None):
#
#     ToDay = date
#     FileDirPath = path
#     fullPath = os.path.join(FileDirPath, f'{filename} {ToDay}.log')
#     place = ''
#
#     try:
#         if not os.path.exists(FileDirPath + ' ' + filename):
#             os.mkdir(FileDirPath + ' ' + filename)
#         else:
#             place = 'Main'
#             raise FileExistsError
#
#         if not os.path.exists(fullPath):
#             open(fullPath, 'w').close()
#         else:
#             raise FileExistsError
#
#     except FileExistsError:
#         if place == 'Main':
#             print("%s directory already exists" % FileDirPath)
#         else:
#             print(f"{filename} {ToDay}.log already exists")
#
#     except OSError as oerr:
#         if place == 'Main':
#             print(f"Creation of the directory {FileDirPath} failed \n got this error: {oerr}")
#         else:
#             print(f"Creation of the {filename} {ToDay}.log failed \n got this error: {oerr}")
#
#     except TypeError as terr:
#         if place == 'Main':
#             print(f"Creation of the directory {FileDirPath} failed \n got this error: {terr}")
#         else:
#             print(f"Creation of the file {filename} {ToDay}.log failed \n got this error: {terr}")
#
#     else:
#         if place == 'Main':
#             print("Successfully created the directory %s" % FileDirPath)
#         else:
#             print(f"Successfully created the {filename} {ToDay}.log ")

