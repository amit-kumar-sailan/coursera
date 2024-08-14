# Import required libraries
import pandas as pd
import numpy as np
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_site_values = [{"label":"ALL Sites", "value":'ALL'},
                     {"label":"CCAFS LC-40","value":"CCAFS LC-40"},
                     {"label":"VAFB SLC-4E","value":"VAFB SLC-4E"},
                     {"label":"KSC LC-39A","value":"KSC LC-39A"},
                     {"label":"CCAFS SLC-40","value":"CCAFS SLC-40"}]


# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                html.Div(dcc.Dropdown(id='site-dropdown',
                                                        options=launch_site_values,
                                                        value='ALL',
                                                        placeholder='Select a Launch Site here',
                                                        searchable=True,
                                                        )),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site

                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, 
                                                max=10000,
                                                step=1000,
                                                marks={0:'0',
                                                     10000:'10000'},
                                                value=[min_payload,max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        all_pie = spacex_df[spacex_df['class']==1]
        all_pie = all_pie['Launch Site'].value_counts().reset_index(name='counts')
        fig = px.pie(all_pie,
                    values='counts', 
                    names='Launch Site', 
                    title='Total Success Launches By Site')
        return fig
    else:
        one_pie = spacex_df[spacex_df['Launch Site']==entered_site]
        one_pie = one_pie['class'].value_counts().reset_index(name='counts')
        fig = px.pie(one_pie, 
                    values='counts', 
                    names='class', 
                    title='Total Success Launches By Site -> '+str(entered_site))
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'),
            Input(component_id='payload-slider',component_property='value'))
def get_scatter_chart(entered_site,slider_values):
    if entered_site == 'ALL':
        all_pie = spacex_df[spacex_df['Payload Mass (kg)']>=list(slider_values)[0]]
        all_pie = all_pie[all_pie['Payload Mass (kg)']<=list(slider_values)[1]]
        fig = px.scatter(all_pie,
                        x='Payload Mass (kg)',
                        y='class',
                        color='Booster Version Category',
                        title='Correlation between Payload and Success for -> '+str(entered_site))
        return fig
    else:
        one_pie = spacex_df[spacex_df['Launch Site']==entered_site]
        one_pie = one_pie[one_pie['Payload Mass (kg)']>=list(slider_values)[0]]
        one_pie = one_pie[one_pie['Payload Mass (kg)']<=list(slider_values)[1]]
        print(one_pie.shape)
        fig = px.scatter(one_pie,
                        x='Payload Mass (kg)',
                        y='class',
                        color='Booster Version Category',
                        title='Correlation between Payload and Success for -> '+str(entered_site))
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()