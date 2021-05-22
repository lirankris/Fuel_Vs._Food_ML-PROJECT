import sys
import os
import pandas as pd
import time

cwd = os.getcwd()
sys.path.append(f'{cwd}\DataFrames')
sys.path.append(f'{cwd}\DataFrames\CreateTools')

from Convert2Currency import ConvertToUSD
from CreateLogger import Log


def sorted_dfs(dfs, CleanLogger):
    CleanLogger.info('Starting 2 sort dfs by values...')

    seo = ['NABS06', 'NABS08', 'NABS124', 'NABS134']

    variable = ['QP', 'EX', 'IM', 'QC', 'ST', 'FE', 'BF',
                'FO', 'OU', 'QP__MA', 'QP__SCA', 'QP__VL']

    commodity = ['WT', 'MA', 'BD', 'ET', 'VL', 'OCG', 'MOL', 'SBE', 'SCA']

    sort_dfs = {}

    for df in dfs:
        if df == 'slim_gbard':
            df1 = dfs['slim_gbard']
            sort_dfs['sort_gbard'] = df1[df1.SEO.isin(seo)].sort_values(
                by=['YEAR', 'SEO', 'COUNTRY'], ignore_index=True)
        if df == 'slim_agricultural' and df:
            df2 = dfs['slim_agricultural']
            sort_dfs['sort_agricultural'] = df2[
                (df2.COMMODITY.isin(commodity)) & (df2.VARIABLE.isin(variable))].sort_values(
                by=['YEAR', 'VARIABLE', 'COMMODITY', 'COUNTRY'], ignore_index=True)

    CleanLogger.debug('Finished sort values by SEO & COMMODITY & VARIABLE')

    # GBARD
    #      R&D related to Agricultural and veterinary sciences - financed by General university funds.
    #      R&D related to Agricultural and veterinary sciences - financed other then the General university funds.
    #      Total government investment in industry and production.
    #      Total government investment in Agricultural R&D.

    # AgriOut
    #     Commodity:
    #         Cereals_and_Oilseeds = Wheat, Maize, Other coarse grains, Vegetable oils.
    #         Sugar = Molasses, Sugar beet, Sugar cane.
    #         Biofuel = Ethanol, Biodiesel.

    # Variables:
    #         Balance = Production, Imports, Consumption, Exports, Ending stocks.
    #         Uses = Feed, Food, Biofuel use, Other use,
    #                 Ethanol production from maize,
    #                 Ethanol production from sugar cane,
    #                 Biodiesel production from vegetable oil.
    #         Ratio = Human consumption per capita.

    return sort_dfs


def Clean_DataFrames(full_datasets, CleanLogger):
    CleanLogger.info('Starting drop/rename...')
    dfs = {}
    for dataset in full_datasets:
        if dataset == 'gbard' and not full_datasets[dataset].empty:
            dfs['slim_gbard'] = ''
            df1 = full_datasets[dataset]
            # ----------------------------drop------------------------------- #
            for count, curr in enumerate(df1.MEASURE):
                if curr != 'MIO_NAC':
                    df1.drop(count, inplace=True)
            df1.drop(["MEASURE"], axis=1, inplace=True)
            df1.dropna(axis=0, inplace=True)
            CleanLogger.debug('drop rows that not contains MIO_NAC in column: MEASURE & \
                              Drop the MEASURE column from GBARD df')
            # ------------------------rename & replace----------------------------- #
            # Rename different columns in more suitable name.
            df1.rename(columns={"Value": "GBARD_Values", "Date": "YEAR"}, inplace=True)
            df1['YEAR'] = [pd.to_datetime(year).year for year in df1['YEAR']]

        if dataset == 'agricultural' and not full_datasets[dataset].empty:
            dfs['slim_agricultural'] = ''
            df2 = full_datasets[dataset]
            # ----------------------------drop------------------------------- #
            df2.dropna(axis=0, inplace=True)
            for c in ['OECD', 'EUN', 'NOA', 'EUR', 'OCD', 'AFR', 'LAC', 'WLD', 'BRICS', 'DVD', 'DVG']:
                df2.drop(df2[df2.LOCATION == c].index, axis=0, inplace=True)
            CleanLogger.debug("drop rows that not contains 'OECD', 'EUN', 'NOA', \
             'EUR', 'OCD', 'AFR', 'LAC', 'WLD', 'BRICS', 'DVD', 'DVG' in column: LOCATION")
            # ------------------------rename & replace----------------------------- #
            # Rename different columns in more suitable name.
            df2.rename(columns={"LOCATION": "COUNTRY", "Date": "YEAR",
                                "Value": "Agri_Values"}, inplace=True)
            print(df2)
            LT_index = df2.index[df2.COMMODITY.isin(['BD', 'ET'])].tolist()
            df2.loc[LT_index, 'Agri_Values'] = df2.Agri_Values / (1143.25)
            df2['YEAR'] = [pd.to_datetime(year).year for year in df2['YEAR']]

        if dataset == 'currncy' and not full_datasets[dataset].empty:
            dfs['slim_currncy'] = ''
            df3 = full_datasets[dataset]
            # ----------------------------drop------------------------------- #
            df3.dropna(axis=0, inplace=True)
            df3.reset_index(drop=True, inplace=True)
            for count, ind in enumerate(df3.TRANSACT):
                if ind != 'EXCE':
                    df3.drop(count, inplace=True)
            df3.drop(["TRANSACT", "MEASURE"], axis=1, inplace=True)
            CleanLogger.debug("drop rows that not contains 'EXCH' & columns: MEASURE, TRANSACT")
            # ------------------------rename & replace----------------------------- #
            # Rename different columns in more suitable name.
            df3.rename(columns={"LOCATION": "COUNTRY", "Date": "YEAR",
                                "Value": "Exchange_Values"}, inplace=True)
            df3['YEAR'] = [pd.to_datetime(year).year for year in df3['YEAR']]

    for dataset in dfs:
        if dataset == 'slim_gbard':
            dfs['slim_gbard'] = df1

        if dataset == 'slim_agricultural':
            dfs['slim_agricultural'] = df2

        if dataset == 'slim_currncy':
            dfs['slim_currncy'] = df3

    CleanLogger.info(f'number dfs: {len(dfs)}, name of dfs: {list(dfs.keys())}')

    return dfs


def df2USA_currency(df, ExcRate, Logger):
    Logger.info('Starting Converting currency 2 USD...')
    #  //CURRENCY:
    #   UD - Australian Dollar        ILS - New Israeli Sheqel
    #   EUR - Euro                    RON - Romanian Leu
    #   USD - US Dollar               RUB - Russian Ruble
    #   MXN - Mexican Peso            ARS - Argentine Peso
    #   SEK - Swedish Krona           KRW - Won
    #   NOK - Norwegian Krone         CZK - Czech Koruna
    #   CAD - Canadian Dollar         TWD - New Taiwan Dollar
    #   GBP - Pound Sterling          PLN - Zloty
    #   DKK - Danish Krone            HUF - Forint
    #   NZD - New Zealand Dollar      TRY - Turkish Lira
    #   JPY - Yen                     CLP - Chilean Peso
    #   CHF - Swiss Franc             No CURRENCY
    #   ISK - Iceland Krona

    yearList = list(df.YEAR.unique())
    Exc_countrylist = list(ExcRate.COUNTRY.unique())
    seoList = list(df.SEO.unique())
    count_country = []
    # ------------------------------------------------------------------------------------------ #
    new_set = []
    for seo in seoList:
        # NABS06, NABS08, NABS124, NABS134
        Logger.info(f'Chosen SEO: {seo}')
        for country in df.COUNTRY.unique():
            Logger.info(f'Chosen country: {country}')
            try:
                contry_df = df[(df.COUNTRY == country) & (df.SEO == seo)]  # Single Country & seo Dataframe.
                contry_years = list(contry_df.YEAR.unique())
                first_year = contry_years[0]
                last_year = contry_years[len(contry_years) - 1]
                Exc_contry_year_list = list(ExcRate.YEAR[ExcRate.COUNTRY == country].unique())
                Logger.info(f'Chosen country years limits: {first_year} - {last_year}')
            except IndexError as err:
                Logger.warning(f'country DataFrame: {country}, is Empty')
                Logger.warning(f'Getting an error: {err}')
                print(f'country DataFrame: {country}, is Empty')
                continue
            else:
                # ------------------------------------------------------------------------------------------ #
                for year in yearList:
                    # ----------------------------------df year empty row--------------------------------------- #
                    if last_year < year or year < first_year:
                        Logger.debug(f"In {year} there's an empty value for {country}")
                        new_set.append({'COUNTRY': country,
                                        'SEO': seo,
                                        'YEAR': year,
                                        'GBARD_Values': 0})

                    # ---------------------------------country in Exc country list----------------------------------- #
                    elif (last_year >= year or year >= first_year) and country in Exc_countrylist:
                        try:
                            if year not in Exc_contry_year_list:
                                Logger.warning("Can't convert this currency in Exc dataset")
                                Logger.debug("Trying to use ConvertToUSD function")
                                currValue = ConvertToUSD(country, year)
                            else:
                                currValue = list(ExcRate.Exchange_Values[(ExcRate.COUNTRY == country)
                                                                         & (ExcRate.YEAR == year)])[0]
                            value2replace = df[
                                (df.COUNTRY == country) & (df.YEAR == year) & (df.SEO == seo)].GBARD_Values
                            newValue = list(value2replace)[0] / currValue
                            new_set.append({'COUNTRY': country,
                                            'SEO': seo,
                                            'YEAR': year,
                                            'GBARD_Values': newValue})

                        except IndexError as err:
                            Logger.warning(f"This error occurred: {err}")
                            if country not in count_country:
                                count_country.append(country)
                                continue

                        except ValueError as err:
                            Logger.warning(f"This error occurred: {err}")
                            if country not in count_country:
                                count_country.append(country)
                                continue
                    # -------------------------------country not in Exc country list--------------------------------- #
                    else:
                        try:
                            if country == 'TWN':
                                currValue = ConvertToUSD('TWN', year)
                                value2replace = df[
                                    (df.COUNTRY == country) & (df.YEAR == year) & (df.SEO == seo)].GBARD_Values
                                newValue = list(value2replace)[0] / currValue
                                new_set.append({'COUNTRY': country,
                                                'SEO': seo,
                                                'YEAR': year,
                                                'GBARD_Values': newValue})

                        except Exception as exc:
                            print(exc)
                            print("\nNoop...that's the end of the rode guys...")
                            continue

    # ------------------------------Try currency valu0e implamantion----------------------------- #
    Logger.debug(f"There were problems with this country's: {count_country}")
    new_df = pd.DataFrame(new_set, columns=['COUNTRY', 'SEO', 'YEAR', 'GBARD_Values'])

    # new_df.reset_index(inplace=True, drop=True)
    new_df.sort_values(by=['COUNTRY', 'YEAR'], inplace=True)
    return new_df


def checkIfnull(df_dict, Logger):
    Logger.info('Starting Cleaning null values...')
    df_list = [df_dict[df] for df in df_dict]
    df_names = [df_dict for df in df_dict]
    for df, df_name in zip(df_list, df_names):
        col_names = list(df.keys())  # get the names of the columns Series.
        Cnull = df.isnull().sum()  # sum all the nan values per columns in df.
        Colvalue = Cnull.values  # get the amount of the nan values.
        for c in range(len(Colvalue)):  # loop through the list, example:[0 0 0 0 0 0 6 0]
            if Colvalue[c]:  # not 0 (False)
                print(f'df name: {df_name}\ncolumn name: {col_names[c]}\namount of null: {Colvalue[c]}')
                ValSeries = df[col_names[c]]  # specific null value place.
                if Colvalue[c] < len(
                        ValSeries) * 0.05:  # if the amount of nan values is less then 5% of the series(column).
                    try:
                        print(f'The mean value of {col_names[c]} is: {ValSeries.mean():.2f} \n')
                        ValSeries.fillna(ValSeries.mean(), inplace=True)  # fill all the nan values by the mean value.
                    except TypeError:
                        print(
                            f'Column {col_names[c]} dont contains integer values, filling it with: No {col_names[c]}\n')
                        ValSeries.fillna(f'No {col_names[c]}', inplace=True)
                        continue


# def adjusted_DataFrames(df1, df2, df3):
def adjusted_DataFrames(full_datasets):
    CleanLogger = Log('Clean_log')

    CleanLogger.info('Starting DataFrames Cleaning...')

    CleanLogger.debug('Going to Clean_DataFrames function')
    # full_datasets: [gbard, agricultural, currncy]
    time.sleep(0.1)
    # progress.progress(60)
    # st.text('Cleaning Datasets..')
    clean_full_datasets = Clean_DataFrames(full_datasets, CleanLogger)
    # clean_full_datasets: [slim_gbard, slim_agricultural, slim_currncy]

    CleanLogger.debug('Going to sorted_dfs function')
    sort_full_datasets = sorted_dfs(clean_full_datasets, CleanLogger)

    CleanLogger.debug('Going to checkIfnull function')
    checkIfnull(df_dict=sort_full_datasets,
                Logger=CleanLogger)

    finit_datasets = {}

    for ds in sort_full_datasets:
        if ds == 'sort_gbard':
            CleanLogger.debug('Going to df2USA_currency function')
            G2usd_df = df2USA_currency(df=sort_full_datasets['sort_gbard'],
                                       ExcRate=clean_full_datasets['slim_currncy'],
                                       Logger=CleanLogger)
            if not G2usd_df.empty:
                finit_datasets['GBARD_final'] = G2usd_df

    for fds in sort_full_datasets:
        if fds == 'sort_agricultural':
            finit_datasets['agricultural_final'] = sort_full_datasets['sort_agricultural']

    # progress.progress(80)
    # st.text('Datasets are all Done')

    return finit_datasets
