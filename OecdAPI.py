import pandas as pd
import datetime
from CreateNewFile import CreateNewFile as cf
from CreateLogger import Log
import OECD_data_mining as ODM
from DataStandart import OECD_criteria_merge as OCM


def OecdAPI(OecdFilepath, ToDay):

    OecdLogPath = cf(FileDirPath=OecdFilepath, Pos='log', FileName="Oecd_log")
    OecdLogger = Log('Oecd_log', OecdLogPath)

    # sub2:
    # OECD_json_get_all_File_path = subDirList1[0] + f'\json_get_all {ToDay}'.
    # OECD_Schema_File_path = subDirList1[0] + f'\Schema {ToDay}'.
    # OECD_Criteria_merge_File_path = subDirList1[0] + f'\Oecd_merged {ToDay}'.
    subDirList2 = [
        OecdFilepath + '\Json_get_all',
        OecdFilepath + '\Schema',
        OecdFilepath + '\Oecd_merged'
    ]

    NewsubDirList2 = []

    for sub2 in subDirList2:
        NewsubDirList2.append(cf(FileDirPath=sub2, Pos='sub2'))

    # Url for data structure schema with families key.
    # Data:
    OecdsourceUrl = 'http://stats.oecd.org/sdmx-json/data/'
    # Data Structure:
    OecdStructureUrl = 'http://stats.oecd.org/RESTSDMX/sdmx.ashx/GetDataStructure/ALL/'
    # Schema:
    OecdschemaUrl = 'http://stats.oecd.org/restsdmx/sdmx.ashx/GetSchema/'

    # New json file OECD keys.
    Oecd_key_names = cf(FileDirPath=OecdFilepath,
                        FileName='OECD_key_names', Pos='json')
    # Freq_key_names = cf(FileDirPath=path1, FileName=f'FREQ_key_names {ToDay}.json', Pos='json')

    # create New json file OECD keys.

    json_Key_File = ODM.OECD_Key_Familis(OecdStructureUrl, Oecd_key_names, OecdLogger, OecdFilepath)

    if json_Key_File:
        OecdLogger.debug('json_Key_File as succeeded')
        OecdLogger.info('Reading df')

        df = pd.read_json(Oecd_key_names)
        keynames = df['KeyFId'].tolist()  # examples: 'QNA', 'SNA_TABLE11'....

        OecdLogger.info('json_Key_File as succeeded')
    else:
        print("somthing got wrong!")
        OecdLogger.debug('End of the Road: got stuck in OECD_Key_Families')
        return None

    # success_count2, FilepathSchema = ODM.OECD_Schema(
    #    OecdschemaUrl, NewsubDirList2[1], keynames, OecdLogger)

    success_count1, FilepathDatasets = ODM.OECD_json_get_all(
        OecdsourceUrl, NewsubDirList2[0], keynames, OecdLogger)

    # ODM.OECD_json_get_timedout(path2, Logger)
    OCM(NewsubDirList2[2], OecdLogger)

    print("completed ...")
    print(len(keynames), " Dataset")
    print(success_count1, " datasets retrieved")
    #print(success_count2, " SchemaS retrieved")

    OecdLogger.debug("OECD API ended at:  %s", str(datetime.datetime.now()))
