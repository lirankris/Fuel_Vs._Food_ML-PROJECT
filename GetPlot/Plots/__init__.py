import matplotlib.pyplot as plt
import pandas as pd
from currency_converter import CurrencyConverter
from Main.DataFrames.GetTools.Get_Continents import DivideByContinents
from icecream import ic


def ConvertToUSD(currency, year):
    if currency == 'ARS':
        return 0.036  # ARS - Argentine Peso
    elif currency == 'TWN' or currency == 'TWD':
        return 0.12  # TWD - New Taiwan Dollar
    elif currency == 'CLP':
        return 0.0045  # CLP - Chilean Peso
    elif currency == 'CAD':
        return 0.38  # CLP - Candian Dollar
    elif currency == 'COP':
        return 0.00091  # COP - Colombian peso
    else:
        conv = CurrencyConverter(fallback_on_wrong_date=True)
        return conv.convert(1, 'USD', currency, date=date(year, 9, 1))


def Agri_plot(variable, continent, commodities, Agri_df, Fname_dfs):
    if variable.lower() in ["exports", "imports", "consumption", "production", "ending stocks"]:
        variable = variable.capitalize()
        Show_variable_val = variable
        dfname = 'balance'
        units = 'Thousands Tonnes'

    elif variable.lower() in ['feed', 'food', 'biofuel use', 'other use',
                              'maize2ethanol', 'sugar2ethanol', 'vegoil2biodiesel']:
        variable = variable.capitalize()
        Show_variable_val = variable
        dfname = 'uses'
        units = 'Thousands Tonnes'

    elif variable.lower() == 'human consumption':
        variable = 'Human consumption per capita'
        Show_variable_val = 'Human Consumption'
        dfname = 'ratio'
        units = 'Kilograms per capita'

    selected_df = Agri_df

    COUNTRY_df2 = Fname_dfs[0]
    VARIABLE_df2 = Fname_dfs[1]
    COMMODITY_df2 = Fname_dfs[2]
    df = selected_df[selected_df.VARIABLE == \
                     list(VARIABLE_df2[1][VARIABLE_df2[0] == variable])[0]]

    commodities_sort = [list(COMMODITY_df2[1][COMMODITY_df2[0] == commodity])[0] for commodity in commodities]
    Continents = DivideByContinents(COUNTRY_df2)
    countries = []
    countries_Fullname = []

    for c in Continents[continent.lower()]:
        countries.append(list(COUNTRY_df2[1][COUNTRY_df2[0] == c])[0])
        countries_Fullname.append(c)

    yearList = list(df.YEAR.unique())

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(7, 7))
    fig.suptitle(f'OECD Agricultural Outlook - {dfname}', fontsize=50, va='center', ha='center',
                 x=1.5, y=2.7)

    setup = [
        [
            i.set_xlabel('Years', fontsize=15.0), \
            i.set_ylabel(f'Values [{units}] ', fontsize=15.0), \
            i.grid(color='grey', linestyle='--', linewidth=0.2)
        ]
        for i in [ax1, ax2, ax3, ax4]
    ]

    setup
    plt.subplots_adjust(left=0.074,
                        right=0.933,
                        wspace=0.329,
                        hspace=0.312,
                        top=0.921,
                        bottom=0.171)

    for ax, commodity in zip([ax1, ax2, ax3, ax4], commodities_sort):
        for country in countries:  # Single Country Dataframe.
            country_df = df[(df.COMMODITY == commodity) & (df.COUNTRY == country)]
            if commodity in ['ET', 'BD']:
                Y = pd.Series([(val / 1143.25) for val in country_df.Agri_Values])
                ax.set_ylabel(f'Values [Millions Litres]', fontsize=20.0)
            else:
                Y = country_df.Agri_Values

            fig.legend(countries_Fullname, loc=8, ncol=6,
                       fontsize=10, fancybox=True, framealpha=0.5, bbox_to_anchor=(0.5, 0.03),
                       title='Countries', title_fontsize='medium')
            ax.plot(yearList, Y)

            commodity_Name = list(COMMODITY_df2[0][COMMODITY_df2[1] == commodity])[0]
            ax.set_title(f'{Show_variable_val} - {commodity_Name} - {continent.upper()}', \
                         fontsize=25.0, c='#a1cae2', fontweight='bold')

        for xtick, ytick in zip(ax.xaxis.get_majorticklabels(), ax.yaxis.get_majorticklabels()):
            xtick.set_fontsize(14)
            ytick.set_fontsize(14)

    plt.show()


def GBARD_plot(in_df, seo, COUNTRY_df, continent):
    if seo.lower() == 'agricultural':
        Figname = 'Agricultural R&D'
        df = in_df[in_df.SEO == 'NABS08']  # Government investment Agricultural R&D.
    elif seo.lower() == 'industry':
        Figname = 'industry and production'
        df = in_df[in_df.SEO == 'NABS06']  # Agricultural in industry and production.
    elif seo.lower() == 'university':
        Figname = 'Agricultural university funds'
        df = in_df[in_df.SEO == 'NABS124']  # R&D related to Agricultural university funds
    else:
        Figname = 'Agricultural other funds'
        df = in_df[in_df.SEO == 'NABS134']  # R&D related to Agricultural other funds

    units = 'USD millones'

    Continents = DivideByContinents(COUNTRY_df)
    del Continents['africa']

    yearList = list(df.YEAR.unique())

    # get a list of countries in the given continent.
    countries = [list(COUNTRY_df[1][COUNTRY_df[0] == c])[0] for c in Continents[continent.lower()]]

    # get the name of thos countries.
    countries_Fullname = [co for co in Continents[continent.lower()]]

    fig = plt.figure(figsize=(12, 6), frameon=True)
    ax = fig.add_subplot(111)
    plt.title(f'Government budget allocations for R&D - {Figname}', fontsize=14)

    # ---------------------------------loop through countries------------------------------------ #
    for country in countries:
        Y = df.GBARD_Values[df.COUNTRY == country]  # Single Country Dataframe.
        try:
            ax.plot(yearList, Y, linewidth=2)
        except ValueError:
            print(f'{country} have only {len(Y)} values in Y..')
            continue

        ax.set_xlabel('Years', fontsize=12)
        ax.set_ylabel(f'Values[{units}]', fontsize=12)
        ax.grid(color='grey', linestyle='--', linewidth=0.2)
    if len(countries) > 6:
        fig.legend(countries_Fullname, loc=10, ncol=10,
                   fontsize=8, fancybox=True, framealpha=0.5, bbox_to_anchor=(0.5, 0.96),
                   title='Countries', title_fontsize='medium')
    else:
        fig.legend(countries_Fullname, loc=10, ncol=2,
                   fontsize=10, fancybox=True, framealpha=0.5, bbox_to_anchor=(0.5, 0.5),
                   title='Countries', title_fontsize='large')

    plt.show()
