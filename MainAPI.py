import OecdAPI
from CreateNewFile import CreateNewFile as cf
from CreateLogger import Log
import datetime


def getDate():
    return str(datetime.date.today().strftime("%d_%m_%Y"))


def main():
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

    ToDay = getDate()

    # Main:
    MainDir = r"C:\Users\liran\OneDrive\Desktop\School\data scientist\Jhon Bryce\DataBase\Data_Set"

    MainDir = cf(FileDirPath=MainDir, Pos='Main')
    MainDirText = MainDir + '\\testText'
    MainDirText = cf(FileDirPath=MainDirText, Pos='sub1')

    # sub1:
    # OECD_File_path = MainDir + f'\OECD {ToDay}'.
    # yahoo_finance_File_path = MainDir + f'\yahoo finance  {ToDay}.
    subDirList1 = [
        MainDir + '\OECD',
        MainDir + '\yahoo finance'
    ]

    MainFilepath = []
    for sub1 in subDirList1:
        MainFilepath.append(cf(FileDirPath=sub1, Pos='sub1'))

    MainLogPath = cf(FileDirPath=MainDir, Pos='log', FileName="Oecd_log")
    MainLogger = Log('Main-Run', MainLogPath)

    # MainLogger.debug("Opening Chrome browser\n")
    # browser = webdriver.Chrome(
    # r'C:\Users\liran\OneDrive\Desktop\School\data scientist\Jhon Bryce\chromedriver.exe')

    # MainLogger.debug("**Starting YahooFinanceAPI function\n")
    # MainLogger.info(
    #    f"The Yahoo Finance Main file directory path is: {NewsubDirList1[1]} \n")

    # call the yahoo finance API
    # YahooFinanceAPI.YahooFinanceAPI(NewsubDirList1[1], browser,
    #                                YFLogger)

    # MainLogger.debug("closing browser")
    # MainLogger.info(f'\nTotal {len(dfTotal)} set of sector data in the system!')
    # browser.close()

    # time.sleep(10)

    MainLogger.debug("**Starting OecdAPI function\n")
    MainLogger.info(f"The Oecd Main file directory path is: {MainFilepath[0]} \n")
    OecdAPI.OecdAPI(MainFilepath[0], ToDay)

    # schedule.every(1).day.at('01:30').do(job_that_executes_multi())

    # schedule.every().day.at('01:30').do(job_that_executes_once())

    MainLogger.debug("Log ended at %s", str(
        datetime.datetime.now().strftime("%d_%m_%Y %H:%M:%S %p")))


if __name__ == '__main__':
    main()
