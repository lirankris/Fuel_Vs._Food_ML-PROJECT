import os
import pandas as pd


def main():

    DataBasePath = r"C:\Users\liran\OneDrive\Desktop\School\data scientist\Jhon Bryce\DataBase"
    dictOced = {}
    dictYf = {}

    for file in os.listdir(DataBasePath):
        if 'Data_Set' in file:
            DataSetPath = os.path.join(DataBasePath, file)
            date = file.split(' ')
            for sub1file in os.listdir(DataSetPath):
                if f'OECD {date[1]}' in sub1file:
                    OECDPath = os.path.join(DataSetPath, sub1file)
                    for sub2file in os.listdir(OECDPath):
                        if 'json_get_all' in sub2file:
                            json_get_allPath = os.path.join(OECDPath, sub2file)
                            if os.path.getsize(json_get_allPath) == 0:
                                pass
                            else:
                                for jsonfile in os.listdir(json_get_allPath):
                                    dictOced[date[1]] = jsonfile

                elif f'yahoo finance {date[1]}' in sub1file:
                    YfPath = os.path.join(DataSetPath, sub1file)
                    if os.path.getsize(YfPath) == 0:
                        pass
                    else:
                        for jsonfile in os.listdir(YfPath):
                            if jsonfile.endswith('.json'):
                                dictYf[date[1]] = jsonfile

    dfOced =
    dfYf =

    #dfOced = pd.DataFrame.from_dict(many_jsons[0])
    #dfYf = pd.DataFrame.from_dict(many_jsons[0])


if __name__ == '__main__':
    main()
