import os
import datetime


def getDate():
    return str(datetime.date.today().strftime("%d_%m_%Y"))


def CreateNewFile(Pos, FileName=None, level=1, data=0, FileDirPath=None):

    ToDay = getDate()

    if level == 0:
        FileDirPath = r"C:\Users\liran\OneDrive\Desktop\School\data scientist\Jhon Bryce\DataBase\Analyze"
    elif level == 1 and Pos not in ['Main', 'sub1', 'sub1'] and FileName is None:
        FileName = FileDirPath.split('\\')[len(FileDirPath.split('\\'))-1]

    try:
        if Pos == 'Main':
            if not os.path.exists(FileDirPath + ' ' + ToDay):
                os.mkdir(FileDirPath + ' ' + ToDay)
        elif Pos == 'sub1' or Pos == 'sub2':
            if not os.path.exists(FileDirPath + ' ' + ToDay):
                os.makedirs(FileDirPath + ' ' + ToDay)
        elif Pos == 'log':
            fullPath = os.path.join(FileDirPath, f'{FileName} {ToDay}.log')
            if not os.path.exists(fullPath):
                open(fullPath, 'w').close()
        elif Pos == 'json':
            fullPath = os.path.join(FileDirPath, f'{FileName} {ToDay}.json')
            if not os.path.exists(fullPath):
                open(fullPath, 'w').close()
        elif Pos == 'text':
            fullPath = os.path.join(FileDirPath, f'{FileName} {ToDay}.txt')
            if not os.path.exists(fullPath):
                open(fullPath, 'w').close()

    except FileExistsError:
        if Pos == 'log' or Pos == 'json' or Pos == 'text':
            print("%s file already exists" % FileName)
        else:
            print("%s directory already exists" % FileDirPath)
    except OSError as oerr:
        if Pos == 'log' or Pos == 'json' or Pos == 'text':
            print(f"Creation of the file {FileName} failed \n got this error: {oerr}")
        else:
            print(f"Creation of the directory {FileDirPath} failed \n got this error: {oerr}")

    except TypeError as terr:
        if Pos == 'log' or Pos == 'json' or Pos == 'text':
            print(f"Creation of the file {FileName} failed \n got this error: {terr}")
        else:
            print(f"Creation of the directory {FileDirPath} failed \n got this error: {terr}")
    else:
        if Pos == 'log' or Pos == 'json' or Pos == 'text':
            print("Successfully created the file %s" % FileName)
            return fullPath
        else:
            print("Successfully created the directory %s" % FileDirPath)
            return FileDirPath + ' ' + ToDay
