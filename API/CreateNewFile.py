import os
import datetime


def CreateNewFile(FileDirPath, Pos, FileName=None):

    ToDay = str(datetime.date.today().strftime("%d_%m_%Y"))

    try:
        if Pos == 'Main':
            if not os.path.exists(FileDirPath + ' ' + ToDay):
                os.mkdir(FileDirPath + ' ' + ToDay)
        elif Pos == 'sub1' or Pos == 'sub2':
            if not os.path.exists(FileDirPath + ' ' + ToDay):
                os.makedirs(FileDirPath + ' ' + ToDay)
        elif Pos == 'log':
            FileName = FileDirPath.split('\\')[len(FileDirPath.split('\\'))-1]
            if not os.path.exists(FileDirPath + ' ' + ToDay + '.log'):
                open(FileDirPath + ' ' + ToDay + '.log', 'w').close()
        elif Pos == 'json':
            FileName = FileDirPath.split('\\')[len(FileDirPath.split('\\'))-1]
            if not os.path.exists(FileDirPath + ' ' + ToDay + '.json'):
                open(FileDirPath + ' ' + ToDay + '.json', 'w').close()

    except FileExistsError:
        if Pos == 'log' or Pos == 'json':
            print("%s file already exists" % FileName)
        else:
            print("%s directory already exists" % FileDirPath)

    except OSError:
        if Pos == 'log' or Pos == 'json':
            print("Creation of the file %s failed" % FileName)
        else:
            print("Creation of the directory %s failed" % FileDirPath)

    else:
        if Pos == 'log' or Pos == 'json':
            print("Successfully created the file %s" % FileName)
        else:
            print("Successfully created the directory %s" % FileDirPath)

    if Pos == 'json':
        return FileDirPath + ' ' + ToDay + '.json'

    elif Pos == 'log':
        return FileDirPath + ' ' + ToDay + '.log'

    else:
        return FileDirPath + ' ' + ToDay
