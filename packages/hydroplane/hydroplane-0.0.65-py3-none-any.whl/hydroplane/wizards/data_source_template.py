import dash, json, requests, os
from dash import dcc 
from dash import html 
from dash.dependencies import Input, Output, State, MATCH, ALL 

from hydroplane.hydro import hydro
from hydroplane.components import wizard

import hydroplane.data_sources.postgres as pg
from hydroplane.data_sources import druid 


class HydroDataSourceWizard:
    def __init__(self):
        pass

    # Data Source Form 
    def data_source_name_form(self):
        return html.Div(id={'type': "input-data-source-name-wrapper", 'index': 1}, className="mb-3", children=[
            dcc.Input(
                id={'type': 'input-data-source-name', 'index': 1},
                className="form-control",
                type="text",
                placeholder="Data Source Name",
            )
        ])

    def data_source_endpoint_form(self):
        return html.Div(className="row", children=[
            html.Div(className="mb-3 col-md-8", children=[
                dcc.Input(
                    id={'type': "input-data-source-endpoint", 'index': 1},
                    className="form-control",
                    type="text",
                    placeholder="Data Source Endpoint",
                ) 
            ]),
            html.Div(className="mb-3 col-md-4", children=[ 
                dcc.Input( 
                    id={'type': "input-data-source-port", 'index': 1},
                    className="form-control",
                    type="text",
                    placeholder="Data Source Port",
                )
            ])
        ])

    def data_source_type_form(self):
        return html.Div(className="mb-3", children=[ 
            dcc.Dropdown( 
                id={'type': "input-data-source-type", 'index': 1},
                options=[
                    {'label': 'Simple', 'value': 'simple'},
                    {'label': 'Druid', 'value': 'druid'},
                    {'label': 'Athena', 'value': 'athena'}
                ],
                value=''
            )
        ])

    def data_source_test_save(self):
        return html.Div(children=[
            html.Div(className="row medium text-muted", children=[
                html.Div(className="col-sm-3 text-truncate", children=[
                    html.Em("Data Source Name:")
                ]),
                html.Div(id={'type': "data-source-name-review", 'index': 1}, className="col", children=[])
            ]),
            html.Div(className="row medium text-muted", children=[
                html.Div(className="col-sm-3 text-truncate", children=[
                    html.Em("Data Source Endpoint:")
                ]),
                html.Div(id={'type': "data-source-endpoint-review", 'index': 1}, className="col", children=[])
            ]),
            html.Div(className="row medium text-muted", children=[
                html.Div(className="col-sm-3 text-truncate", children=[
                    html.Em("Data Source Port:")
                ]),
                html.Div(id={'type': "data-source-port-review", 'index': 1}, className="col", children=[])
            ]),
            html.Div(className="row medium text-muted", children=[
                html.Div(className="col-sm-3 text-truncate", children=[
                    html.Em("Data Source Type:")
                ]),
                html.Div(id={'type': "data-source-type-review", 'index': 1}, className="col", children=[])
            ]),
            html.Br(),
            html.Div(className="row", children=[
                html.Div(className="mb-8", children=[ 
                    html.Button(
                        'Test Data Source', 
                        id={'type': "data-source-test-btn", 'index': 1}, 
                        n_clicks=0,
                        className="btn btn-primary",
                        style={
                            "margin": "20px"
                        }
                    ),  
                    html.Button(
                        'Save Data Source', 
                        id={'type': "data-source-save-btn", 'index': 1}, 
                        n_clicks=0,
                        disabled=True,
                        className="btn btn-success"
                    ),
                ])
            ]),
                
        ])


hydro_data_source = HydroDataSourceWizard()

DATA_SOURCE_BUILD_TEMPLATE = {
    1: {
        "tab_label": "data_source_name",
        "tab_header": "Data Source Name",
        "tab_details": "Provide a Unique Name for your Data Source",
        "body_header": "Step 1 - Data Source Name",
        "body_details": "Provide a Unique Name for your Data Source",
        "form": hydro_data_source.data_source_name_form()
    },
    2: {
        "tab_label": "data_source_endpoint",
        "tab_header": "Data Source Endpoint",
        "tab_details": "Provide the Endpoint for your Data Source",
        "body_header": "Step 2 - Data Source Endpoint",
        "body_details": "Provide the Endpoint for your Data Source",
        "form": hydro_data_source.data_source_endpoint_form()
    },
    3: {
        "tab_label": "data_source_type",
        "tab_header": "Data Source Type",
        "tab_details": "Provide the Data Source Type",
        "body_header": "Step 3 - Data Source Type",
        "body_details": "Provide the Data Source Type",
        "form": hydro_data_source.data_source_type_form()
    },
    4: {
        "tab_label": "data_source_test",
        "tab_header": "Data Source Test",
        "tab_details": "Provide the Endpoint for your Data Source",
        "body_header": "Step 4 - Data Source Test",
        "body_details": "Provide the Endpoint for your Data Source",
        "form": hydro_data_source.data_source_test_save()
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
    Output("wizard-step-body-state-name", 'value'),  
    Output({'type': 'input-data-source-name', 'index': ALL}, 'value'),
    Input("wizard-step-body-state-name", 'value'), 
    Input({'type': 'input-data-source-name', 'index': ALL}, 'value'), 
)
def data_source_form_fx(state, name):    
    return form_helper(state, name)


@hydro.callback(
    Output("wizard-step-body-state-endpoint", 'value'),  
    Output({'type': 'input-data-source-endpoint', 'index': ALL}, 'value'),
    Input("wizard-step-body-state-endpoint", 'value'), 
    Input({'type': 'input-data-source-endpoint', 'index': ALL}, 'value'), 
)
def data_source_form_endpoint(state, endpoint):   
    return form_helper(state, endpoint)

@hydro.callback(
    Output("wizard-step-body-state-port", 'value'),  
    Output({'type': 'input-data-source-port', 'index': ALL}, 'value'),
    Input("wizard-step-body-state-port", 'value'), 
    Input({'type': 'input-data-source-port', 'index': ALL}, 'value'), 
)
def data_source_form_port(state, port):   
    return form_helper(state, port)

@hydro.callback(
    Output("wizard-step-body-state-type", 'value'),  
    Output({'type': 'input-data-source-type', 'index': ALL}, 'value'),
    Input("wizard-step-body-state-type", 'value'), 
    Input({'type': 'input-data-source-type', 'index': ALL}, 'value'), 
)
def data_source_form_type(state, source_type):   
    return form_helper(state, source_type)

@hydro.callback(  
    Output({'type': 'data-source-name-review', 'index': ALL}, 'children'),
    Output({'type': 'data-source-endpoint-review', 'index': ALL}, 'children'),
    Output({'type': 'data-source-port-review', 'index': ALL}, 'children'),
    Output({'type': 'data-source-type-review', 'index': ALL}, 'children'),
    Input("wizard-step-body-state-name", 'value'),
    Input("wizard-step-body-state-endpoint", 'value'),  
    Input("wizard-step-body-state-port", 'value'),  
    Input("wizard-step-body-state-type", 'value'),  
)
def data_source_form_review(name, endpoint, port, ds_type):    
    return [name], [endpoint], [port], [ds_type]

@hydro.callback(   
    Output({'type': 'data-source-test-btn', 'index': ALL}, 'disabled'),
    Output({'type': 'data-source-save-btn', 'index': ALL}, 'disabled'),
    Input({'type': 'data-source-test-btn', 'index': ALL}, 'n_clicks'),
    Input({'type': 'data-source-name-review', 'index': ALL}, 'children'),
    Input({'type': 'data-source-endpoint-review', 'index': ALL}, 'children'),
    Input({'type': 'data-source-port-review', 'index': ALL}, 'children'),
    Input({'type': 'data-source-type-review', 'index': ALL}, 'children')
)
def data_source_test(test_btn, name, endpoint, port, ds_type):     
    if ds_type[0] == "druid":
        if test_btn[0] > 0:
            status = druid.druid_status(endpoint, port)
            if status:
                return [False], [False]  
        if name != '' and endpoint != '' and port != '' and ds_type != '':
            return [False], [True]
    elif name != '' and endpoint != '' and port != '' and ds_type != '':
        return [False], [True]
    return [True], [True]

@hydro.callback(   
    Output({'type': 'data-source-save-btn', 'index': ALL}, 'n_clicks'), 
    Input({'type': 'data-source-save-btn', 'index': ALL}, 'n_clicks'),
    Input({'type': 'data-source-name-review', 'index': ALL}, 'children'),
    Input({'type': 'data-source-endpoint-review', 'index': ALL}, 'children'),
    Input({'type': 'data-source-port-review', 'index': ALL}, 'children'),
    Input({'type': 'data-source-type-review', 'index': ALL}, 'children')
)
def data_source_save(save_btn, name, endpoint, port, ds_type): 
    if save_btn[0] > 0: 
        conn = pg.postgres_connection(host=os.environ['POSTGRES_HOST'], port=os.environ['POSTGRES_PORT'], database=os.environ['POSTGRES_DB'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'])
        pg.postgres_data_source_insert(conn, name[0], endpoint[0], port[0], ds_type[0]) 
    return [0]