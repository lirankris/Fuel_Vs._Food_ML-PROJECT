import sys
import os
import pandas as pd
import numpy as np
import sqlite3 as sq3
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import mean_squared_error, r2_score
import copy
from scipy import stats


def get_filtered_dfs(dfs: list):
    filtered_dfs = {}

    for df in dfs:
        var_name = f'{df.VARIABLE.unique()[0]}_df'
        filter_value = df.Agri_Values.max() / 100
        filter_df = df[df.Agri_Values < filter_value]
        counts = filter_df.COUNTRY.value_counts()
        mask = df.COUNTRY.isin(counts[counts > 200].index).copy()  # lower value countries index's.
        df['COUNTRY'][mask] = 'other'
        df['Total'] = df.groupby(['CONTINENT',
                                  'COUNTRY',
                                  'YEAR',
                                  'COMMODITY'])['Agri_Values'].transform('sum')
        # Group and sum all the 'other' countries values in each continent.
        new_df = df.drop_duplicates(subset=['CONTINENT',
                                            'COUNTRY',
                                            'YEAR',
                                            'COMMODITY'])
        new_df.drop(['Agri_Values'], axis=1, inplace=True)
        new_df.rename(columns={'Total': 'Agri_Values'}, inplace=True)
        new_df['Total'] = new_df.groupby(['CONTINENT',
                                          'COMMODITY',
                                          'YEAR'])['Agri_Values'].transform('sum')

        # Group and sum each continent values by year.
        sum_df = new_df.drop_duplicates(subset=['CONTINENT',
                                                'COMMODITY',
                                                'YEAR'])
        sum_df.drop(['Agri_Values', 'COUNTRY'], axis=1, inplace=True)
        sum_df.rename(columns={'Total': 'Agri_Values'}, inplace=True)

        filtered_dfs[var_name] = sum_df
        return filtered_dfs


def get_dummies(filtered_dfs, columns):
    dummy_df = {}
    for df in filtered_dfs:
        CONTINENT_dummy_df = pd.get_dummies(filtered_dfs[df].CONTINENT, drop_first=True)
        CONTINENT_dummy_df.reset_index(inplace=True, drop=True)
        dummy_df[f'{df}_dummy'] = CONTINENT_dummy_df
        print(f'{df}_dummy')

    for df in dummy_df:
        dummy_df[df].drop_duplicates(ignore_index=True, inplace=True)

    bin_continents = {}
    for num, dum_continent in enumerate(columns):
        bin_continents[dum_continent] = list(dummy_df['QP_df_dummy'].iloc[num])
        #  result = {'africa': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #           'central asia': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #           'eastern asia': [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        #           'europe': [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        #           'north america': [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        #           'north asia': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        #           'oceania': [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        #           'south america': [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        #           'south asia': [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        #           'south-eastern asia': [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        #           'western asia': [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]}

    return dummy_df, bin_continents


def concat_all(filtered_dfs, dummy_dfs, commodity):
    merged_dfs = {}
    for df, dummy in zip(filtered_dfs, dummy_dfs):
        merged_df = pd.concat([filtered_dfs[df].reset_index(drop=True),
                               dummy.reset_index(drop=True)], axis=1)
        merged_df.drop(['CONTINENT'], axis=1, inplace=True)
        commodity_df = merged_df[merged_df.COMMODITY == commodity]
        commodity_df.reset_index(inplace=True)
        commodity_df = commodity_df.drop(['index', 'COMMODITY'], axis=1)
        merged_dfs[f'{df}_merged'] = commodity_df

    return merged_dfs


def import_binary(continents_list):
    c_list = continents_list

    def sample(continent, year):
        continents_binary = c_list[continent]
        valid_sample = [year] + continents_binary
        return valid_sample

    return sample


def LinearRegModule(df, commodity='WT', continent='africa'):
    '''
    QP = Production
    QP__MA = Ethanol production from maize
    QP__SCA = Ethanol production from sugar cane
    QP__VL = Biodiesel production from vegetable oil
    IM = Imports
    QC = Consumption
    ST = Ending stocks ??
    EX = Exports
    FE = Feed
    FO = Food
    BF = Biofuel use
    OU = Other use

    QC = FO + FE + BF + OU
    QP = QC + EX
    '''

    # Production BY Continent.
    QP_df = df[df.VARIABLE == 'QP']
    QP_df.drop(['VARIABLE'], axis=1, inplace=True)

    # Imports BY Continent.
    IM_df = df[df.VARIABLE == 'IM']
    IM_df.drop(['VARIABLE'], axis=1, inplace=True)

    # Consumption BY Continent.
    QC_df = df[df.VARIABLE == 'QC']
    QC_df.drop(['VARIABLE'], axis=1, inplace=True)

    # Feed BY Continent.
    FE_df = df[df.VARIABLE == 'FE']
    FE_df.drop(['VARIABLE'], axis=1, inplace=True)

    # Food BY Continent.
    FO_df = df[df.VARIABLE == 'FO']
    FO_df.drop(['VARIABLE'], axis=1, inplace=True)

    # Biofuel use BY Continent.
    BF_df = df[df.VARIABLE == 'BF']
    BF_df.drop(['VARIABLE'], axis=1, inplace=True)

    filtered_dfs = get_filtered_dfs([QP_df, IM_df, QC_df, FE_df, FO_df, BF_df])
    print(filtered_dfs.keys())

    columns = list(df.CONTINENT.unique())
    dummy_df, bin_continents = get_dummies(filtered_dfs=filtered_dfs,
                                           columns=columns)
    print(dummy_df.keys())

    merged_dfs = concat_all(filtered_dfs, dummy_df, commodity)
    print(merged_dfs.keys())

    # Start predictions:

    years = list(df.YEAR.unique())
    continents = list(df.CONTINENT.unique())
    sample = import_binary(bin_continents)
    predicts_dfs = {}

    for df in merged_dfs:
        pred_df = merged_dfs[df]
        X = merged_dfs[df].drop(['Agri_Values'], axis=1)
        y = merged_dfs[df]['Agri_Values']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.38, random_state=42)
        model = LinearRegression().fit(X_train, y_train)
        predictions = [{'country': continent,
                        'year': year,
                        'prediction': float(f'{float(model.predict([sample(continent, year)])):.2f}'),
                        'real values': list(pred_df[(pred_df.CONTINENT == continent) &
                                                    (pred_df.YEAR == year) &
                                                    (pred_df.COMMODITY == commodity)].Agri_Values)[0]}
                       for continent in continents for year in years]
        predicts_dfs[f'{df}_pred'] = pd.DataFrame(predictions)
        predicts_dfs[f'{df}_pred']['residual'] = predicts_dfs[f'{df}_pred']['real values'] - predicts_dfs[f'{df}_pred'][
            'prediction']
        print(model.score(X, y))

    return predicts_dfs
