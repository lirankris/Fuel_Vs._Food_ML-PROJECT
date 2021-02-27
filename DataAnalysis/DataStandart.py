import os
import pandas as pd
import CreateText as ct
from OECD_data_mining import OECD_json_get_all as OJGA


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
    count, jsonDir = OJGA()
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
