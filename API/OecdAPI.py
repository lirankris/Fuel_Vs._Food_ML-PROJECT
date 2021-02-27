import os
import pandas as pd
import datetime
import CreateText as ct
from CreateNewFile import CreateNewFile
import OECD_data_mining as ODM


def OecdAPI(OecdFilepath, ToDay, Logger):

    # url for data structure schema with families key.
    OecdsourceUrl = 'http://stats.oecd.org/sdmx-json/data/'
    OecdStructureUrl = 'http://stats.oecd.org/RESTSDMX/sdmx.ashx/GetDataStructure/ALL/'
    OecdschemaUrl = 'http://stats.oecd.org/restsdmx/sdmx.ashx/GetSchema/'

    path1 = OecdFilepath[0]  # Main file directory of OECD API path.
    path2 = OecdFilepath[1]  # file directory of OECD_json_get_all path.
    path3 = OecdFilepath[2]  # file directory of OECD_Schema path.
    path4 = OecdFilepath[3]  # file directory of OECD_Criteria_merge_File_path.

    # New json file OECD keys.
    NewKeysfiles = {
        'KeynamesFILE': os.path.join(path1, f'OECD_key_names {ToDay}.json'),
        'FrqnamesFILE': os.path.join(path1, f'FREQ_key_names {ToDay}.json')
    }

    for keyfile in NewKeysfiles:
        CreateNewFile(keyfile, 'json')
        # create New json file OECD keys.

    json_Key_File = ODM.OECD_Key_Familis(OecdStructureUrl, NewKeysfiles['KeynamesFILE'], Logger)

    if json_Key_File:
        Logger.debug('json_Key_File as succeeded')
        Logger.info('Reading df')
        df = pd.read_json(NewKeysfiles['KeynamesFILE'])
        ct.data2text(df, 'KeynamesFILE_df')
        keynames = df['KeyFId'].tolist()
        Logger.info('json_Key_File as succeeded')
    else:
        print("somthing got wrong!")
        Logger.debug('End of the Road: got stuck in OECD_Key_Families')
        return None

    success_count1, FilepathDatasets = ODM.OECD_json_get_all(
        OecdsourceUrl, NewKeysfiles['KeynamesFILE'], path2, keynames, Logger)

    success_count2, FilepathSchema = ODM.OECD_Schema(
        OecdschemaUrl, NewKeysfiles['KeynamesFILE'], path3, keynames, Logger)

    #ODM.OECD_json_get_timedout(path2, Logger)
    ODM.OECD_criteria_merge(path4, Logger)

    print("completed ...")
    print(len(keynames), " Dataset")
    print(success_count1, " datasets retrieved")
    print(success_count2, " SchemaS retrieved")

    Logger.debug("OECD API ended at:  %s", str(datetime.datetime.now()))
