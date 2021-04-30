import sqlite3 as sq3
import sys
import os
import time
import streamlit as st

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
    # # dbLogger.debug('Getting DataFrames..')
    # GBARD_df, Agri_df, Usd2conv_df, GBARD_country_df, \
    # GBARD_seo_df, Agri_country_df, \
    # Agri_commodity_df, Agri_variable_df = OecdAPI(db_list=db_list)
    time.sleep(0.1)
    progress.progress(20)
    st.text('Trying to open Oecd API')
    full_datasets, sector_datasets = OecdAPI(db_list=db_list, progress=progress)

    # G2usd_df_sort, Agri_df_sort, Usd2conv_df_sort = adjust_df(GBARD_df, Agri_df, Usd2conv_df)
    datasets_to_use = adjust_df(full_datasets, progress)
    # G2usd_df_sort, Agri_df_sort, Usd2conv_df_sort
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

    time.sleep(0.1)
    progress.progress(100)
    st.text('Process Completed')
