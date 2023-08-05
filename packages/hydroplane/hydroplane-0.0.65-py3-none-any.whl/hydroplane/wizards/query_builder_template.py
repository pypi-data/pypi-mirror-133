import dash, json, requests, os
from dash import dcc 
from dash import html 
from dash.dependencies import Input, Output, State, MATCH, ALL 
 
from hydroplane.hydro import hydro
from hydroplane.components import wizard, cards, table

import hydroplane.data_sources.postgres as pg
from hydroplane.data_sources import druid 

from pydruid.client import *
from pydruid.utils.aggregators import * 
from pydruid.utils.postaggregator import * 


class HydroQueryWizard:
    def __init__(self):
        pass

    def query_builder_name_form(self): 
        data_source_list = []
        conn = pg.postgres_connection(host=os.environ['POSTGRES_HOST'], port=os.environ['POSTGRES_PORT'], database=os.environ['POSTGRES_DB'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'])
        data_sources = pg.postgres_get_data_sources(conn)
        for data_source in data_sources:
            data_source_list.append({'label': data_source[0], 'value': data_source[0]}) 
        return html.Div(id={'type': "input-query-name-wrapper", 'index': 1}, className="mb-3", children=[
            dcc.Input(
                id={'type': 'input-query-name', 'index': 1},
                className="form-control",
                type="text",
                placeholder="Query Name",
            ),
            html.Br(),
            dcc.Dropdown( 
                id={'type': "input-query-data-source", 'index': 1},
                placeholder="Select Data Source...",
                options=data_source_list,
                value=''
            )
        ])

    def query_builder_object_form(self):
        return html.Div(id={'type': "input-query-object-wrapper", 'index': 1}, className="mb-3", children=[ 
            dcc.Dropdown( 
                id={'type': "input-query-object", 'index': 1},
                placeholder="Select Query Object...",
                options=[], 
                value=''
            )
        ])

    def query_builder_dimensions_form(self):
        return html.Div(id={'type': "input-query-object-dimensions-wrapper", 'index': 1}, className="mb-3", children=[ 
            dcc.Dropdown( 
                id={'type': "input-query-object-dimensions", 'index': 1},
                placeholder="Select Query Dimensions...",
                options=[],
                multi=True,
                value=''
            )
        ])
    def query_preview_form(self):
        return html.Div(id={'type': "input-query-preview-wrapper", 'index': 1}, className="mb-3", children=[ 
            html.Div(id={'type': "query-preview", 'index': 1}, children=[]),
            
            html.Button(
                        'Save Query', 
                        id={'type': "query-save-btn", 'index': 1}, 
                        n_clicks=0,
                        disabled=True,
                        className="btn btn-success"
                    ),
            
        ])


hydro_query = HydroQueryWizard()

QUERY_BUILDER_TEMPLATE = {
    1: {
        "tab_label": "query_name_data_source",
        "tab_header": "Query Name & Data Source",
        "tab_details": "Name your Query & Select Data Source",
        "body_header": "Step 1 - Query Name & Data Source",
        "body_details": "Provide a Unique Name for your Query",
        "form": hydro_query.query_builder_name_form()
    }, 
    2: {
        "tab_label": "query_obj",
        "tab_header": "Query Object",
        "tab_details": "Select Your Query Object",
        "body_header": "Step 2 - Query Object",
        "body_details": "Select Your Query Object",
        "form": hydro_query.query_builder_object_form()
    }, 
    3: {
        "tab_label": "query_dimensions",
        "tab_header": "Query Dimensions",
        "tab_details": "Select Your Query Dimensions",
        "body_header": "Step 3 - Query Dimensions",
        "body_details": "Select Your Query Dimensions",
        "form": hydro_query.query_builder_dimensions_form()
    }, 
    4: {
        "tab_label": "query_preview",
        "tab_header": "Query Preview",
        "tab_details": "Preview Your Query",
        "body_header": "Step 4 - Query Preview",
        "body_details": "Preview Your Query",
        "form": hydro_query.query_preview_form()
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
    Output("wizard-step-body-state-query-name", 'value'),  
    Output({'type': 'input-query-name', 'index': ALL}, 'value'),
    Input("wizard-step-body-state-query-name", 'value'), 
    Input({'type': 'input-query-name', 'index': ALL}, 'value'), 
)
def query_wizard_name(state, name):    
    return form_helper(state, name)

@hydro.callback(
    Output("wizard-step-body-state-query-data-source-name", 'value'),  
    Output({'type': 'input-query-data-source', 'index': ALL}, 'value'),
    Input("wizard-step-body-state-query-data-source-name", 'value'), 
    Input({'type': 'input-query-data-source', 'index': ALL}, 'value'), 
)
def query_wizard_data_source_name(state, data_source):    
    return form_helper(state, data_source)

@hydro.callback(
    Output({'type': 'input-query-object', 'index': ALL}, 'options'),
    Input("wizard-step-body-state-query-data-source-name", 'value') 
)
def query_wizard_populate_data_source_objects(name):  
    conn = pg.postgres_connection(host=os.environ['POSTGRES_HOST'], port=os.environ['POSTGRES_PORT'], database=os.environ['POSTGRES_DB'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'])
    data_type = pg.postgres_get_data_source_type(conn, name) 
    option_list = [] 
    if data_type[0] == "druid":   
        conn = pg.postgres_connection(host=os.environ['POSTGRES_HOST'], port=os.environ['POSTGRES_PORT'], database=os.environ['POSTGRES_DB'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'])
        end_port = pg.postgres_get_data_source_endpoint_port(conn, name)
        endpoint = end_port[0]
        port = end_port[1] 
        if druid.druid_status(endpoint, port):
            data_source_tbls = druid.druid_data_sources(name) 
            for tbl in data_source_tbls:
                option_list.append({'label': tbl, 'value': tbl})
            return [option_list]
    return [[]]

@hydro.callback(
    Output("wizard-step-body-state-query-object", 'value'),  
    Output({'type': 'input-query-object', 'index': ALL}, 'value'),
    Input("wizard-step-body-state-query-object", 'value'), 
    Input({'type': 'input-query-object', 'index': ALL}, 'value'), 
)
def query_wizard_query_object(state, tbl):    
    return form_helper(state, tbl)

@hydro.callback(
    Output({'type': 'input-query-object-dimensions', 'index': ALL}, 'options'),
    Input("wizard-step-body-state-query-data-source-name", 'value'),
    Input("wizard-step-body-state-query-object", 'value')
)
def query_wizard_populate_dimensions(name, obj_name):  
    conn = pg.postgres_connection(host=os.environ['POSTGRES_HOST'], port=os.environ['POSTGRES_PORT'], database=os.environ['POSTGRES_DB'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'])
    data_type = pg.postgres_get_data_source_type(conn, name) 
    option_list = []
    if data_type[0] == "simple":    
        return [[]]
    if data_type[0] == "druid":   
        conn = pg.postgres_connection(host=os.environ['POSTGRES_HOST'], port=os.environ['POSTGRES_PORT'], database=os.environ['POSTGRES_DB'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'])
        end_port = pg.postgres_get_data_source_endpoint_port(conn, name)
        endpoint = end_port[0]
        port = end_port[1]  
        if druid.druid_status(endpoint, port):
            dimensions = druid.druid_data_source_dimensions(name, obj_name) 
            for dim in dimensions["dimensions"]:
                option_list.append({'label': dim, 'value': dim})
            return [option_list]
    return [[]]

@hydro.callback(
    Output("wizard-step-body-state-query-dimensions", 'value'),  
    Output({'type': 'input-query-object-dimensions', 'index': ALL}, 'value'),
    Input("wizard-step-body-state-query-dimensions", 'value'), 
    Input({'type': 'input-query-object-dimensions', 'index': ALL}, 'value'), 
)
def query_wizard_query_dimensions(state, dim):    
    return form_helper(state, dim)


@hydro.callback(
    Output({'type': "query-preview", 'index': ALL}, "children"),
    Output({'type': "query-save-btn", 'index': ALL}, 'disabled'), 
    Input("wizard-step-body-state-query-name", 'value'),
    Input("wizard-step-body-state-query-data-source-name", 'value'), 
    Input("wizard-step-body-state-query-object", 'value'), 
    Input("wizard-step-body-state-query-dimensions", 'value'), 
    Input({'type': "query-save-btn", 'index': ALL}, 'disabled'), 
    Input({'type': "query-preview", 'index': ALL}, "children"),
)
def query_wizard_preview_save_btn(query_name, data_source_name, object_name, dimensions, disabled, preview): 
    if query_name != "" and data_source_name != "" and object_name != "" and dimensions != []: 
        client = druid.druid_client(data_source_name)
        granularity = "day"
        intervals = '2021-02-02/p4w'
        aggregations = {'open': doublesum('Open'), 'close': doublesum('Close')}
        post_aggregations = {'o-c diff': (Field('open') / Field('close'))}
        limit_spec = {
                "type": "default",
                "limit": 5,
                "columns" : []
            }
        df = druid.druid_group_by_query(client, object_name, granularity, intervals, aggregations, post_aggregations, None, limit_spec) 
        column_names = {
            "o-c diff": "Open Close Differential",
            "close": "Close",
            "open": "Open",
            "timestamp": "Timestamp" 
        } 
        children =  table.table_builder(df, column_names) 
        return [children], [False]
    return preview, [True]


@hydro.callback( 
    Output({'type': "query-save-btn", 'index': ALL}, 'n_clicks'),
    Input("wizard-step-body-state-query-name", 'value'),
    Input("wizard-step-body-state-query-data-source-name", 'value'), 
    Input("wizard-step-body-state-query-object", 'value'), 
    Input("wizard-step-body-state-query-dimensions", 'value'),  
    Input({'type': "query-save-btn", 'index': ALL}, 'n_clicks'),
)
def query_wizard_preview_save_query(query_name, data_source_name, object_name, dimensions, clicks): 
    if clicks[0] > 0:
        conn = pg.postgres_connection(host=os.environ['POSTGRES_HOST'], port=os.environ['POSTGRES_PORT'], database=os.environ['POSTGRES_DB'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'])
        pg.postgres_data_source_query_insert(conn, query_name, data_source_name, object_name, dimensions)
    return [0]