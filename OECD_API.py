import sys
import os
import pandas as pd
import requests as req
import xmltodict
import datetime
import pandasdmx

cwd = os.getcwd()
sys.path.append(f'{cwd}\DataFrames\CreateTools')
from CreateLogger import Log


# # ---------------------SDMX-JSON -----------------------------#


def OECD_Key_Familis(Url, Logger):
    Logger.warning('Starting to reach OECD key Family names')

    # Create a loop for a Session in the OECD Site (OecdStructureUrl) to get
    # the key family id's to reach all the data from OecdsourceUrl.

    # Url = 'http://stats.oecd.org/RESTSDMX/sdmx.ashx/GetDataStructure/ALL/'
    # KeynamesFILE (write)= ....'\OECD_key_names {ToDay}.json'
    # Logger = Oecd_log.

    # In: data from OECD server.
    # Out: OECD_key_names DataFrames

    try:
        GetRequest = req.get(Url, timeout=60)
    except req.exceptions.ReadTimeout:
        Logger.debug('Data read timed out')
    except req.exceptions.Timeout:
        Logger.debug('Data request timed out')
    except req.exceptions.HTTPError:
        Logger.debug('HTTP error')
    except req.exceptions.ConnectionError:
        Logger.debug('Connection error')
    else:
        if GetRequest.status_code == 200:
            # the request was received and understood and is being processed (Http code = 200).
            keyFamIdList = []  # key Family Id, example: QNA, OECD_TSE2010, AEO11_OVERVIEW_CHAPTER1_TAB1_PT,
            keyFamNameList = []  # key Family Name, example : Quarterly National Accounts, Patent indicators
            keyfamilies_dict = xmltodict.parse(GetRequest.text)
            keyFamilies = keyfamilies_dict['message:Structure']['message:KeyFamilies']['KeyFamily']

            # <message:Structure>
            #       <message:KeyFamilies>
            #           <KeyFamily>
            #               **keyFamily**
            #           </KeyFamily>
            #       </message:KeyFamilies>
            # </message:Structure>

            for keyF in keyFamilies:
                keyfam_id = keyF['@id']
                keyFamIdList.append(keyfam_id)
                keyNames = keyF['Name']

                #  checking if keyNames is a list or a dictionary:
                if isinstance(keyNames, list):
                    for keyN in keyNames:
                        try:
                            keyfam_lang = keyN['@xml:lang']
                            # example:    <xs:documentation xml:lang="en">Experimental value</xs:documentation>
                            # Insert family keyfam_text the text for the given keyNames.
                            if keyfam_lang == 'en':  # if the language is english.
                                # get a object name, example: Information, communication.
                                keyfam_text = keyN['#text']
                                keyFamNameList.append(keyfam_text)
                        except KeyError as err1:
                            print(f'Something want wrong this is the problem: {err1}')
                            Logger.debug(f"No @xml:lang/#text key in {keyN}")

                        Logger.debug(
                            f'\nThis is the key famly id: {keyfam_id}. \n and name list: {keyfam_text}!')
                elif isinstance(keyNames, dict):
                    try:
                        keyfam_lang = keyNames['@xml:lang']  # get a language.
                        if keyfam_lang == 'en':  # if the language is english.
                            # Insert family keyfam_text the text for the given keyNames.
                            keyfam_text = keyNames['#text']
                            keyFamNameList.append(keyfam_text)
                    except KeyError as err2:
                        print(f'Something want wrong this is the problem: {err2}')
                        Logger.debug(f"No @xml:lang/#text key in {keyNames}")
                Logger.debug(
                    f'\nThis is the key famly id: {keyfam_id}. \n and name list: {keyfam_text}!')
            # Create data frame with the index of key Family Id and key Family Name.
            keyFamdf = pd.DataFrame.from_dict(
                {'KeyFId': keyFamIdList, 'KeyFName': keyFamNameList}, orient='columns')
            Logger.debug("finished creating key Family as a json file.")
            return keyFamdf

        else:
            print('HTTP Failed', GetRequest.status_code)
            Logger.debug('HTTP Failed with code %d', GetRequest.status_code)
            return False


'/////////////////////////////////////////////////////////////////////////////'


def OECD_dataset_name(keynames, Logger):
    GBARD_YEAR = ''
    GBARD = ''
    CUR_TABLE = ''

    HIGH_AGLINK_YEAR = ''
    HIGH_AGLINK = ''

    Logger.debug('Starting to get datasets names..')

    for dataset_id in keynames:
        if 'GBARD' in dataset_id:
            year = dataset_id.split('_')[1].split('S')[1]
            if year > GBARD_YEAR:
                GBARD_YEAR = year
                GBARD = dataset_id

        if 'HIGH_AGLINK' in dataset_id:
            year = dataset_id.split('_')[2]
            if year > HIGH_AGLINK_YEAR:
                HIGH_AGLINK_YEAR = year
                HIGH_AGLINK = dataset_id

        if dataset_id == 'SNA_TABLE4':
            CUR_TABLE = dataset_id

    dataset_ids = [GBARD, HIGH_AGLINK, CUR_TABLE]

    Logger.debug(f'Finished, Selected datasets are: {GBARD, HIGH_AGLINK, CUR_TABLE}')

    return dataset_ids


'/////////////////////////////////////////////////////////////////////////////'


def get_df(data_response, Logger):
    try:
        oecd_data = data_response
        df = pandasdmx.to_pandas(oecd_data,
                                 datetime=dict(dim='TIME_PERIOD', axis=1))
    except req.exceptions.ConnectionError as err:
        Logger.critical(f'response took too long, this is the error: {err}')
    return df


'/////////////////////////////////////////////////////////////////////////////'


def OECD_dataset(dataset_ids, Logger):
    Logger.warning('Trying to get data form OECD.stat')
    oecd = pandasdmx.Request('OECD')
    params = dict(startPeriod='1990-Q1',
                  endPeriod='2021-Q1',
                  dimensionAtObservation='TimeDimension',
                  detail='Full')
    dfs = []

    for dataset in dataset_ids:
        if 'GBARD' in dataset:
            try:
                Logger.warning(f'Loading {dataset} from OECD database')
                data_response = oecd.data(resource_id=dataset,
                                          params=params)
                df = get_df(data_response, Logger)
                Logger.debug(f'flattening {dataset} df')
                df.reset_index(level=['COUNTRY',
                                      'SEO',
                                      'MEASURE'],
                               inplace=True)
                sort_df: object = df.melt(id_vars=['COUNTRY',
                                                   'SEO',
                                                   'MEASURE'],
                                          var_name="Date",
                                          value_name="Value")

            except req.exceptions.ConnectionError as err:
                Logger.warning(f'This {dataset} got this error: {err}')
                print(f'This dataset: {dataset} as failed to response')
                continue

        elif 'HIGH_AGLINK' in dataset:
            try:
                Logger.warning(f'Loading {dataset} from OECD database')
                data_response = oecd.data(resource_id=dataset,
                                          params=params)
                df = get_df(data_response, Logger)
                Logger.debug(f'flattening {dataset} df')
                df.reset_index(level=['LOCATION',
                                      'COMMODITY',
                                      'VARIABLE'],
                               inplace=True)
                sort_df: object = df.melt(id_vars=['LOCATION',
                                                   'COMMODITY',
                                                   'VARIABLE'],
                                          var_name="Date",
                                          value_name="Value")

            except req.exceptions.ConnectionError as err:
                Logger.warning(f'This {dataset} got this error: {err}')
                print(f'This dataset: {dataset} as failed to response')
                continue

        elif 'SNA_TABLE4' in dataset:
            try:
                Logger.warning(f'Loading {dataset} from OECD database')
                data_response = oecd.data(resource_id=dataset,
                                          params=params)

                df = get_df(data_response, Logger)
                Logger.debug(f'flattening {dataset} df')
                df.reset_index(level=['LOCATION',
                                      'TRANSACT',
                                      'MEASURE'],
                               inplace=True)
                sort_df: object = df.melt(id_vars=['LOCATION',
                                                   'TRANSACT',
                                                   'MEASURE'],
                                          var_name="Date",
                                          value_name="Value")

            except req.exceptions.ConnectionError as err:
                Logger.warning(f'This {dataset} got this error: {err}')
                print(f'This dataset: {dataset} as failed to response')
                continue

        dfs.append(sort_df)

    if len(dfs) == 3:
        Logger.debug('Success')
        print('Success')
    else:
        Logger.info(f'Only {len(dfs)} dataset were found')
        print(f'Only {len(dfs)} dataset were found')

    return dfs


'/////////////////////////////////////////////////////////////////////////////'


def OECD_get_id_df(dataset_ids, Logger):
    logging = Logger
    schemaUrl = 'http://stats.oecd.org/restsdmx/sdmx.ashx/GetSchema/'

    # GBARD
    G_country_id = []
    G_country_full_name = []

    seo_id = []
    seo_full_name = []

    # HIGH_AGLINK
    A_country_id = []
    A_country_full_name = []

    commodity_id = []
    commodity_full_name = []

    variable_id = []
    variable_full_name = []

    with req.Session() as reqSe:
        for keyname in dataset_ids:
            try:
                Request = reqSe.get(schemaUrl + keyname, timeout=61)
            except req.exceptions.ReadTimeout:
                print(keyname, ": Data request read timed out")
                logging.debug('%s: Data read timed out', keyname)
            except req.exceptions.Timeout:
                print(keyname, ": Data request timed out")
                logging.debug('%s: Data request timed out', keyname)
            except req.exceptions.HTTPError:
                print(keyname, ": HTTP error")
                logging.debug('%s: HTTP error', keyname)
            except req.exceptions.ConnectionError:
                print(keyname, ": Connection error")
                logging.debug('%s: Connection error', keyname)
            else:
                if Request.status_code == 200:

                    #             Example:
                    #                         <xs:enumeration value="BEL">
                    #                             <xs:annotation>
                    #                                 <xs:documentation xml:lang="en">Belgium</xs:documentation>
                    #                                 <xs:documentation xml:lang="fr">Belgique</xs:documentation>
                    #                             </xs:annotation>
                    #                         </xs:enumeration>

                    keyfamilies_dict = xmltodict.parse(Request.text)
                    selected_dict = keyfamilies_dict[list(keyfamilies_dict.keys())[0]]
                    simpleType = selected_dict['xs:simpleType']

                    if 'GBARD' in keyname:
                        for sp in simpleType:
                            sp_name = sp['@name']
                            try:
                                if 'COUNTRY' in sp_name:
                                    for country in sp['xs:restriction']['xs:enumeration']:
                                        # id english country name.
                                        G_country_id.append(country['@value'])
                                        # full english country name.
                                        G_country_full_name.append(country['xs:annotation']
                                                                   ['xs:documentation']
                                                                   [0]['#text'])
                                elif 'SEO' in sp_name:
                                    for country in sp['xs:restriction']['xs:enumeration']:
                                        # id english seo name.
                                        seo_id.append(country['@value'])
                                        # full english seo name.
                                        seo_full_name.append(country['xs:annotation']
                                                             ['xs:documentation']
                                                             [0]['#text'])
                            except KeyError as err:
                                print(f'problem in {err}')
                                continue

                    elif 'HIGH_AGLINK' in keyname:
                        for sp in simpleType:
                            sp_name = sp['@name']
                            try:
                                if 'LOCATION' in sp_name:
                                    for country in sp['xs:restriction']['xs:enumeration']:
                                        # id english country name.
                                        A_country_id.append(country['@value'])
                                        # full english country name.
                                        A_country_full_name.append(country['xs:annotation']
                                                                   ['xs:documentation']
                                                                   [0]['#text'])
                                elif 'COMMODITY' in sp_name:
                                    for country in sp['xs:restriction']['xs:enumeration']:
                                        # id english seo name.
                                        commodity_id.append(country['@value'])
                                        # full english seo name.
                                        commodity_full_name.append(country['xs:annotation']
                                                                   ['xs:documentation']
                                                                   [0]['#text'])

                                elif 'VARIABLE' in sp_name:
                                    for country in sp['xs:restriction']['xs:enumeration']:
                                        # id english seo name.
                                        variable_id.append(country['@value'])
                                        # full english seo name.
                                        variable_full_name.append(country['xs:annotation']
                                                                  ['xs:documentation']
                                                                  [0]['#text'])
                            except KeyError as err:
                                print(f'problem in {err}')
                                continue

                else:
                    print(keyname, Request.status_code)
                    logging.debug('%s HTTP Failed with code %d', keyname, Request.status_code)

    GBARD_country_df = pd.DataFrame({"country_id": G_country_id,
                                     "country_full_name": G_country_full_name})
    GBARD_seo_df = pd.DataFrame({"seo_id": seo_id,
                                 "seo_full_name": seo_full_name})
    Agri_country_df = pd.DataFrame({"country_id": A_country_id,
                                    "country_full_name": A_country_full_name})
    Agri_commodity_df = pd.DataFrame({"commodity_id": commodity_id,
                                      "commodity_full_name": commodity_full_name})
    Agri_variable_df = pd.DataFrame({"variable_id": variable_id,
                                     "variable_full_name": variable_full_name})

    dfs = GBARD_country_df, \
          GBARD_seo_df, \
          Agri_country_df, \
          Agri_commodity_df, \
          Agri_variable_df

    return dfs


'////////////////////////////////////////////////////////////////////'


def OecdAPI():
    OecdLogger = Log('Oecd_log', cwd)
    # Url for data structure schema with families key.
    OecdStructureUrl = 'http://stats.oecd.org/RESTSDMX/sdmx.ashx/GetDataStructure/ALL/'

    # create New json file OECD keys.
    json_Key_File = OECD_Key_Familis(
        OecdStructureUrl, OecdLogger)

    if not json_Key_File.empty:
        OecdLogger.debug('json_Key_File as succeeded')
        OecdLogger.info('Reading df')

        key_name_df = json_Key_File
        keynames = key_name_df['KeyFId'].tolist()  # examples: 'QNA', 'SNA_TABLE11'....
        OecdLogger.info('json_Key_File as succeeded')
    else:
        print("somthing got wrong!")
        OecdLogger.debug('End of the Road: got stuck in OECD_Key_Families')
        return None

    dataset_ids = OECD_dataset_name(keynames, OecdLogger)
    try:
        GBARD_df, Agri_df, Usd2conv_df = OECD_dataset(dataset_ids, OecdLogger)
    except ValueError as err:
        OecdLogger.debug(f"Not all of the Datasets got response, we get this error {err}")
        print(f"Not all of the Datasets got response, we get this error {err}")
        pass

    GBARD_country_df, \
    GBARD_seo_df, \
    Agri_country_df, \
    Agri_commodity_df, \
    Agri_variable_df = OECD_get_id_df(dataset_ids, OecdLogger)

    print("completed ...")
    OecdLogger.debug("OECD API ended at:  %s", str(datetime.datetime.now()))

    dfs = GBARD_df, Agri_df, Usd2conv_df, GBARD_country_df, \
          GBARD_seo_df, Agri_country_df, Agri_commodity_df, \
          Agri_variable_df

    return dfs
