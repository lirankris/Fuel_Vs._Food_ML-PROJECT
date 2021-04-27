import sqlite3 as sq3
import sys
import os

cwd = os.getcwd()
sys.path.append(f'{cwd}\DataFrames')
sys.path.append(f'{cwd}\DataFrames\CreateTools')

from CreateLogger import Log
from OECD_API import OecdAPI
from Clean_DataFrames import adjusted_DataFrames as adjust_df

files = os.listdir(cwd)
dbLogger = Log('Database_log', cwd)


# ---------------------Get DataFrames---------------------------#


def Get_init_data2sql(cwd=cwd):
    # dbLogger.debug('Getting DataFrames..')
    GBARD_df, Agri_df, Usd2conv_df, GBARD_country_df, \
    GBARD_seo_df, Agri_country_df, \
    Agri_commodity_df, Agri_variable_df = OecdAPI()

    G2usd_df_sort, Agri_df_sort, Usd2conv_df_sort = adjust_df(GBARD_df, Agri_df, Usd2conv_df)

    # ---------------------connection & cursor-----------------------------#
    dbLogger.debug('Starting to create database..')

    # ---------------------GBARD table-------------------#
    if 'OECD_Database_GBARD_init.db' not in os.listdir(cwd):
        connection = sq3.connect('OECD_Database_GBARD_init.db')
        dbLogger.debug('Getting DataFrames GBARD to DB')
        G2usd_df_sort.to_sql('OECD_Database_GBARD',
                        con=connection)

    # ---------------------Agricultural table------------#
    if 'OECD_Database_Agri_init.db' not in os.listdir(cwd):
        connection = sq3.connect('OECD_Database_Agri_init.db')
        dbLogger.debug('Getting DataFrames Agricultural')
        Agri_df_sort.to_sql('OECD_Database_Agri',
                       con=connection)

# def Get_new_data(Logger = dbLogger, cwd=cwd):





