import os
import time
import pandas as pd
from datetime import date
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
import Sql_Database as sqldb
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from NavBar import navgationbar
from Tables import table_Agricultural, table_GBARD


# ** need to add debug **
# start$$ Get current date-------------------------------#
def get_current_date():
    return date.today().strftime("%d/%m/%Y")


# ------------------------------------Get current date $$end


# start$$ check if Data exist----------------------------------#
def load_init_data(db_list: list):
    return sqldb.Get_init_data2sql(db_list)


def get_database_connection(databases: list):
    return sqldb.Read_init_sql(databases)


def check_if_DB_exist():
    cwd = os.getcwd()
    Get_db_list = os.listdir(rf'{cwd}\DB_initialize')
    missing_db = []
    for db in ['OECD_db_GBARD_init.db', 'OECD_db_Agri_init.db',
               'Agri_country.db', 'commodity.db',
               'Agri_variable.db', 'GBARD_country.db', 'seo.db',
               'OECD_db_Agri_continents.db',
               'OECD_db_Agri_continents_1990.db',
               'OECD_db_Agri_continents_2020.db']:

        if db not in Get_db_list:
            print(f"{db} - Dosen't exist!")

            missing_db.append(db)

    if missing_db:
        print('Creating new database Please wait..')
        # ** need to add progress bar **
        time.sleep(0.1)
        load_init_data(db_list=missing_db)
    else:
        print("All database are all present and accounted for.")


# ------------------------------------check if Data exist $$end


# start$$ Load Agricultural Data-----------------------------------#
def load_data_A():
    Agri_data = get_database_connection(databases=['Agricultural'])
    # ---------------------Agricultural columns------------#
    country_col = list(Agri_data[0].COUNTRY.unique())
    comm_col = list(Agri_data[0].COMMODITY.unique())
    var_col = list(Agri_data[0].VARIABLE.unique())
    datasets = {'country_col': country_col,
                'comm_col': comm_col,
                'var_col': var_col,
                'Agri_data': Agri_data[0]}

    return datasets


# ------------------------------------Load Agricultural Data $$end


# start$$ Load GBARD Data-----------------------------------#
def load_data_G():
    GBARD_data = get_database_connection(databases=['GBARD'])
    # ---------------------GBARD columns-------------------#
    country_col = list(GBARD_data[0].COUNTRY.unique())
    seo_col = list(GBARD_data[0].SEO.unique())
    datasets = {'country_col': country_col,
                'seo_col': seo_col,
                'GBARD_data': GBARD_data[0]}

    return datasets


# ------------------------------------Load GBARD Data $$end


# start$$ Load data full name-----------------------------------#
def load_data_full_name():
    data = get_database_connection(databases=['Agri_country',
                                              'commodity',
                                              'Agri_variable',
                                              'GBARD_country',
                                              'seo'])
    # ---------------------full name columns-------------------#
    datasets = {'A_country': data[0],
                'commodity': data[1],
                'variable': data[2],
                'G_country': data[3],
                'seo': data[4]
                }

    return datasets


# ------------------------------------Load data full name $$end


# start$$ Load_continents_data-----------------------------------#
def load_continents_data():
    data = get_database_connection(databases=['continents',
                                              'continents_1990',
                                              'continents_2020'])
    # ---------------------full continents-------------------#
    datasets = {'continents': data[0],
                'continents_1990': data[1],
                'continents_2020': data[2]
                }

    return datasets


# -----------------------------------Load_continents_data $$end


# start$$ Get full name-----------------------------------#
def get_data_full_name_A(A_country, country_col, A_country_list,
                         A_commodity, comm_col, commodity_list,
                         A_variable, var_col, variable_list):
    full_name_country_col = [
        f'{country} - {A_country.country_full_name[int(A_country[A_country.country_id == country].index.values)]}'
        for country in country_col if country in A_country_list]
    full_name_comm_col = [
        f'{comm} - {A_commodity.commodity_full_name[int(A_commodity[A_commodity.commodity_id == comm].index.values)]}'
        for comm in comm_col if comm in commodity_list]
    full_name_var_col = [
        f'{var} - {A_variable.variable_full_name[int(A_variable[A_variable.variable_id == var].index.values)]}'
        for var in var_col if var in variable_list]

    return full_name_country_col, full_name_comm_col, full_name_var_col


def get_data_full_name_G(G_country, country_col, G_country_list,
                         G_seo, seo_col, seo_list):
    full_name_country_col = [
        f'{country} - {G_country.country_full_name[int(G_country[G_country.country_id == country].index.values)]}'
        for country in country_col if country in G_country_list]
    full_name_seo_col = [
        f'{seo} - {G_seo.seo_full_name[int(G_seo[G_seo.seo_id == seo].index.values)]}'
        for seo in seo_col if seo in seo_list]

    return full_name_country_col, full_name_seo_col


# ------------------------------------Get full name $$end


# start$$ Load Agricultural data------------------------------------------------------#

A_datasets = load_data_A()
Agri_data = A_datasets['Agri_data']
A_country_col = A_datasets['country_col']
var_col = A_datasets['var_col']
comm_col = A_datasets['comm_col']

G_datasets = load_data_G()
GBARD_data = G_datasets['GBARD_data']
G_country_col = G_datasets['country_col']
seo_col = G_datasets['seo_col']

full_name_datasets = load_data_full_name()
A_variable = full_name_datasets['variable']
A_country = full_name_datasets['A_country']
A_commodity = full_name_datasets['commodity']
G_country = full_name_datasets['G_country']
G_seo = full_name_datasets['seo']

continents_datasets = load_continents_data()
continents = continents_datasets['continents']
continents_1990 = continents_datasets['continents_1990']
continents_2020 = continents_datasets['continents_2020']

A_country_id_list = list(A_country.country_id)
commodity_id_list = list(A_commodity.commodity_id)
variable_id_list = list(A_variable.variable_id)
G_country_list = list(G_country.country_id)
seo_list = list(G_seo.seo_id)

full_name_country_col_A, \
full_name_comm_col, \
full_name_var_col = get_data_full_name_A(A_country, A_country_col, A_country_id_list,
                                         A_commodity, comm_col, commodity_id_list,
                                         A_variable, var_col, variable_id_list)
full_name_country_col_G, \
full_name_seo_col = get_data_full_name_G(G_country, G_country_col,
                                         G_country_list, G_seo, seo_col,
                                         seo_list)
# -----------------------------------------------------Load Agricultural data $$end


# start$$ Load style------------------------------#
external_stylesheets = [dbc.themes.CERULEAN]
# --------------------------------Load style $$end


# start$$ app & app layout----------------------------------------#
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Fuel Vs.Food Dashboard"
# -------------------------------------------app & app layout $$end


# start$$ Main dropdowns layout------------------------------------------#
country_dropdowns_items = dcc.Dropdown(id='country_dropdowns', multi=True,
                                       style={"width": "400px",
                                              'color': '#696969',
                                              'border': '#f9f9f9',
                                              'cursor': 'pointer',
                                              'margin': '4px',
                                              'font-size': '16px'},
                                       options=[{'label': (country.split('-'))[1], 'value': country}
                                                for country in full_name_country_col_A],
                                       placeholder='Country',
                                       className='dropdowns-menu-row')

commodity_dropdowns_items = dcc.Dropdown(id='commodity_dropdowns',
                                         style={"width": "150px",
                                                'color': '#696969',
                                                'border': '#f9f9f9',
                                                'cursor': 'pointer',
                                                'margin': '4px',
                                                'font-size': '16px'},
                                         options=[{'label': (commodity.split('-'))[1], 'value': commodity}
                                                  for commodity in full_name_comm_col],
                                         placeholder='Commodity',
                                         className='dropdowns-menu-row')

variable_dropdowns_items = dcc.Dropdown(id='variable_dropdowns',
                                        style={"width": "150px",
                                               'color': '#696969',
                                               'border': '#f9f9f9',
                                               'cursor': 'pointer',
                                               'margin': '4px',
                                               'font-size': '16px'},
                                        options=[{'label': (variable.split('-'))[1], 'value': variable}
                                                 for variable in full_name_var_col],
                                        placeholder='Variable',
                                        className='dropdowns-menu-row')

seo_dropdowns_items = dcc.Dropdown(id='seo_dropdowns',
                                   style={"width": "150px",
                                          'color': '#696969',
                                          'border': '#f9f9f9',
                                          'cursor': 'pointer',
                                          'margin': '4px',
                                          'font-size': '16px'},
                                   options=[{'label': (seo.split('-'))[1], 'value': seo}
                                            for seo in full_name_seo_col],
                                   placeholder='Seo',
                                   className='dropdowns-menu-row')
# -----------------------------------Main dropdowns layout end$$


# start$$ Header config--------------------------------------------------------#
Header = html.Div(
    html.Div(dbc.Container([
        html.H1('By Liran Krispin',
                className='header-logo'),
        dbc.Row(
            html.H2("Fuel Vs.Food Dashboard🌽",
                    style={"fontSize": "52px", "color": "white"},
                    className="header-title")
        ),
        dbc.Row(
            html.P("Create a smart annual predictions algorithm to predict the"
                   "diverting of crops "
                   "for biofuels production, Feed and food supply,"
                   "between 1990 and 2020",
                   className="header-description"))
    ],
        fluid=True,
    )),
    className='header')
# ---------------------------------------------------------Header config end$$


# start$$ dropdowns aggregation--------------------------------------#
dropdownsApp_Agricultural = html.Div(children=[
    html.Div(dbc.Row(
        [
            dbc.Col(variable_dropdowns_items,
                    width={"order": 1}),
            dbc.Col(commodity_dropdowns_items,
                    width={"order": 2}),
            dbc.Col(country_dropdowns_items,
                    width={"order": 3}),
            dbc.Col(dbc.Button('Submit',
                               id='submit-val',
                               n_clicks=0),
                    width={"order": 4}),
            html.Div(children=[],
                     id='output1',
                     hidden=True),
            html.Div(id='output2',
                     children=[],
                     hidden=True),
            html.Div(id='output3',
                     children=[],
                     hidden=True)
        ],
        justify='start',
        form=True,
        align='start')
    )
])

dropdownsApp_GBARD = html.Div(
    children=[
        html.Div(dbc.Row([
            dbc.Col(seo_dropdowns_items),
            dbc.Col(html.Div(children=[],
                             id='output4',
                             hidden=True))]))
    ]
)
# -------------------------------------------dropdowns aggregation $$end


# start$$ table & graph config config--------------------------------------#
table_Agricultural_dataApp = table_Agricultural(Agri_data)
table_GBARD_dataApp = table_GBARD(GBARD_data)

Agricultural_visualizeApp = html.Div(
    children=[dcc.Graph(
        id="Agri_Values-chart",
        config={"displayModeBar": False,
                'responsive': True,
                'plotGlPixelRatio': 30},
        figure={})])

GBARD_visualizeApp = html.Div(
    children=[dcc.Graph(
        id="GBARD_Values-chart",
        config={"displayModeBar": False,
                'responsive': True,
                'plotGlPixelRatio': 30},
        figure={})])

Indicator = html.Div(children=[
    dcc.Graph(id="Indicator",
              figure={})])

left_card_Agricultural_sum = dbc.Card(
    children=[
        dbc.CardHeader("Graph",
                       style={'fontSize': 14,
                              'color': '#808080'}),
        dbc.CardBody(Indicator)],
    body=True, outline=False,
    style={'border-radius': '6px'})

Agricultural_Main_card = dbc.Card(
    children=[
        dbc.CardHeader(["Agricultural",
                        dropdownsApp_Agricultural],
                       style={'fontSize': 20, 'color': '#808080'}),
        dbc.CardBody(
            dbc.Row(
                [
                    dbc.Col(table_Agricultural_dataApp, lg=5, width={"order": 1}),
                    dbc.Col(Agricultural_visualizeApp, width={"order": 2})
                ]
            )),
    ],
    style={"width": "1300px",
           "height": "600px",
           'border-radius': '10px'})

GBARD_Main_card = dbc.Card(
    children=[
        dbc.CardHeader(
            ["Government budget allocations for R&D",
             dropdownsApp_GBARD],
            style={'fontSize': 20, 'color': '#808080'}),
        dbc.CardBody([
            dbc.Row(
                [
                    dbc.Col(table_GBARD_dataApp, lg=5, width={"order": 1}),
                    dbc.Col(GBARD_visualizeApp, width={"order": 2})
                ]
            )
        ])
    ],
    style={"width": "1300px",
           "height": "600px",
           'border-radius': '10px'})

globe = dbc.Container(
    children=[
        dbc.Row(
            [
                dbc.Col(
                    html.Div(children=dcc.Graph(
                        id='globe',
                        figure={},
                        config={"displayModeBar": False,
                                'responsive': True}
                    )),
                    width={"order": 1, "size": 3, 'offset': -8}),
                dbc.Col(
                    dcc.Graph(
                        id='globe_bar',
                        figure={},
                        config={"displayModeBar": False,
                                'responsive': True}),
                    width={"order": 2, "size": 3, 'offset': 2}
                )
            ]
        )
    ]
)

top_card_1 = dbc.Card("1", body=True, outline=False,
                      style={'height': '100px', 'width': '300px'})
top_card_2 = dbc.Card("2", body=True, outline=False,
                      style={'height': '100px', 'width': '300px'})
top_card_3 = dbc.Card("3", body=True, outline=False,
                      style={'height': '100px', 'width': '300px'})

bottom_card_1 = dbc.Card("1", body=True, outline=False)
bottom_card_2 = dbc.Card("2", body=True, outline=False)
bottom_card_3 = dbc.Card("3", body=True, outline=False)
bottom_card_4 = dbc.Card("4", body=True, outline=False)
# ----------------------------------table & graph config $$end


# start$$ Agricultural Data Selection config--------------------------------------#
# hoverApp = html.Div(className='data-exct',
#                     children=[
#                         html.Div([
#                             dcc.Markdown("Zoom and Relayout Data"),
#                             html.Pre(id='relayout-data',
#                                      style={'color': '#404040'})])
#                     ])

# -------------------------------------Agricultural Data Selection config $$end


# start$$ side bar config--------------------------------------#
sidebar, content = navgationbar()
# ------------------------------------------side bar config$$end


# start$$ pages setup---------------------------------------#
Home_page = html.Div([
    html.Div(children=
    [
        dbc.Row([
            dbc.Col(top_card_1, width={"size": 3, "order": 1}),
            dbc.Col(top_card_2, width={"size": 3, "order": 2}),
            dbc.Col(top_card_3, width={"size": 3, "order": 3})]),
        dbc.Row(
            dbc.Col(globe))
    ]
    ),
    html.Div(id='check_bd', children=[])
])

analyze_page = html.Div(
    # id="page-content", style=CONTENT_STYLE,
    children=[
        html.Div(dbc.Container(className='container',
                               children=[
                                   html.Div(
                                       children=[
                                           dbc.Row([
                                               dbc.Col(
                                                   left_card_Agricultural_sum,
                                                   width={"size": 3,
                                                          "order": 1})
                                           ])
                                       ]),
                                   dbc.Row(Agricultural_Main_card,
                                           justify="end",
                                           align="stretch",
                                           no_gutters=True, form=True),
                                   dbc.Row(GBARD_Main_card,
                                           justify="end",
                                           align="stretch",
                                           no_gutters=True, form=True),
                                   dbc.Row([
                                       dbc.Col(bottom_card_1),
                                       dbc.Col(bottom_card_2),
                                       dbc.Col(bottom_card_3),
                                       dbc.Col(bottom_card_4)
                                   ])
                               ])
                 )])

# --------------------------------------pages setup $$end


# start$$ app layout---------------------------------------#
app.layout = html.Div([
    html.Div(Header),
    html.Div([dcc.Location(id="url"), sidebar, content])]
)


# --------------------------------------app layout $$end


# start$$ app callbacks---------------------------------------#
@app.callback(
    [Output("output1", "children"),
     Output("output2", "children"),
     Output("output3", "children"),
     Output("output4", "children")],
    Input("submit-val", "n_clicks"),
    [State('country_dropdowns', 'value'),
     State('commodity_dropdowns', 'value'),
     State('variable_dropdowns', 'value'),
     State('seo_dropdowns', 'value')])
def update_select(n_clicks, input1, input2, input3, input4):
    print(input4)
    if input1 is None:
        country_return = 'ISR'
    else:
        country_return = [(country.split(' -'))[0] for country in input1]

    if input2 is None:
        commodity_return = 'WT'
    else:
        commodity_return = (input2.split(' -'))[0]

    if input3 is None:
        variable_return = 'QP'
    else:
        variable_return = (input3.split(' -'))[0]

    if input4 is None:
        seo_return = 'NABS06'
    else:
        seo_return = (input4.split(' -'))[0]
    print(country_return, commodity_return, variable_return, seo_return)
    return country_return, commodity_return, variable_return, seo_return


@app.callback(
    Output("Agricultural_table", "data"),
    Input("output1", "children"),
    Input("output2", "children"),
    Input("output3", "children"),
)
def update_table(input1, input2, input3):
    print(input1)
    if isinstance(input1, str):
        return Agri_data[(Agri_data['COUNTRY'] == input1) &
                         (Agri_data.COMMODITY == input2) &
                         (Agri_data.VARIABLE == input3)].to_dict('records')
    else:
        return Agri_data[(Agri_data['COUNTRY'].isin(input1)) &
                         (Agri_data.COMMODITY == input2) &
                         (Agri_data.VARIABLE == input3)].to_dict('records')


@app.callback(
    Output("GBARD_table", "data"),
    Input("output1", "children"),
    Input("output4", "children"),
)
def update_table2(input1, input2):
    print(input1)
    if isinstance(input1, str):
        return GBARD_data[(GBARD_data['COUNTRY'] == input1) &
                          (GBARD_data.SEO == input2)].to_dict('records')
    else:
        return GBARD_data[(GBARD_data['COUNTRY'].isin(input1)) &
                          (GBARD_data.SEO == input2)].to_dict('records')


@app.callback(
    Output("Agri_Values-chart", "figure"),
    Input("Agricultural_table", "data"),
)
def update_graph(input1):
    df = pd.DataFrame.from_dict(input1)
    countries = df.COUNTRY.unique()
    print(countries)
    fig = go.Figure()
    for con in countries:
        fig.add_trace(go.Scatter(x=df[df.COUNTRY == con].YEAR,
                                 y=df[df.COUNTRY == con].Agri_Values,
                                 mode='lines',
                                 name=con))
        fig.update_layout(showlegend=True)
        fig.update_layout(legend={'title': 'countries'})
        fig.update_layout(paper_bgcolor='#F8F8F8',
                          plot_bgcolor='#F8F8F8',
                          clickmode='event+select')
        fig.update_layout(autosize=False,
                          width=630,
                          height=455)
        fig.update_traces(marker_size=20)
        fig.update_traces(text=con,
                          hovertemplate='<br><br>'
                                        ' year: %{x} <br>value: %{y}')
    return fig


@app.callback(
    [Output("GBARD_Values-chart", "figure"),
     Output("Indicator", "figure")],
    Input("GBARD_table", "data"),
)
def update_graph(input1):
    df = pd.DataFrame.from_dict(input1)
    countries = df.COUNTRY.unique()
    fig = go.Figure()
    for con in countries:
        fig.add_trace(go.Scatter(x=df[df.COUNTRY == con].YEAR,
                                 y=df[df.COUNTRY == con].GBARD_Values,
                                 mode='lines',
                                 name=con))
        fig.update_layout(showlegend=True)
        fig.update_layout(legend={'title': 'countries'})
        fig.update_layout(paper_bgcolor='#F8F8F8',
                          plot_bgcolor='#F8F8F8',
                          clickmode='event+select')
        fig.update_layout(autosize=False,
                          width=630,
                          height=455)
        fig.update_traces(marker_size=20)
        fig.update_traces(text=con,
                          hovertemplate='<br><br>'
                                        'year: %{x} <br>value: %{y}')

    fig2 = go.Figure(
        go.Indicator(
            mode="number+delta",
            value=400,
            number={'prefix': "%"},
            delta={'position': "top",
                   'reference': 300},
            domain={'row': 0, 'column': 0})
    )
    fig2.update_layout(paper_bgcolor="#F8F8F8",
                       plot_bgcolor='#F8F8F8')
    fig2.update_layout(autosize=False,
                       width=170,
                       height=60,
                       font={'size': 5000})

    return fig, fig2


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")])
def page_content(pathname):
    if pathname == "/":
        return Home_page
    elif pathname == "/page-1":
        return analyze_page
    elif pathname == "/page-2":
        return html.P("this is predictions page!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found",
                    className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


@app.callback(
    [Output("globe", "figure"),
     Output("globe_bar", "figure")],
    Input("url", "pathname"))
def globe_show(input):
    df = continents[(continents.VARIABLE == 'IM') & (continents.COMMODITY == 'WT')]
    results = df.groupby(by=['CONTINENT'], as_index=False).sum()
    selected_results = ['IM', 'WT']
    results.drop(['index', 'YEAR'], axis=1, inplace=True)

    fig = go.Figure(data=go.Scattergeo(mode="markers+lines"))
    fig.update_layout(margin={"r": 0,
                              "t": 0,
                              "l": 0,
                              "b": 0})
    fig.update_layout(showlegend=True,
                      autosize=False,
                      width=400,
                      height=400
                      )
    fig.update_layout(paper_bgcolor='#F8F8F8',
                      plot_bgcolor='#F8F8F8',
                      title='Oecd regions')
    fig.update_layout(
        geo=dict(
            showland=True,
            showcountries=True,
            showocean=True,
            countrywidth=0.9,
            landcolor='#eccca2',
            lakecolor='#4fdcff',
            oceancolor='#009dc4',
            projection=dict(
                type='orthographic')
        ),
    )
    fig.update_geos(fitbounds="locations")

    fig2 = go.Figure(go.Bar(x=results.CONTINENT,
                            y=results.Agri_Values,
                            name='Overall continents',
                            marker_color='lightsalmon'))
    fig2.update_layout(barmode='group',
                       xaxis_tickangle=-45,
                       title_text=f'Overall continents from {selected_results}')
    fig2.update_layout(paper_bgcolor='#FFFFFF',
                       plot_bgcolor='#FFFFFF',
                       clickmode='event+select',
                       autosize=False,
                       width=450,
                       height=400)
    fig2.update_traces(marker_line_color='#FFFFFF',
                       opacity=0.6)

    return fig, fig2


@app.callback(
    Output("check_bd", "children"),
    [Input("url", "pathname")])
def page_content(input):
    return check_if_DB_exist()


# @app.callback(
#     Output('relayout-data', 'children'),
#     Input('Agri_Values-chart', 'relayoutData'))
# def display_relayout_data(relayoutData):
#     results = json.dumps(relayoutData, indent=4)
#     # show_results = pd.read_json(results, orient='index')
#     # print(show_results)
#     show_results = json.loads(results)
#     yeras = f"{(show_results['xaxis.range[0]']):.0f} " \
#             f"{(show_results['xaxis.range[1]']):.0f} "
#
#     values = f"{show_results['yaxis.range[0]']:.2f}" \
#              f"{show_results['yaxis.range[1]']:.2f}"
#
#     return f'{yeras} \n {values}'
# --------------------------------------app callbacks $$end


if __name__ == '__main__':
    app.run_server(debug=False,
                   dev_tools_hot_reload=False)
