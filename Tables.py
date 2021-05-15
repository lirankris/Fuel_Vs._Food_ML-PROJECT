import dash_table


def table_Agricultural(Agri_data):
    table_Agricultural_config = dash_table.DataTable(
        id='Agricultural_table',
        columns=[{'id': col, 'name': col} for col in Agri_data.columns],
        style_as_list_view=True,
        style_cell={'fontSize': 11,
                    'textAlign': 'left',
                    'padding': '5px',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'color': '#404040'},
        style_header={
            'fontSize': 10,
            'backgroundColor': '#F8F8F8',
            'fontWeight': 'bold',
            'textAlign': 'center'},
        style_table={'height': '400px',
                     'overflowY': 'auto',
                     'overflowX': 'auto'},
        fixed_rows={'headers': True},
        style_cell_conditional=[
            {
                'if': {
                    'column_id': col
                },
                'textAlign': 'center'
            } for col in Agri_data.columns],
        style_data_conditional=[
            # {
            #     'if': {
            #         'filter_query': '{COUNTRY} = ISR',
            #     },
            #     'backgroundColor': 'tomato',
            #     'color': 'white'
            # },
            {
                'if': {
                    'filter_query': '{Agri_Values} > 0.01',
                    'column_id': 'Agri_Values'
                },
                'color': '#404040',
                'fontWeight': 'bold'
            },
            {
                'if': {'column_id': 'index'},
                'width': '6px'},
            {'if': {'column_id': 'YEAR'},
             'width': '15px'},
            {'if': {'column_id': 'COUNTRY'},
             'width': '25px'},
            {'if': {'column_id': 'Agri_Values'},
             'width': '45px'},
            {'if': {'column_id': 'COMMODITY'},
             'width': '10px'},
            {'if': {'column_id': 'VARIABLE'},
             'width': '10px'}
        ])
    return table_Agricultural_config


def table_GBARD(GBARD_data):
    table_GBARD_config = dash_table.DataTable(
        id='GBARD_table',
        columns=[{'id': col, 'name': col} for col in GBARD_data.columns],
        style_as_list_view=True,
        style_cell={'fontSize': 11,
                    'textAlign': 'left',
                    'padding': '5px',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'color': '#404040'},
        style_header={
            'fontSize': 10,
            'backgroundColor': '#F8F8F8',
            'fontWeight': 'bold',
            'textAlign': 'center'},
        style_table={'height': '400px',
                     'overflowY': 'auto',
                     'overflowX': 'auto'},
        fixed_rows={'headers': True},
        style_cell_conditional=[
            {
                'if': {
                    'column_id': col
                },
                'textAlign': 'center'
            } for col in GBARD_data.columns
        ],
        style_data_conditional=[
            # {
            #     'if': {
            #         'filter_query': '{COUNTRY} = ISR',
            #     },
            #     'backgroundColor': 'tomato',
            #     'color': 'white'
            # },
            {
                'if': {
                    'filter_query': '{GBARD_Values} > 0.01',
                    'column_id': 'GBARD_Values'
                },
                'color': '#404040',
                'fontWeight': 'bold'
            },
            {
                'if':
                    {'column_id': 'index'},
                'width': '6px'},
            {'if':
                 {'column_id': 'YEAR'},
             'width': '15px'},
            {'if':
                 {'column_id': 'COUNTRY'},
             'width': '25px'},
            {'if':
                 {'column_id': 'GBARD_Values'},
             'width': '45px'},
            {'if':
                 {'column_id': 'SEO'},
             'width': '10px'}
        ])
    return table_GBARD_config
