import sqlite3 as sq3
import sys
import os
import time
import streamlit as st
import pandas as pd

cwd = os.getcwd()
sys.path.append(f'{cwd}\DataFrames')
sys.path.append(f'{cwd}\DataFrames\CreateTools')

from CreateLogger import Log
from OECD_API import OecdAPI
from Clean_DataFrames import adjusted_DataFrames as adjust_df

files = os.listdir(cwd)
dbLogger = Log('Database_log')


# ---------------------Get DataFrames---------------------------#
def Get_init_data2sql(db_list: list, progress):
    time.sleep(0.1)
    progress.progress(20)
    st.text('Trying to open Oecd API')
    full_datasets, sector_datasets = OecdAPI(db_list=db_list, progress=progress)

    datasets_to_use = adjust_df(full_datasets, progress)
    # ---------------------connection & cursor-----------------------------#
    dbLogger.debug('Starting to create database..')
    st.write(datasets_to_use)

    for dataset_to_sql in datasets_to_use:
        # ---------------------GBARD table-------------------#
        if dataset_to_sql == 'GBARD_final':
            connection = sq3.connect('DB_initialize\OECD_db_GBARD_init.db')
            dbLogger.debug('Getting DataFrames GBARD to DB')
            datasets_to_use[dataset_to_sql].to_sql('OECD_db_GBARD',
                                                   con=connection)
        # ---------------------Agricultural table------------#
        if dataset_to_sql == 'agricultural_final':
            connection = sq3.connect('DB_initialize\OECD_db_Agri_init.db')
            dbLogger.debug('Getting DataFrames Agricultural')
            datasets_to_use[dataset_to_sql].to_sql('OECD_db_Agri',
                                                   con=connection)
        else:
            pass

    for dataset_to_sql in sector_datasets:
        # ---------------------Agricultural table------------#
        if dataset_to_sql == 'Agri_country':
            connection = sq3.connect('DB_initialize\Agri_country.db')
            dbLogger.debug('Getting DataFrames Agri_country')
            sector_datasets[dataset_to_sql].to_sql('Agri_country',
                                                   con=connection)
        # ---------------------Agricultural table------------#
        if dataset_to_sql == 'commodity':
            connection = sq3.connect('DB_initialize\commodity.db')
            dbLogger.debug('Getting DataFrames commodity')
            sector_datasets[dataset_to_sql].to_sql('commodity',
                                                   con=connection)
        # ---------------------Agricultural table------------#
        if dataset_to_sql == 'Agri_variable':
            connection = sq3.connect('DB_initialize\Agri_variable.db')
            dbLogger.debug('Getting DataFrames Agri_variable')
            sector_datasets[dataset_to_sql].to_sql('Agri_variable',
                                                   con=connection)
        # ---------------------Agricultural table------------#
        if dataset_to_sql == 'GBARD_country':
            connection = sq3.connect('DB_initialize\GBARD_country.db')
            dbLogger.debug('Getting DataFrames GBARD_country')
            sector_datasets[dataset_to_sql].to_sql('GBARD_country',
                                                   con=connection)
        # ---------------------Agricultural table------------#
        if dataset_to_sql == 'seo':
            connection = sq3.connect('DB_initialize\seo.db')
            dbLogger.debug('Getting DataFrames seo')
            sector_datasets[dataset_to_sql].to_sql('seo',
                                                   con=connection)
        else:
            pass

    time.sleep(0.1)
    progress.progress(100)
    st.text('Process Completed')


def Read_init_sql(databases: list):
    dfs = []
    dbLogger.debug(f'databases to read: {databases}')

    for db in databases:
        if db == 'Agricultural':
            connection = sq3.connect('DB_initialize\OECD_db_Agri_init.db')
            Agri_data = pd.read_sql('SELECT * FROM OECD_db_Agri', con=connection)
            dfs.append(Agri_data)
            dbLogger.debug('Read_init_sql: append Agricultural df to dfs')

        elif db == 'GBARD':
            connection = sq3.connect('DB_initialize\OECD_db_GBARD_init.db')
            GBARD_data = pd.read_sql('SELECT * FROM OECD_db_GBARD', con=connection)
            dfs.append(GBARD_data)
            dbLogger.debug('Read_init_sql: append GBARD df to dfs')

        elif db == 'Agri_country':
            connection = sq3.connect('DB_initialize\Agri_country.db')
            Agri_country = pd.read_sql('SELECT * FROM Agri_country', con=connection)
            dfs.append(Agri_country)
            dbLogger.debug('Read_init_sql: append Agri_country df to dfs')

        elif db == 'commodity':
            connection = sq3.connect('DB_initialize\commodity.db')
            commodity = pd.read_sql('SELECT * FROM commodity', con=connection)
            dfs.append(commodity)
            dbLogger.debug('Read_init_sql: append commodity df to dfs')

        elif db == 'Agri_variable':
            connection = sq3.connect('DB_initialize\Agri_variable.db')
            Agri_variable = pd.read_sql('SELECT * FROM Agri_variable', con=connection)
            dfs.append(Agri_variable)
            dbLogger.debug('Read_init_sql: append Agri_variable df to dfs')

        elif db == 'GBARD_country':
            connection = sq3.connect('DB_initialize\GBARD_country.db')
            GBARD_country = pd.read_sql('SELECT * FROM GBARD_country', con=connection)
            dfs.append(GBARD_country)
            dbLogger.debug('Read_init_sql: append GBARD_country df to dfs')

        elif db == 'seo':
            connection = sq3.connect('DB_initialize\seo.db')
            seo = pd.read_sql('SELECT * FROM seo', con=connection)
            dfs.append(seo)
            dbLogger.debug('Read_init_sql: append seo df to dfs')

    return dfs

