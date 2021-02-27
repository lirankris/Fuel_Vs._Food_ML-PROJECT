import os
import pandas as pd
import requests as req
import xmltodict
import lxml.etree as etree
import CreateText as ct


def OECD_Key_Familis(OecdStructureUrl, KeynamesFILE, Logger):

    Logger.warning('Starting to reach OECD key Family names')
    # Create a loop for the Session in the OECD Site.
    # In: data from OECD server.
    # Out: OECD_keys/OECD_key_names.json

    try:
        GetRequest = req.get(OecdStructureUrl, timeout=40)
    except req.exceptions.ReadTimeout:
        print("Data request read timed out")
        Logger.debug('Data read timed out')
    except req.exceptions.Timeout:
        print("Data request timed out")
        Logger.debug('Data request timed out')
    except req.exceptions.HTTPError:
        print("HTTP error")
        Logger.debug('HTTP error')
    except req.exceptions.ConnectionError:
        print("Connection error")
        Logger.debug('Connection error')
    else:
        if GetRequest.status_code == 200:
            # the request was received and understood and is being processed (Http code = 200).
            keyFamIdList = []
            keyFamNameList = []

            keyfamilies_dict = xmltodict.parse(GetRequest.text)
            keyFamilies = keyfamilies_dict['message:Structure']['message:KeyFamilies']['KeyFamily']

            for keyF in keyFamilies:

                keyfam_id = keyF['@id']
                keyFamIdList.append(keyfam_id)
                keyNames = keyF['Name']

                if isinstance(keyNames, list):  # checks if the keyNames is an instance of list.
                    for keyN in keyNames:
                        try:
                            keyfam_lang = keyN['@xml:lang']
                            # Insert family keyfam_text the text for the given keyNames.
                            if keyfam_lang == 'en':  # if the language is english.
                                keyfam_text = keyN['#text']   # get a language.
                                keyFamNameList.append(keyfam_text)
                        except KeyError:
                            Logger.debug("No @xml:lang/#text key in {}".format(keyN))

                # checks if the keyNames is an instance of dictionary.
                elif isinstance(keyNames, dict):
                    try:
                        keyfam_lang = keyNames['@xml:lang']  # get a language.
                        if keyfam_lang == 'en':   # if the language is english.
                            # Insert family keyfam_text the text for the given keyNames.
                            keyfam_text = keyNames['#text']
                            keyFamNameList.append(keyfam_text)
                    except KeyError:
                        Logger.debug("No @xml:lang/#text key in {}".format(keyNames))
                Logger.debug(
                    f'\nThis is the key famly id: {keyfam_id}. \n and name list: {keyfam_text}!')
            # Create data frame with the index of key Family Id and key Family Name.
            keyFamdf = pd.DataFrame.from_dict(
                {'KeyFId': keyFamIdList, 'KeyFName': keyFamNameList}, orient='index')
            keyFamdf.to_json(KeynamesFILE, orient="index")
            Logger.debug("finished creating key Family as a json file.")
            Logger.info(f"key Family file path is: {KeynamesFILE}")
            return True

        else:
            print('HTTP Failed', GetRequest.status_code)
            Logger.debug('HTTP Failed with code %d', GetRequest.status_code)
            return False


'/////////////////////////////////////////////////////////////////////////////'


def OECD_Schema(Url, KeynamesFILE, Paths, keynames, Logger):

    # Create a for loop with a lode bar for the Session in the OECD Site.
    # In: data from OECD server; OECD_keys/OECD_key_names.csv
    # Out: OECD_schema/<dataset id>.xml

    success_count = 0  # Reset the count of success in attempts of requests.

    Logger.warning('Starting to reach out Oecd Data source for xml schema')

    with req.Session() as ReqS:
        for keyname in keynames:
            try:
                GetRequest = ReqS.get(Url[0] + keyname, timeout=40)
            except req.exceptions.ReadTimeout:
                print(keyname, ": Data request read timed out")
                Logger.debug('%s: Data read timed out', keyname)
                ct.data2text(keyname, 'jsonReadTimeout', 'text')
            except req.exceptions.Timeout:
                print(keyname, ": Data request timed out")
                Logger.debug('%s: Data request timed out', keyname)
                ct.data2text(keyname, 'request_timed_out', 'text')
            except req.exceptions.HTTPError:
                print(keyname, ": HTTP error")
                Logger.debug('%s: HTTP error', keyname)
                ct.data2text(keyname, 'jsonHTTP_error', 'text')
            except req.exceptions.ConnectionError:
                print(keyname, ": Connection error")
                Logger.debug('%s: Connection error', keyname)
                ct.data2text(keyname, 'jsonConnection_error', 'text')

            else:
                if GetRequest.status_code == 200:  # success to get Keys.
                    target1 = os.path.join(Paths[1], 'OECD_Schema' + ' ' + keyname + ".xml")
                    tree = etree.fromstring(GetRequest.text)
                    pretty_xml_str = etree.tostring(tree, pretty_print=True).decode("utf-8")

                    # write to a new text file all the schema data.
                    with open(target1, 'w', encoding='utf-8') as f:
                        f.write(pretty_xml_str)
                        success_count += 1
                else:
                    print(keyname, GetRequest.status_code)
                    Logger.debug('%s HTTP Failed with code %d',
                                 keyname, GetRequest.status_code)
    return success_count, target1


'/////////////////////////////////////////////////////////////////////////////'


def OECD_json_get_all(Url, KeynamesFILE, Path, keynames, Logger):

    # Create a for loop with a lode bar for the Session in the OECD Site.
    # In: data from OECD server; OECD_keys/OECD_key_names.csv
    # Out: OECD_json_datasets/<dataset id>.json

    Logger.warning('Starting to reach out Oecd Data source for json_get_all')

    success_count = 0  # Reset the count of success in attempts of requests.

    with req.Session() as ReqS:
        for dataset_id in keynames:
            try:
                GetRequest = ReqS.get(Url + dataset_id + '/all/all', timeout=40)
            except req.exceptions.ReadTimeout:
                print(dataset_id, ": OECD data request read timed out")
                Logger.debug('%s: OECD data request read timed out', dataset_id)
            except req.exceptions.Timeout:
                print(dataset_id, ": OECD data request timed out")
                Logger.debug('%s: OECD data request timed out', dataset_id)
            except req.exceptions.HTTPError:
                print(dataset_id, ": HTTP error")
                Logger.debug('%s: HTTP error', dataset_id)
            except req.exceptions.ConnectionError:
                print(dataset_id, ": Connection error", )
                Logger.debug('%s: Connection error', dataset_id)
            else:
                if GetRequest.status_code == 200:  # success to get dataset.
                    target2 = os.path.join(Path, dataset_id + ".json")

                    # write to a new text file of the source data.
                    with open(target2, 'w', encoding='utf-8') as file:
                        file.write(GetRequest.text)
                        success_count += 1

                else:
                    print(dataset_id, 'HTTP Failed with code', GetRequest.status_code)
                    Logger.debug('%s HTTP Failed with code %d',
                                 dataset_id, GetRequest.status_code)

    return success_count, target2


'/////////////////////////////////////////////////////////////////////////////'


def standardize_data(dset_id, df, FilePath):
    # standardized column names
    stdcol_dict = {'Time Period': 'YEAR',
                   'Observation': 'series',
                   'Industry': 'INDUSTRY',
                   'Measure': 'MEASURE',
                   'Country': 'NATION'}

    cols = df.columns.values.tolist()
    print(dset_id, cols)

    # for test
    # original_df = df

    # first deal with any potential tuple columns
    # e.g. 'Country - distribution'
    tuple_col = 'Country - distribution'
    if tuple_col in cols:  # 'Country - distribution' in the data frame column.
        split_list = tuple_col.split(' - ')  # [Country, distribution]

        for n, col in enumerate(split_list):
            # df[col] = df['Country - distribution'].apply(lambda x: x.split('-')[0,1,2...])
            df[col] = df[tuple_col].apply(lambda x: x.split('-')[n])
        df = df.drop(tuple_col, axis=1)

    df2text = ct.data2text(df.values, 'standardize_data_df')
    print(df2text)
    # rename common occurrence column names
    # 'Time Period' to 'YEAR', 'Observation' to 'series'
    # 'Industry' to 'INDUSTRY', 'Country' to 'NATION'
    df.rename(stdcol_dict, axis='columns', inplace=True)
    cols = df.columns.values.tolist()
    print(cols)

    # Industry 'other' rename
    industry_renames = ['Activity', 'ISIC3', 'Sector']
    # for all columns in dataframe if loop var (k) in ['Activity', 'ISIC3', 'Sector'] at all.
    if any(k in industry_renames for k in cols):
        no = list(set(industry_renames) & set(cols))
        df.rename(columns={no[0]: 'INDUSTRY'}, inplace=True)
        cols = df.columns.values.tolist()
        print(cols)

    # Country 'other' rename - has do be done in order
    # 'Country - distribution' is a special case already dealt with above
    country_renames = ['Declaring country', 'Partner country', 'Reporting country']
    for cname in country_renames:
        if cname in cols:
            df.rename({cname: 'NATION'}, axis='columns', inplace=True)
            break
    cols = df.columns.values.tolist()
    print(f'dset_id is : {dset_id}', cols)

    # now find columns that are not YEAR, series, INDUSTRY, MEASURE or NATION
    stdcols_list = []
    nonstdcols_list = []
    measurecol = False

    for k in stdcol_dict:
        stdcols_list.append(stdcol_dict[k])
    for cname in cols:
        if cname not in stdcols_list:
            nonstdcols_list.append(cname)
        elif not measurecol and cname == 'MEASURE':
            measurecol = True
    if nonstdcols_list:
        if measurecol:
            df = df.rename(columns={'MEASURE': 'temp'})
            nonstdcols_list.append('temp')
        df['MEASURE'] = df[nonstdcols_list].apply(lambda x: ','.join(x), axis=1)
        df.drop(nonstdcols_list, axis=1, inplace=True)

    cols = df.columns.values.tolist()
    print(dset_id, nonstdcols_list, measurecol)
    print(dset_id, cols)
    df.set_index('YEAR', inplace=True)
    df.to_json(os.path.join(FilePath, dset_id + '_C.json'))

    return FilePath


'/////////////////////////////////////////////////////////////////////////////'

# STAGE 1: OECD data set JSON analysis for data sets covering industries


def OECD_criteria_merge(FilePath, Logger):
    # criteria
    criteria = ['Industry', 'Activity', 'ISIC3', 'Sector']
    candidates = []
    column_name = []
    count, jsonDir = OECD_json_get_all()
    # iterate through each JSON file in the directory and analyse it
    for filename in os.listdir(jsonDir):
        if filename.endswith(".json"):
            dsetid = os.path.splitext(filename)[0]
            fromfile = os.path.join(jsonDir, filename)  # full JSON file path.
            print(dsetid)

            oecd_dataset_df = pd.read_json(fromfile)
            oecd_cols = oecd_dataset_df.columns.values.tolist()  # create a list of columns names.

            if any(k in criteria for k in oecd_cols):
                intersection = list(set(criteria) & set(oecd_cols))
                candidates.append(dsetid)
                occurrence = next((x for x in intersection if x == criteria[0]), None)
                if occurrence is None:
                    column_name.append(intersection[0])
                else:
                    column_name.append(occurrence)
                print(dsetid, intersection, occurrence)

    # create candidate DataFrame
    candidates_df = pd.DataFrame({'KeyFamilyId': candidates, 'ColumnName': column_name})

    # diagnostic info
    print(len(candidates), 'industry candidates found')

    # STAGE 2 : analysis of OECD industry related data set for specific industry criteria

    # criteria
    industryTypeKey = 'ELECTRICITY'
    hasTarget = []

    # find which have data on target industry type
    for row in candidates_df.iterrows():
        datasetId = row[1]['KeyFamilyId']
        colName = row[1]['ColumnName']

        dataset_df = pd.read_json(os.path.join(jsonDir, datasetId + '.json'))
        print('checking', datasetId)

        try:
            filtered_df = dataset_df[dataset_df[colName].str.startswith(industryTypeKey)]
        except ValueError:
            # all NaNs in target column, nothing to see here - move on
            pass
        else:
            if len(filtered_df.index):
                # non-empty DataFrame
                hasTarget.append(datasetId)
                # call stage 3
                ProcDir = standardize_data(datasetId, filtered_df, FilePath)

    # diagnostic info
    print(len(hasTarget), 'beginning with', industryTypeKey)
    print(hasTarget)

    # target data frame
    def_cols = ['YEAR', 'series', 'INDUSTRY', 'NATION', 'MEASURE']
    combined_df = pd.DataFrame(columns=def_cols)

    #  STAGE 4. Iterate through each JSON file in the directory and concatenate it
    for filename in os.listdir(ProcDir):
        if filename.endswith('_C.json'):
            fname = os.path.splitext(filename)[0]
            fromfile = os.path.join(ProcDir, filename)
            print(f'fname is: {fname}')
            print(f'fromfile is: {fromfile}')

            source_df = pd.read_json(fromfile)
            list_of_series = [source_df[def_cols[0]], source_df[def_cols[1]], source_df[def_cols[2]],
                              source_df[def_cols[3]], source_df[def_cols[4]]]
            stripped_df = pd.concat(list_of_series, axis=1)
            combined_df = pd.concat([combined_df, stripped_df])

    combined_df.set_index('YEAR', inplace=True)
    combined_df.to_json(os.path.join(FilePath, 'oecd_merged.json'))

    print('criteria_merge completed ...')
