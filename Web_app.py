import sqlite3 as sq3
import os
import sys
import streamlit as st
import seaborn as sns
import jupyterlab as jupyter
import bokeh
import plotly.express as py
import pandas as pd
# import Sql_Database as sqldb
import time
# ---------------------Get initial data-------------------#
# def load_data():
#     return sqldb.Get_init_data2sql()

# load_data()
# -----------------------------------Main---------------------------------------------#
# Dashboard Title
st.title("OECD Dashboard")

# -----------------------------------sidebar------------------------------------------#
# sidebar Title
st.sidebar.title("DataFrames")
st.sidebar.subheader('Data sets')
# checkboxes
check_box_1 = st.sidebar.checkbox(label="Display Agricultural result")
check_box_2 = st.sidebar.checkbox(label="Display GBARD result")
check_box_3 = st.sidebar.checkbox(label="Load initial Data")

# feature selection


if check_box_1:
    check_box_2 = False
    st.markdown("Only Agricultural results")
    # ---------------------Agricultural columns------------#
    connection = sq3.connect('OECD_Database_Agri_init.db')
    Agri_data = pd.read_sql('SELECT * FROM OECD_Database_Agri',
                            con=connection)

    country_col = list(Agri_data.LOCATION.unique())
    comm_col = list(Agri_data.COMMODITY.unique())
    var_col = list(Agri_data.VARIABLE.unique())
    time.sleep(2)
    st.write(Agri_data.head(20))
    feature_selection = st.sidebar.selectbox(label="feature to plot",
                                             options=comm_col)
    country_selection = st.sidebar.selectbox(label="Country",
                                             options=country_col)
    variable_selection = st.sidebar.selectbox(label="Variable",
                                              options=var_col)

    sub_check_box_1 = st.checkbox(label="Display Agricultural plot")
    if sub_check_box_1:
        if not feature_selection:
            st.write('Select feature?')
        else:
            time.sleep(2)
            st.write('you have slected1', country_selection)
            st.write('you have slected2', feature_selection)
            data2plot = Agri_data[
                (Agri_data.LOCATION == country_selection) &
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
    df_features = data2plot[feature_selection][:31]
    plotly_figure = py.line(x=df_features,
                            y=year_col,
                            data_frame=df_features,
                            title=str(country_dropdown))
    st.plotly_chart(plotly_figure)

# if check_box_3:
#     load_data()
