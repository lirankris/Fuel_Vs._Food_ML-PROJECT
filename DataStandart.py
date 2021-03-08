import os
import json
import pandas as pd


def standardize_data(dset_id, df, FilePath):
    # standardized column names
    stdcol_dict = {'Time Period': 'YEAR',
                   'Observation': 'series',
                   'Industry': 'INDUSTRY',
                   'Measure': 'MEASURE',
                   'Country': 'NATION'}

    cols = df.columns.values.tolist()  # get's the df columns and turn them to list.
    print(dset_id, cols)

    # for test
    # original_df = df

    # first deal with any potential tuple columns
    # e.g. 'Country - distribution'
    tuple_col = 'Country - distribution'
    if tuple_col in cols:  # 'Country - distribution' in the data frame column.
        split_list = tuple_col.split(' - ')  # [Country, distribution]

        for n, col in enumerate(split_list):  # 0 col1, 1 col2, 2 col3, 3 col4 ....
            df[col] = df[tuple_col].apply(lambda x: x.split('-')[n])
            # example: df['Country'](values) = df['Country - distribution'](values).split('-')[0]
        df = df.drop(tuple_col, axis=1)  # delete column 'Country - distribution'

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
            df.rename({cname: 'NATION'}, axis=1, inplace=True)
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


def OECD_criteria_merge(Logger, path, FilePath):
    # criteria
    criteria = ['Industry', 'Activity', 'ISIC3', 'Sector']
    candidates = []
    column_name = []
    jsonDir = path
    StructureNames = []

    count = 0
    countCan = 0
    countCan = 0
    countCol = 0
    interLength = 0
    # iterate through each JSON file in the directory and analyse it
    for filename in os.listdir(jsonDir):
        if filename.endswith(".json"):
            dsetid = os.path.splitext(filename)[0]
            fromfile = os.path.join(jsonDir, filename)
            # example: C:\Users\liran\OneDrive\Desktop\School\data scientist\
            # Jhon Bryce\DataBase\Data_Set 27_02_2021\OECD 27_02_2021\
            # json_get_all 27_02_2021\AFA_IN3
            # oecd_dataset_df = pd.read_json(fromfile)
            try:
                oecd_dataset = json.load(open(fromfile))  # from json to dict.
            except json.decoder.JSONDecodeError:
                count += 1
                pass

            oecd_dataset_df = pd.json_normalize(oecd_dataset, max_level=1)
            oecd_dataset_df.to_csv('out.csv', index=True)
            break
            oecd_cols = oecd_dataset_df.columns.values.tolist()
            for col in oecd_cols:
                print(col)
                break
            print(
                f"oecd_dataset_df['structure.description']: {oecd_dataset_df['structure.description'][0]}")
            StructureNames.append(oecd_dataset_df['structure.description'][0])
            # create a list of columns names.
            if any(k in criteria for k in oecd_cols):
                # looks for evidence of a column matching one of the column criteria
                # any() returns True if any of the (oecd column in criteria) == True.
                intersection = list(set(criteria) & set(oecd_cols))
                interLength += 1
                # get a list only of string in both variables.
                candidates.append(dsetid)  # get file name and add to candidates.
                countCan += 1
                occurrence = next((x for x in intersection if x == criteria[0]), None)

                # if criteria[0]='Industry' equals to intersection[i] get intersection[i+1].
                if occurrence is None:  # there is no next item.
                    column_name.append(intersection[0])
                    countCol += 1
                    # intersection[0]= criteria[0] = 'Industry' | 'Activity' | 'ISIC3' | 'Sector'
                else:
                    column_name.append(occurrence)
                    countCol += 1
                    # column_name = occurrence, candidates = file names.

    print(
        f'oecd_dataset: {count} of {len(os.listdir(jsonDir))}, Total {len(os.listdir(jsonDir)) - count} succeeded')
    Logger.debug(
        f'oecd_dataset: {count} of {len(os.listdir(jsonDir))}, Total {len(os.listdir(jsonDir)) - count} succeeded')
    print(
        f'candidates: {countCan} of {len(os.listdir(jsonDir))}, Total {len(os.listdir(jsonDir)) - countCan} Failed')
    Logger.debug(
        f'candidates: {countCan} of {len(os.listdir(jsonDir))}, Total {len(os.listdir(jsonDir)) - countCan} Failed')
    print(
        f'column_name: {countCol} of {interLength}, Total {interLength - countCol} Failed')
    Logger.debug(
        f'column_name: {countCol} of {interLength}, Total {interLength - countCol} Failed')

    # create candidate DataFrame
    candidates_df = pd.DataFrame({'KeyFamilyId': candidates, 'ColumnName': column_name})

    # diagnostic info
    print(len(candidates), 'Industry candidates found')

    # criteria
    industryTypeKey = 'ELECTRICITY'
    hasTarget = []

    # find which have data on target industry type
    for row in candidates_df.iterrows():
        datasetId = row[1]['KeyFamilyId']
        print(f'this is the candidates row KeyFamilyId: {datasetId}')
        Logger.debug(f'this is the candidates row KeyFamilyId: {datasetId}')
        colName = row[1]['ColumnName']
        print(f'this is the candidates cloumn name: {colName}')
        Logger.debug(f'this is the candidates cloumn name: {colName}')

        dataset_df = pd.read_json(os.path.join(jsonDir, datasetId + '.json'))
        print('checking', datasetId)

        try:
            filtered_df = dataset_df[dataset_df[colName].str.startswith(industryTypeKey)]
            # if  dataset_df[cloumn name] don't start with ELECTRICITY raise error.
        except ValueError:
            # all NaNs in target column, nothing to see here - move on
            pass
        else:
            if len(filtered_df.index):  # non-empty DataFrame
                hasTarget.append(datasetId)  # add KeyFamilyId from json file.
                # call stage 3
                ProcDir = standardize_data(datasetId, filtered_df, jsonDir)

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
