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

from hydroplane.components import cards


class HydroPageWizard:
    def __init__(self):
        pass

    def page_wizard_name_collection_form(self):
        return html.Div(id={'type': "input-page-name-collection-wrapper", 'index': 1}, className="mb-3", children=[
            dcc.Input(
                id={'type': 'input-page-name', 'index': 1},
                className="form-control",
                type="text",
                placeholder="Page Name...",
            ),
            html.Br(),
            dcc.Input(
                id={'type': 'input-page-endpoint', 'index': 1},
                className="form-control",
                type="text",
                placeholder="Page Endpoint (i.e. /example)...",
            ),
            html.Br(),
            html.Button(id="temp-save-btn", className="btn btn-danger", n_clicks=0, children="TEMP SAVE BTN")
        ])

    def page_wizard_preview(self, card_idx=0, card_size="preview", body=None):
        if body == None:
            body = html.Div(children=[
                html.Br(),
                dcc.Dropdown( 
                    id={'type': "input-page-card-selector", 'index': card_idx},
                    placeholder="Select Card...",
                    options=[], 
                    value=''
                ),
                html.Br()
            ])
            
        return html.Div(id="page-rows", children=[
            html.Div(id="test-page-card", className="row", children=[
                cards.plain_card(card_idx+2, "preview-1", body), 
                html.Div(className="col-lg-2 mb-4", children=[ 
                    html.Div(style={"height": "20px;"}),
                    html.Div(style={"height": "10px"}), 
                    html.Button(className="btn btn-primary", children="+ Card"),
                    html.Br(),
                    html.Div(style={"height": "20px"}), 
                    html.Button(className="btn btn-danger", children="- Row"), 
                ])
            ]),
            html.Div(id={'type': "input-page-row", 'index': 2}, className="row", children=[
                cards.plain_card(card_idx, "preview-2", body), 
                cards.plain_card(card_idx+1, "preview-2", body), 
                html.Div(className="col-lg-2 mb-4", children=[ 
                    html.Div(style={"height": "20px;"}),
                    html.Div(style={"height": "10px"}), 
                    html.Button(className="btn btn-primary", children="+ Card"),
                    html.Br(),
                    html.Div(style={"height": "20px"}), 
                    html.Button(className="btn btn-danger", children="- Row"), 
                ])
            ]),
            html.Div(className="row", children=[ 
                html.Div(className="col-lg-2 mb-4", children=[  
                    html.Button(className="btn btn-primary", children="+ Row") 
                ])
            ])
        ])



hydro_page = HydroPageWizard()

PAGE_BUILDER_TEMPLATE = {
    1: {
        "tab_label": "page_name",
        "tab_header": "Page Name",
        "tab_details": "Name Your Page & Assign to a Collection",
        "body_header": "Step 1 - Page Name & Collection",
        "body_details": "Provide a Unique Name for your Page & Assign to a Collection",
        "form": hydro_page.page_wizard_name_collection_form()
    },
    2: {
        "tab_label": "page_layout",
        "tab_header": "Page Layout",
        "tab_details": "Build Your Layout",
        "body_header": "Step 1 - Page Layout",
        "body_details": "Build Your Page Layout",
        "form": hydro_page.page_wizard_preview()
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
    Output("wizard-step-body-state-page-name", 'value'),  
    Output({'type': 'input-page-name', 'index': ALL}, 'value'), 
    Input("wizard-step-body-state-page-name", 'value'), 
    Input({'type': 'input-page-name', 'index': ALL}, 'value'), 
)
def page_wizard_name(state, name):  
    return form_helper(state, name)


@hydro.callback(
    Output("wizard-step-body-state-page-endpoint", 'value'),  
    Output({'type': 'input-page-endpoint', 'index': ALL}, 'value'), 
    Input("wizard-step-body-state-page-endpoint", 'value'), 
    Input({'type': 'input-page-endpoint', 'index': ALL}, 'value'), 
)
def page_wizard_name(state, name):  
    return form_helper(state, name)


@hydro.callback( 
    Output("temp-save-btn", 'n_clicks'), 
    Input("wizard-step-body-state-page-name", 'value'),
    Input("wizard-step-body-state-page-endpoint", 'value'), 
    Input("temp-save-btn", 'n_clicks'),
)
def page_wizard_preview_save(name, endpoint, clicks): 
    page_layout = ["Test Name ABCDEFGHIJKLMNOPQRSTUVWXYZ"] 
    if clicks > 0:
        conn = pg.postgres_connection(host=os.environ['POSTGRES_HOST'], port=os.environ['POSTGRES_PORT'], database=os.environ['POSTGRES_DB'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'])
        pg.postgres_data_source_page_insert(conn, name, endpoint, page_layout)
    return 0