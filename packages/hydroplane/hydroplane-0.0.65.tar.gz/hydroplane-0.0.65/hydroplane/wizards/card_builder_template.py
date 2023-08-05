import dash, json, requests, os
from dash import dcc 
from dash import html 
from dash.dependencies import Input, Output, State, MATCH, ALL 
import plotly.express as px

from hydroplane.hydro import hydro
from hydroplane.components import wizard, cards, table

import hydroplane.data_sources.postgres as pg
from hydroplane.data_sources import druid 

from pydruid.client import * 
from pydruid.utils.aggregators import * 
from pydruid.utils.postaggregator import * 

from hydroplane.components import cards


class HydroCardWizard:
    def __init__(self):
        pass

    def card_builder_name_type_form(self): 
        data_source_list = [] 
        return html.Div(id={'type': "input-card-name-type-wrapper", 'index': 1}, className="mb-3", children=[
            dcc.Input(
                id={'type': 'input-card-name', 'index': 1},
                className="form-control",
                type="text",
                placeholder="Card Name...",
            ),
            html.Br(),
            dcc.Dropdown( 
                id={'type': "input-card-type", 'index': 1},
                placeholder="Select Card Type...",
                options=[
                    {"label": "Chart", "value": "chart"},
                    {"label": "Table", "value": "table"},
                    {"label": "Map", "value": "map"}
                ],
                value=''
            )
        ])
    def card_builder_query_form(self): 
        query_list = [] 
        conn = pg.postgres_connection(host=os.environ['POSTGRES_HOST'], port=os.environ['POSTGRES_PORT'], database=os.environ['POSTGRES_DB'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'])
        for row in pg.postgres_get_query_id_name(conn):
            query_list.append({"label": row[1], "value": str(row[0])})
        return html.Div(id={'type': "input-card-query-wrapper", 'index': 1}, className="mb-3", children=[ 
            dcc.Dropdown( 
                id={'type': "input-card-query", 'index': 1},
                placeholder="Select Query...",
                options=query_list,
                value=''
            )
        ])

    def card_builder_chart_type_form(self):  
        return html.Div(id={'type': "input-card-chart-type-wrapper", 'index': 1}, className="mb-3", children=[  
            dcc.Dropdown( 
                id={'type': "input-card-chart-type-selector", 'index': 1},
                placeholder="Select Chart Type...",
                options=[
                    {"label": "Line", "value": "scatter"},
                    {"label": "Histogram", "value": "histogram"},
                    {"label": "Pie", "value": "pie"}
                ],
                value=''
            ),
            html.Br(),
            dcc.Dropdown( 
                id={'type': "input-card-chart-type-dimensions-selector", 'index': 1},
                placeholder="Select Chart Dimensions...",
                options=[
                    {"label": "Line", "value": "scatter"},
                    {"label": "Histogram", "value": "histogram"},
                    {"label": "Pie", "value": "pie"}
                ],
                multi=True,
                value=''
            ),
            html.Br(),
            dcc.Dropdown( 
                id={'type': "input-card-tbl-type-dimensions-selector", 'index': 1},
                placeholder="Select Table Dimensions...",
                options=[
                    {"label": "Line", "value": "scatter"},
                    {"label": "Histogram", "value": "histogram"},
                    {"label": "Pie", "value": "pie"}
                ],
                multi=True,
                value=''
            ) 
        ])

    def card_builder_preview_form(self):
        return html.Div(children=[
            html.Div(id={'type': "input-card-preview", 'index': 1}, children=[
                cards.simple_card(1, "large", "tab_header", ""),
            ]),
            html.Button(
                'Save Card', 
                id={'type': "card-save-btn", 'index': 1}, 
                n_clicks=0,
                disabled=True,
                className="btn btn-success"
            ),
        ])


hydro_card = HydroCardWizard()


CARD_BUILDER_TEMPLATE = {
    1: {
        "tab_label": "card_name_type",
        "tab_header": "Card Name & Type",
        "tab_details": "Name your card & select your type",
        "body_header": "Step 1 - Card Name & Type",
        "body_details": "Provide a Unique Name for your Card and Select Your Type",
        "form": hydro_card.card_builder_name_type_form()
    },  
    2: {
        "tab_label": "card_query",
        "tab_header": "Card Query",
        "tab_details": "Provide Your Card a Query",
        "body_header": "Step 2 - Card Query",
        "body_details": "Provide Your Card a Query",
        "form": hydro_card.card_builder_query_form()
    },
    3: {
        "tab_label": "card_type_config",
        "tab_header": "Card Type Config",
        "tab_details": "Configure Your Card Type",
        "body_header": "Step 3 - Card Type Configure",
        "body_details": "Configure Your Card Type",
        "form": hydro_card.card_builder_chart_type_form()
    },
    4: {
        "tab_label": "card_preview",
        "tab_header": "Card Preview",
        "tab_details": "Preview Your Card",
        "body_header": "Step 4 - Card Preview",
        "body_details": "Preview Your Card",
        "form": hydro_card.card_builder_preview_form()
    } 
}

def form_helper(state, input):  
    if len(input) > 0 and input[0] is not None and len(input[0]) == 0:
        return state, [state]   
    if state != "" and len(input) > 0 and input[0] is not None: 
        return input[0], input 
    if len(input) > 0 and input[0] is not None:   
        return input[0], input    
    if state != '' and input == []: 
        return state, []
    if state != '' and input != []:  
        return state, [state]   
    return state, input


@hydro.callback(
    Output("wizard-step-body-state-card-name", 'value'),  
    Output({'type': 'input-card-name', 'index': ALL}, 'value'), 
    Input("wizard-step-body-state-card-name", 'value'), 
    Input({'type': 'input-card-name', 'index': ALL}, 'value'), 
)
def card_wizard_name(state, name):    
    return form_helper(state, name)

@hydro.callback( 
    Output({'type': 'input-card-preview', 'index': ALL}, 'children'),
    Input("wizard-step-body-state-card-name", 'value'),
    Input("wizard-step-body-state-card-type", 'value'), 
    Input("wizard-step-body-state-card-query", 'value'),  
    Input("wizard-step-body-state-chart-type-selector", 'value'), 
    Input("wizard-step-body-state-chart-type-dimensions-selector", 'value'), 
    Input("wizard-step-body-state-tbl-type-dimensions-selector", 'value'), 
)
def card_wizard_preview(name, card_type, query, chart_type, chart_dimensions, tbl_dimensions):
    body = ""
    if query != "":
        conn = pg.postgres_connection(host=os.environ['POSTGRES_HOST'], port=os.environ['POSTGRES_PORT'], database=os.environ['POSTGRES_DB'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'])
        query_details = pg.postgres_get_query_details(conn, query)
        print(query_details)
        conn = pg.postgres_connection(host=os.environ['POSTGRES_HOST'], port=os.environ['POSTGRES_PORT'], database=os.environ['POSTGRES_DB'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'])
        data_type = pg.postgres_get_data_source_type(conn, query_details[2]) 
        option_list = [] 
        print(data_type)
        print("XX", query_details[2])
        if data_type is not None and data_type[0] == "simple":    
            print("SIMPLE")
        if data_type is not None and data_type[0] == "druid":   
            conn = pg.postgres_connection(host=os.environ['POSTGRES_HOST'], port=os.environ['POSTGRES_PORT'], database=os.environ['POSTGRES_DB'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'])
            end_port = pg.postgres_get_data_source_endpoint_port(conn, query_details[2])
            print(end_port)
            endpoint = end_port[0]
            port = end_port[1] 
            client = druid.druid_client(query_details[2])
            granularity = "day"
            intervals = '2021-02-02/p4w'
            aggregations = {'open': doublesum('Open'), 'close': doublesum('Close')}
            post_aggregations = {'o-c diff': (Field('open') / Field('close'))}
            limit_spec = {
                    "type": "default",
                    "limit": 5,
                    "columns" : []
                }
            df = druid.druid_group_by_query(client, query_details[3], granularity, intervals, aggregations, post_aggregations, None, limit_spec) 
    x_name = name   
    if card_type == "table":  
        column_names = {
            "o-c diff": "Open Close Differential",
            "close": "Close",
            "open": "Open",
            "timestamp": "Timestamp" 
        } 
        body =  table.table_builder(df, column_names)  
    elif card_type == "chart":
        body = dcc.Graph(figure=px.line(df, x="timestamp", y="o-c diff"))
    if name == "":
        x_name = "Card Name" 
    z = html.Div(children=[
        query, card_type, chart_type, html.Div(children=chart_dimensions), html.Div(children=tbl_dimensions)
    ])
    return [cards.simple_card(1, "large", x_name, body)]

@hydro.callback(
    Output("wizard-step-body-state-card-type", 'value'),  
    Output({'type': 'input-card-type', 'index': ALL}, 'value'),
    Input("wizard-step-body-state-card-type", 'value'), 
    Input({'type': 'input-card-type', 'index': ALL}, 'value'), 
)
def card_wizard_type(state, card_type):    
    return form_helper(state, card_type)

@hydro.callback(
    Output("wizard-step-body-state-card-query", 'value'),  
    Output({'type': 'input-card-query', 'index': ALL}, 'value'),
    Input("wizard-step-body-state-card-query", 'value'), 
    Input({'type': 'input-card-query', 'index': ALL}, 'value'), 
)
def card_wizard_query(state, query):    
    return form_helper(state, query)

# @hydro.callback(
#     Output("wizard-step-body-state-card-type-selector", 'value'),  
#     Output({'type': 'input-card-type-selector', 'index': ALL}, 'value'),
#     Input("wizard-step-body-state-card-type-selector", 'value'), 
#     Input({'type': 'input-card-type-selector', 'index': ALL}, 'value'), 
# )
# def card_wizard_card_type(state, card_type):    
#     return form_helper(state, card_type)

@hydro.callback(
    Output("wizard-step-body-state-chart-type-selector", 'value'),  
    Output({'type': 'input-card-chart-type-selector', 'index': ALL}, 'value'),
    Input("wizard-step-body-state-chart-type-selector", 'value'), 
    Input({'type': 'input-card-chart-type-selector', 'index': ALL}, 'value'), 
)
def card_wizard_chart_type(state, chart_type):    
    return form_helper(state, chart_type)

@hydro.callback(
    Output("wizard-step-body-state-chart-type-dimensions-selector", 'value'),  
    Output({'type': 'input-card-chart-type-dimensions-selector', 'index': ALL}, 'value'),
    Input("wizard-step-body-state-chart-type-dimensions-selector", 'value'), 
    Input({'type': 'input-card-chart-type-dimensions-selector', 'index': ALL}, 'value'), 
)
def card_wizard_chart_dimensions(state, chart_dimensions):    
    return form_helper(state, chart_dimensions)


@hydro.callback(
    Output("wizard-step-body-state-tbl-type-dimensions-selector", 'value'),  
    Output({'type': 'input-card-tbl-type-dimensions-selector', 'index': ALL}, 'value'),
    Input("wizard-step-body-state-tbl-type-dimensions-selector", 'value'), 
    Input({'type': 'input-card-tbl-type-dimensions-selector', 'index': ALL}, 'value'), 
)
def card_wizard_table_dimensions(state, table_dimensions):    
    return form_helper(state, table_dimensions)

 


@hydro.callback(  
    Output({'type': 'input-card-chart-type-dimensions-selector', 'index': ALL}, 'options'),
    Output({'type': 'input-card-tbl-type-dimensions-selector', 'index': ALL}, 'options'),
    Input("wizard-step-body-state-card-query", 'value') 
)
def card_wizard_dimensions(query):   
    dimensions = [] 
    if query != "":
        conn = pg.postgres_connection(host=os.environ['POSTGRES_HOST'], port=os.environ['POSTGRES_PORT'], database=os.environ['POSTGRES_DB'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'])
        row = pg.postgres_get_query_dimensions(conn, query)
        for opt in row[0]:
            dimensions.append({"label": opt, "value": opt}) 
    return [dimensions], [dimensions]
 


@hydro.callback( 
    Output({'type': 'card-save-btn', 'index': ALL}, 'disabled'),
    Input("wizard-step-body-state-card-name", 'value'),
    Input("wizard-step-body-state-card-type", 'value'), 
    Input("wizard-step-body-state-card-query", 'value'),  
    Input("wizard-step-body-state-chart-type-selector", 'value'), 
    Input("wizard-step-body-state-chart-type-dimensions-selector", 'value'), 
    Input("wizard-step-body-state-tbl-type-dimensions-selector", 'value'), 
)
def card_save_btn(name, card_type, query, chart_type, chart_dimensions, tbl_dimensions):
    print(card_type, query, chart_type, chart_dimensions, tbl_dimensions)
    if name != "" and card_type != "" and query != "" and chart_type != "" and chart_dimensions != [] and tbl_dimensions != []:
        print("AAAAAA")
        return [False]
    else:
        return [True] 


@hydro.callback( 
    Output({'type': "card-save-btn", 'index': ALL}, 'n_clicks'),
    Input("wizard-step-body-state-card-name", 'value'),
    Input("wizard-step-body-state-card-type", 'value'), 
    Input("wizard-step-body-state-card-query", 'value'),  
    Input("wizard-step-body-state-chart-type-selector", 'value'), 
    Input("wizard-step-body-state-chart-type-dimensions-selector", 'value'), 
    Input("wizard-step-body-state-tbl-type-dimensions-selector", 'value'), 
    Input({'type': "card-save-btn", 'index': ALL}, 'n_clicks'),
)
def query_wizard_preview_save_query(name, card_type, query, chart_type, chart_dimensions, tbl_dimensions, clicks): 
    if clicks[0] > 0:
        conn = pg.postgres_connection(host=os.environ['POSTGRES_HOST'], port=os.environ['POSTGRES_PORT'], database=os.environ['POSTGRES_DB'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'])
        pg.postgres_cards_insert(conn,name, card_type, query, chart_type, chart_dimensions, tbl_dimensions)
    return [0]