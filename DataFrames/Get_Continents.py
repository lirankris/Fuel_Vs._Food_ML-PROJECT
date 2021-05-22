import sys
import os
import pandas as pd

cwd = os.getcwd()
sys.path.append(f'{cwd}\DataFrames')
sys.path.append(f'{cwd}\DataFrames\CreateTools')


def DivideByContinents(df, country_df):
    cwd = os.getcwd()
    filespath = rf'{cwd}\continents'
    filelist = os.listdir(filespath)
    continents = {}
    dfs_countrys_full_name = list(country_df.country_full_name)

    for file in filelist:
        with open(f'{filespath}\\{file}', 'r',
                  encoding="utf8") as f:  # open text file with all the countries per continent.
            countries = []
            for c in f.readlines():
                country = c.split("\n")[0]
                if country in dfs_countrys_full_name:  # if country from text file in df.
                    countries.append(country)
            continents[(str(file).split('.')[
                0]).lower()] = countries  # add all the countries per continent to the dataset continents.

    commodities = df.COMMODITY.unique()
    variables = df.VARIABLE.unique()

    continents_df = pd.DataFrame()
    continents_df_1990 = pd.DataFrame()
    continents_df_2020 = pd.DataFrame()

    for continent in continents:
        for country in continents[continent]:
            country_id = list(country_df[country_df.country_full_name == country].country_id)[0]
            for commodity in commodities:
                for var in variables:
                    temp_df = df[(df.COUNTRY == country_id) &
                                 (df.VARIABLE == var) &
                                 (df.COMMODITY == commodity)]

                    temp_df.insert(0, 'CONTINENT', continent)
                    continents_df = continents_df.append(temp_df)

                    try:
                        df_1990 = temp_df[temp_df.YEAR == 1990]
                        continents_df_1990 = continents_df_1990.append(df_1990)

                    except IndexError:
                        print(f'{country} have no values in {var} for {commodity} in year 1990')
                        continue

                    try:
                        df_2020 = temp_df[temp_df.YEAR == 2020]
                        continents_df_2020 = continents_df_2020.append(df_2020)
                    except IndexError:
                        print(f'{country} have no values in {var} for {commodity} in year 2020')
                        continue

    continents_datasets = {'continents': continents_df,
                           'continents_1990': continents_df_1990,
                           'continents_2020': continents_df_2020}

    print(continents_datasets['continents'])
    print(continents_datasets['continents_1990'])
    print(continents_datasets['continents_2020'])

    return continents_datasets
