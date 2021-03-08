from DataStandart import OECD_criteria_merge as OCM
from CreateLogger import Log


def main():
    # directorys :
    # [0]MainDir.

    # files :
    # [0]LogFILE.
    JsonPath = r'C:\Users\liran\OneDrive\Desktop\School\data scientist\Jhon Bryce\DataBase\Data_Set 27_02_2021\OECD 27_02_2021\json_get_all 27_02_2021'
    MainLogPath = r'C:\Users\liran\OneDrive\Desktop\projects\Offical_Projects\Oecd_and_YahooFinance_DataMining\Main\DataAnalysis'
    MainLogger = Log('Main_Data_Analysis_log', MainLogPath)
    DataPath = r'C:\Users\liran\OneDrive\Desktop\School\data scientist\Jhon Bryce\DataBase\analyze'
    OCM(MainLogger, JsonPath, DataPath)


if __name__ == '__main__':
    main()
