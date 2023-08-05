import dash, json, requests, os
from dash import dcc 
from dash import html 
from dash.dependencies import Input, Output, State, MATCH, ALL
from hydroplane import templates 

from hydroplane.hydro import hydro  
from  hydroplane.wizards.data_source_template import DATA_SOURCE_BUILD_TEMPLATE 
from  hydroplane.wizards.query_builder_template import QUERY_BUILDER_TEMPLATE 
from hydroplane.wizards.card_builder_template import CARD_BUILDER_TEMPLATE
from hydroplane.wizards.page_builder_template import PAGE_BUILDER_TEMPLATE
from hydroplane.wizards.collection_builder_template import COLLECTION_BUILDER_TEMPLATE

class HydroWizard:
    def __init__(self):
        pass

    def multi_step_wizard_tabs(self, idx, wizard_template):
        btn_list = []
        for key in wizard_template.keys():
            step = wizard_template[key] 

            if key == idx: 
                clsName = "nav-item nav-link active"
            else: 
                clsName = "nav-item nav-link"
            btn = html.Button(id={'type':'wizard-step-btn','index':key}, n_clicks=0, className=clsName, children=[
                    html.Div(className="wizard-step-icon", children=[
                        str(key)
                    ]),
                    html.Div(className="wizard-step-text", children=[
                        html.Div(className="wizard-step-text-name", children=[
                            step["tab_header"]
                        ]),
                        html.Div(className="wizard-step-text-details", children=[
                            step["tab_details"]
                        ])
                    ])
                ])
            btn_list.append(btn)
        return btn_list
    
    def multi_step_wizard(self, wizard_template):
        btn_list = []
        body_list = []
        body_dict = {}
        for key in wizard_template.keys():
            step = wizard_template[key] 
            label = step["tab_label"]
            body_dict[label] = []

        btn_list = self.multi_step_wizard_tabs(1, wizard_template)
        body = html.Div(id="wizard-step-body", className="tab-pane py-5 py-xl-10 fade show active", children=[
                    html.Div(className="row justify-content-center", children=[
                        html.Div(className="col-xxl-8 col-xl-12", children=[
                            html.Div(style={"display": "none"}, children=[ 
                                dcc.Input(id='wizard-template', value=""),  
                            ]),
                            html.Div(id="wizard-state-values", style={"display": "none"}, children=[ 
                                dcc.Input(id='wizard-step-body-state-name', value=""), 
                                dcc.Input(id='wizard-step-body-state-endpoint', value=""), 
                                dcc.Input(id='wizard-step-body-state-port', value=""), 
                                dcc.Input(id='wizard-step-body-state-type', value=""), 

                                dcc.Input(id='wizard-step-body-state-query-name', value=""), 
                                dcc.Input(id='wizard-step-body-state-query-data-source-name', value=""), 
                                dcc.Input(id='wizard-step-body-state-query-object', value=""), 
                                dcc.Dropdown(id='wizard-step-body-state-query-dimensions', value=[], multi=True), 

                                dcc.Input(id='wizard-step-body-state-card-name', value=""), 
                                dcc.Input(id='wizard-step-body-state-card-type', value=""), 
                                dcc.Input(id='wizard-step-body-state-card-query', value=""), 
                                dcc.Input(id='wizard-step-body-state-card-type-selector', value=""), 
                                dcc.Input(id='wizard-step-body-state-chart-type-selector', value=""), 
                                dcc.Dropdown(id='wizard-step-body-state-chart-type-dimensions-selector', value=[], multi=True),  
                                dcc.Dropdown(id='wizard-step-body-state-tbl-type-dimensions-selector', value=[], multi=True),  

                                dcc.Input(id='wizard-step-body-state-page-name', value=""),  
                                dcc.Input(id='wizard-step-body-state-page-endpoint', value=""),  
                            ]),
                            html.H3(id="wizard-step-body-header", className="text-primary", children=[]),
                            html.H5(id="wizard-step-body-details", className="card-title mb-4", children=[]),
                            html.Div(id="wizard-step-body-form", className="row gx-3", children=[])

                        ])
                    ])
                ])
        return html.Div(className="col-lg-12 mb-4", children=[
            html.Div(className="card", children=[
                html.Div(className="card-header border-bottom", children=[
                    html.Div(id="wizard-step-tabs", className="nav nav-pills nav-justified flex-column flex-xl-row nav-wizard", children=btn_list)
                ]),
                html.Div(className="card-body", children=[
                    html.Div(className="tab-content", children=body)
                ])
            ])
        ]) 

 


@hydro.callback(
    Output('wizard-template', 'value'), 
    Input('url', 'pathname')
)
def wizard_template(url): 
    if url == "/wizard/query": 
        return "query"
    elif url == "/wizard/data-source":
        return "data-source"
    elif url == "/wizard/card":
        return "card"
    elif url == "/wizard/page":
        return "page"
    elif url == "/wizard/collection":
        return "collection"
    else:
        return ""


@hydro.callback(
    Output("wizard-step-tabs", "children"),
    Output("wizard-step-body-header", "children"),
    Output("wizard-step-body-details", "children"),
    Output("wizard-step-body-form", "children"),
    Output({'type': 'wizard-step-btn', 'index': ALL}, 'n_clicks'),
    Input('wizard-template', 'value'),  
    Input({'type': 'wizard-step-btn', 'index': ALL}, 'n_clicks'),   
)
def show_step(template, step_clicks): 
    if template == "query":
        build_template = QUERY_BUILDER_TEMPLATE
    elif template == "data-source":
        build_template = DATA_SOURCE_BUILD_TEMPLATE
    elif template == "card":
        build_template = CARD_BUILDER_TEMPLATE
    elif template == "page":
        build_template = PAGE_BUILDER_TEMPLATE
    elif template == "collection":
        build_template = COLLECTION_BUILDER_TEMPLATE
    else:
        build_template = DATA_SOURCE_BUILD_TEMPLATE 
    clicks_len = len(step_clicks) 
    hydro_wizard = HydroWizard()
    tabs = hydro_wizard.multi_step_wizard_tabs(1, build_template)
    header = build_template[1]["body_header"]
    details = build_template[1]["body_details"]
    form = build_template[1]["form"]
    for i, val in enumerate(step_clicks):
        if val == 1: 
            tabs = hydro_wizard.multi_step_wizard_tabs(i+1, build_template)
            header = build_template[i+1]["body_header"]
            details = build_template[i+1]["body_details"]
            form = build_template[i+1]["form"]
            return tabs, header, details, form, [0]*clicks_len 
    return tabs, header, details, form, [0]*clicks_len