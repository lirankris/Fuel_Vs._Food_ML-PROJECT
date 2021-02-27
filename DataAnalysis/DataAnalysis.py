import MainAPI as MAPI
import os
import json
import pandas as pd


def main():

    DataBasePath = r"C:\Users\liran\OneDrive\Desktop\School\data scientist\Jhon Bryce\DataBase"
    OcedFile = []
    YfFIle = []

    for file in os.listdir(DataBasePath):
        if os.path.isfile(os.path.join(DataBasePath, file)) and 'Data_Set' in file:
            DataSetName = os.path.join(DataBasePath, file)
            Filelist = os.listdir(DataSetName)
            if 'OECD' in Filelist:
                for Osubfile in Filelist:
                    if 'json_get_all' in Osubfile:
                        print(Osubfile)
                        OcedFile.append([jsonfile for jsonfile in os.listdir(
                            Osubfile) if jsonfile.endswith('.json')])

            elif 'yahoo finance' in Filelist:
                for Ysubfile in Filelist:
                    print(Ysubfile)
                    YfFIle.append([jsonfile for jsonfile in os.listdir(
                        Ysubfile) if jsonfile.endswith('.json')])


if __name__ == '__main__':
    main()
