import os
import sys
import streamlit as st
import Sql_Database as sqldb
import time
from datetime import date
import plotly.graph_objects as go

# from Get_Continents import DivideByContinents

cwd = os.getcwd()
sys.path.append(f'{cwd}\Pic')
sys.path.append(f'{cwd}\DataFrames')

st.set_page_config(page_title='Fuel Vs.Food Dashboard',
                   layout='wide')


def get_current_date():
    return date.today().strftime("**%d/%m/%Y**")


@st.cache(suppress_st_warning=True)
def check_if_DB_exist():
    Get_db_list = os.listdir(rf'{cwd}\DB_initialize')
    missing_db = []
    for db in ['OECD_db_GBARD_init.db', 'OECD_db_Agri_init.db',
               'Agri_country.db', 'commodity.db',
               'Agri_variable.db', 'GBARD_country.db', 'seo.db']:
        if db not in Get_db_list:
            st.text(f"{db} - Dosen't exist!")
            missing_db.append(db)
    st.text(missing_db)

    if missing_db:
        st.text('Creating new database Please wait..')
        prog_bar = st.progress(0)
        time.sleep(0.1)
        load_init_data(db_list=missing_db,
                       progress=prog_bar)
    else:
        db_check_text = st.text("All database are all present and accounted for.")
        time.sleep(3)
        db_check_text.empty()


def load_init_data(db_list: list, progress):
    return sqldb.Get_init_data2sql(db_list, progress)


@st.cache(allow_output_mutation=True)
def get_database_connection(databases: list):
    return sqldb.Read_init_sql(databases)


@st.cache(allow_output_mutation=True)
def load_data_A():
    Agri_data = get_database_connection(databases=['Agricultural'])
    time.sleep(0.5)
    # ---------------------Agricultural columns------------#
    country_col = list(Agri_data[0].COUNTRY.unique())
    comm_col = list(Agri_data[0].COMMODITY.unique())
    var_col = list(Agri_data[0].VARIABLE.unique())
    # year_col = list(Agri_data.YEAR.unique())
    return country_col, comm_col, var_col, Agri_data[0]


@st.cache(allow_output_mutation=True)
def load_data_G():
    GBARD_data = get_database_connection(databases=['GBARD'])
    time.sleep(0.5)
    # ---------------------GBARD columns-------------------#
    country_col = list(GBARD_data[0].COUNTRY.unique())
    seo_col = list(GBARD_data[0].SEO.unique())
    # year_col = list(GBARD_data.YEAR.unique())
    return country_col, seo_col, GBARD_data[0]


@st.cache(allow_output_mutation=True)
def load_data_full_name_A():
    data = get_database_connection(databases=['Agri_country',
                                              'commodity',
                                              'Agri_variable'])
    time.sleep(0.5)
    # ---------------------Agri full name columns-------------------#
    A_country = data[0]
    A_commodity = data[1]
    A_variable = data[2]
    return A_country, A_commodity, A_variable


@st.cache(allow_output_mutation=True)
def load_data_full_name_G():
    data = get_database_connection(databases=['GBARD_country',
                                              'seo'])
    time.sleep(0.5)
    # ---------------------GBARD full name columns-------------------#
    G_country = data[0]
    G_seo = data[1]
    return G_country, G_seo


def plot_raw_data_A(sections, df):
    fig = go.Figure()
    for country in sections[0]:
        data2plot = df[
            (df.COUNTRY == country) &
            (df.COMMODITY == sections[1]) &
            (df.VARIABLE == sections[2])]

        fig.add_trace(go.Scatter(x=data2plot['YEAR'],
                                 y=data2plot['Agri_Values'],
                                 mode='lines',
                                 name=country))

    fig.plotly_update(title_text=str(sections[0]),
                      xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)


def plot_raw_data_G(sections, df):
    fig = go.Figure()
    for country in sections[0]:
        data2plot = df[(df.COUNTRY == country)]

        fig.add_trace(go.Scatter(x=data2plot['YEAR'],
                                 y=data2plot['GRARD_Values'],
                                 mode='lines',
                                 name=country))

    fig.plotly_update(title_text="GRARD_Values",
                      xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)


def country_selection(col):
    return st.sidebar.multiselect(label="Country", options=col)


def commodity_selection(col):
    return st.sidebar.selectbox(label='Commodity', options=col)


def variable_selection(col):
    return st.sidebar.selectbox(label='Variable', options=col)


def seo_selection(col):
    return st.sidebar.multiselect(label="Seo", options=col)


# ---------------------------------------Main---------------------------------------------#
def main():
    # Dashboard temp Title.
    time.sleep(3)
    # Dashboard Title.
    st.title("Fuel Vs.Food Dashboard")
    current_time = get_current_date()
    # -----------------------------------sidebar------------------------------------------#
    # sidebar Title.
    st.sidebar.markdown(f"Today's date is: {current_time}")
    st.sidebar.title("Control panel")
    # sub sidebar Title.
    st.sidebar.subheader('Data sets')
    # ----------------------------------Get initial data----------------------------------#
    check_if_DB_exist()

    # checkboxes
    check1 = st.sidebar.checkbox('Agricultural result')
    check2 = st.sidebar.checkbox('GBARD result')
    # feature selection
    if check1:
        check2 = False
        data_load_stat = st.text('Loading data...')

        country_col, comm_col, var_col, \
        Agri_data = load_data_A()
        A_country, A_commodity, A_variable = load_data_full_name_A()

        data_load_stat.text('Loading data done!')
        data_load_stat.empty()

        A_country_list = list(A_country.country_id)
        commodity_list = list(A_commodity.commodity_id)
        variable_list = list(A_variable.variable_id)

        full_name_country_col = [
            f'{country} - {A_country.country_full_name[int(A_country[A_country.country_id == country].index.values)]}'
            for country in country_col if country in A_country_list]
        full_name_comm_col = [
            f'{comm} - {A_commodity.commodity_full_name[int(A_commodity[A_commodity.commodity_id == comm].index.values)]}'
            for comm in comm_col if comm in commodity_list]
        full_name_var_col = [
            f'{var} - {A_variable.variable_full_name[int(A_variable[A_variable.variable_id == var].index.values)]}'
            for var in var_col if var in variable_list]

        try:
            df = Agri_data.drop(labels='index', axis=1, inplace=True)
        except KeyError:
            df = Agri_data

        placeholder = st.empty()
        placeholder.write(df.head(30))

        sub_button_Get_plot = st.button(label="Plot")
        # sub_button_Export_csv = st.button(label="Export to CSV")

        country = country_selection(col=full_name_country_col)
        commodity = commodity_selection(col=full_name_comm_col)
        variable = variable_selection(col=full_name_var_col)

        if sub_button_Get_plot:
            placeholder.empty()
            country = [con.split(' -')[0] for con in country]
            sections = [country,
                        commodity.split(' -')[0],
                        variable.split(' -')[0]]
            st.write(df[(df.COUNTRY.isin(sections[0])) &
                        (df.COMMODITY == sections[1]) &
                        (df.VARIABLE == sections[2])])
            plot_raw_data_A(sections, df)

    if check2:
        check1 = False
        # sub_button_Export_csv = st.button(label="Export to CSV")

        data_load_stat = st.text('Loading data...')

        country_col, seo_col, GBARD_data = load_data_G()
        G_country, G_seo = load_data_full_name_G

        data_load_stat.text('Loading data done!')
        data_load_stat.empty()

        G_country_list = list(G_country.country_id)
        seo_list = list(G_seo.seo_id)

        full_name_country_col = [
            f'{country} - {G_country.country_full_name[int(G_country[G_country.country_id == country].index.values)]}'
            for country in country_col if country in G_country_list]
        full_name_seo_col = [
            f'{seo} - {G_seo.seo_full_name[int(G_seo[G_seo.seo_id == seo].index.values)]}'
            for seo in seo_col if seo in seo_list]

        try:
            df = GBARD_data.drop(labels='index', axis=1, inplace=True)
        except KeyError:
            df = GBARD_data

        placeholder = st.empty()
        placeholder.write(df.head(30))

        sub_button_Get_plot = st.button(label="Plot")
        # sub_button_Export_csv = st.button(label="Export to CSV")

        country = country_selection(col=full_name_country_col)
        seo = seo_selection(col=full_name_seo_col)
        df = GBARD_data.drop('index', axis=1, inplace=True)

        if sub_button_Get_plot:
            placeholder.empty()
            country = [con.split(' -')[0] for con in country]
            sections = [country, seo.split(' -')[0]]
            st.write(df[(df.COUNTRY.isin(sections[0])) &
                        (df.SEO == sections[1])])
            plot_raw_data_G(sections, df)


if __name__ == '__main__':
    main()
