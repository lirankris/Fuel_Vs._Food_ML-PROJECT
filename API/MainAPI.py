import OecdAPI
import YahooFinanceAPI
from CreateNewFile import CreateNewFile
from CreateLogger import Log
import itertools
from selenium import webdriver
import datetime
import time
import os


def main_api():
    # directorys :
    # [0]MainDir.
    # [1]yahoo_finance_File_path.
    # [2]OECD_File_path.
    # [3]OECD_json_get_all_File_path.
    # [4]OECD_Schema_File_path.

    # files :
    # [0]LogFILE.
    # [1]LogFILE_YF.
    # [2]LogFILE_Oecd.
    # get the date to add to the file name.

    ToDay = str(datetime.date.today().strftime("%d_%m_%Y"))

    # Main:
    DataBasePath = r"C:\Users\liran\OneDrive\Desktop\School\data scientist\Jhon Bryce\DataBase"
    FileDirName = "\Data_Set"
    MainDir = DataBasePath + FileDirName

    MainDir = CreateNewFile(MainDir, 'Main')
    MainDirText = MainDir + '\\testText'
    MainDirText = CreateNewFile(MainDirText, 'sub1')

    # sub1:
    # OECD_File_path = MainDir + f'\OECD {ToDay}'.
    # yahoo_finance_File_path = MainDir + f'\yahoo finance  {ToDay}.
    subDirList1 = [
        MainDir + '\OECD',
        MainDir + '\yahoo finance'
    ]

    NewsubDirList1 = []
    for sub1 in subDirList1:
        NewsubDirList1.append(CreateNewFile(sub1, 'sub1'))

    # sub2:
    # OECD_json_get_all_File_path = subDirList1[0] + f'\json_get_all {ToDay}'.
    # OECD_Schema_File_path = subDirList1[0] + f'\Schema {ToDay}'.
    # OECD_Criteria_merge_File_path = subDirList1[0] + f'\Oecd_merged {ToDay}'.
    subDirList2 = [
        NewsubDirList1[0] + '\json_get_all',
        NewsubDirList1[0] + '\Schema',
        NewsubDirList1[0] + '\Oecd_merged'
    ]
    # log:
    # LogFILE = os.path.join(MainDir, f'Main-Run {ToDay}.log').
    # LogFILE_Oecd = os.path.join(subDirList1[0], f'OECD {ToDay}.log').
    # LogFILE_YF = os.path.join(subDirList1[1], f'Yahoo finance {ToDay}.log').
    logList = [
        os.path.join(MainDir, 'Main-Run'),
        os.path.join(NewsubDirList1[0], 'OECD'),
        os.path.join(NewsubDirList1[1], 'Yahoo finance')
    ]

    NewsubDirList2 = []
    NewlogList = []
    for sub2, log in itertools.zip_longest(subDirList2, logList):
        NewsubDirList2.append(CreateNewFile(sub2, 'sub2'))
        NewlogList.append(CreateNewFile(log, 'log'))

    MainLogger = Log('Main_log', NewlogList[0], ToDay)
    OecdLogger = Log('Oecd_log', NewlogList[1], ToDay)
    YFLogger = Log('YF_log', NewlogList[2], ToDay)

    OecdFilepath = [NewsubDirList1[0], NewsubDirList2[0], NewsubDirList2[1], NewsubDirList2[2]]

    MainLogger.debug("Opening Chrome browser\n")
    browser = webdriver.Chrome(
        r'C:\Users\liran\OneDrive\Desktop\School\data scientist\Jhon Bryce\chromedriver.exe')

    MainLogger.debug("**Starting YahooFinanceAPI function\n")
    MainLogger.info(
        f"The Yahoo Finance Main file directory path is: {NewsubDirList1[1]} \n")

    # call the yahoo finance API
    YahooFinanceAPI.YahooFinanceAPI(NewsubDirList1[1], browser,
                                    YFLogger)

    MainLogger.debug("closing browser")
    # MainLogger.info(f'\nTotal {len(dfTotal)} set of sector data in the system!')
    browser.close()

    time.sleep(10)

    MainLogger.debug("**Starting OecdAPI function\n")
    MainLogger.info(f"The Oecd Main file directory path is: {NewsubDirList1[0]} \n")

    OecdAPI.OecdAPI(OecdFilepath, ToDay, OecdLogger)

    # schedule.every(1).day.at('01:30').do(job_that_executes_multi())

    # schedule.every().day.at('01:30').do(job_that_executes_once())

    MainLogger.debug("Log ended at %s", str(
        datetime.datetime.now().strftime("%d_%m_%Y %H:%M:%S %p")))

    return
