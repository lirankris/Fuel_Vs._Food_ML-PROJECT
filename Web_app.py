import sqlite3 as sq3
import os
import sys
import streamlit as st
# import seaborn as sns
# import jupyterlab as jupyter
# import bokeh
import plotly.express as py
import pandas as pd
import Sql_Database as sqldb
import time

cwd = os.getcwd()
sys.path.append(f'{cwd}\Pic')

st.set_page_config(page_title='Fuel Vs.Food Dashboard'
                   , layout='wide',
                   initial_sidebar_state='collapsed')


@st.cache
def Create_check_box(label='New check box'):
    return st.sidebar.checkbox(label=label)


def Create_sidebar(options: list = [],
                   label: str = 'New check sidebar', sidebar_type: str = ''):
    if sidebar_type == 'select_box':
        return st.sidebar.selectbox(label=label, options=options)
    elif sidebar_type == 'multiselect':
        return st.sidebar.multiselect(label=label, options=options)
    elif sidebar_type == 'progress':
        return st.progress(0)


def load_init_data(db_list: list, progress):
    return sqldb.Get_init_data2sql(db_list, progress)


# ---------------------------------------Main---------------------------------------------#
def main():
    # Dashboard sub Title.
    first_Hello = st.title('Hello')
    user_input_placeholder = st.empty()
    user_input = user_input_placeholder.text_input(label="What is your name:")
    if user_input:
        first_Hello.empty()
        user_input_placeholder.empty()
        first_Hello = st.title(f'Hello {user_input}')
        time.sleep(3)
        first_Hello.empty()
        # Dashboard Title.
        st.title("Fuel Vs.Food Dashboard")
        # -----------------------------------sidebar------------------------------------------#
        # sidebar Title.
        st.sidebar.title("Control panel")
        st.sidebar.title(f"User: {user_input}")
        # sub sidebar Title.
        st.sidebar.subheader('Data sets')
        # ----------------------------------Get initial data----------------------------------#
        Get_db_list = os.listdir(rf'{cwd}\DB_initialize')
        missing_db = []
        for db in ['OECD_db_GBARD_init.db',
                   'OECD_db_Agri_init.db']:
            if db not in Get_db_list:
                st.text(f"{db} - Dosen't exist!")
                missing_db.append(db)

        if missing_db:
            st.text('Creating new database Please wait..')
            prog_bar = Create_sidebar(sidebar_type='progress')
            time.sleep(0.1)
            load_init_data(db_list=missing_db,
                           progress=prog_bar)
        else:
            st.text("All database are all present and accounted for")
        # ----------------------------------Get initial data----------------------------------#
        # checkboxes
        check_box_1 = Create_check_box(label='Display Agricultural result')
        check_box_2 = Create_check_box(label='Display GBARD result')

        # feature selection
        if check_box_1:
            st.markdown("Agricultural results:")
            # ---------------------Agricultural columns------------#
            connection = sq3.connect('OECD_Database_Agri_init.db')
            Agri_data = pd.read_sql('SELECT * FROM OECD_Database_Agri',
                                    con=connection)
            time.sleep(1)
            country_col = list(Agri_data.LOCATION.unique())
            comm_col = list(Agri_data.COMMODITY.unique())
            var_col = list(Agri_data.VARIABLE.unique())

            time.sleep(2)
            st.dataframe(Agri_data.style.highlight_max(axis=0))
            # st.write(Agri_data.head(100))

            country_selection = Create_sidebar(label="Country",
                                               options=country_col,
                                               sidebar_type='multiselect')
            feature_selection = Create_sidebar(label="feature to plot",
                                               options=comm_col,
                                               sidebar_type='select_box')
            variable_selection = Create_sidebar(label="Variable",
                                                options=var_col,
                                                sidebar_type='select_box')

            sub_button_Get_plot = st.button(label="Get Plot")
            sub_button_Export_csv = st.button(label="Export to CSV")

            if sub_button_Get_plot:
                if not feature_selection:
                    st.write('Select feature?')
                else:
                    time.sleep(2)
                    st.write('you have selected:', country_selection)
                    data2plot = Agri_data[
                        (Agri_data.LOCATION.isin(country_selection)) &
                        (Agri_data.COMMODITY == feature_selection) &
                        (Agri_data.VARIABLE == variable_selection)]

                    plotly_figure = py.line(x='Date',
                                            y='Value',
                                            data_frame=data2plot,
                                            title=str(country_selection))
                    st.plotly_chart(plotly_figure)

        if check_box_2:
            check_box_1 = False
            st.markdown("Only GBARD results")
            # ---------------------GBARD columns-------------------#
            connection = sq3.connect('OECD_Database_GBARD_init.db')
            GBARD_data = pd.read_sql('SELECT * FROM OECD_Database_GBARD',
                                     con=connection)

            country_col = list(GBARD_data.COUNTRY.unique())
            seo_col = list(GBARD_data.SEO.unique())
            year_col = list(GBARD_data.Date.unique())

            st.write(GBARD_data)
            feature_selection = st.sidebar.multiselect(label="feature to plot",
                                                       options=seo_col)
            country_dropdown = st.sidebar.selectbox(label="Country",
                                                    options=country_col)
            data2plot = GBARD_data[GBARD_data.COUNTRY == country_dropdown]
            df_features = data2plot[feature_selection]
            plotly_figure = py.line(x=df_features,
                                    y=year_col,
                                    data_frame=df_features,
                                    title=str(country_dropdown))
            st.plotly_chart(plotly_figure)


if __name__ == '__main__':
    main()
# if check_box_3:
#     load_data()
