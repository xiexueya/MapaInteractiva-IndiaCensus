#!/usr/bin/env python
# coding: utf-8

# In[7]:


import dash
import pathlib
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import json
import numpy as np

# In[8]:


india_states = json.load(open("states_india.geojson", "r"))

# In[9]:


state_id_map = {}
for feature in india_states["features"]:
    feature["id"] = feature["properties"]["state_code"]
    state_id_map[feature["properties"]["st_nm"]] = feature["id"]

# In[10]:
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

inf = pd.read_csv(DATA_PATH.joinpath("india_census.csv"))
inf["Density"] = inf["Density[a]"].apply(lambda x: int(x.split("/")[0].replace(",", "")))
inf["id"] = inf["State or union territory"].apply(lambda x: state_id_map[x])

# In[11]:


inf.head()

# In[12]:


inf["Density"].plot()

# In[13]:


inf["DensityScale"] = np.log10(inf["Density"])
inf["DensityScale"].plot()

# In[ ]:


app = dash.Dash(__name__)
server = app.server

img = px.choropleth(
    inf,
    locations="id",
    geojson=india_states,
    color="DensityScale",
    hover_name="State or union territory",
    hover_data=["Density"],
    title="India Population Density",
)
img.update_geos(fitbounds="locations", visible=False)

app.layout = html.Div([
    html.Div([
        html.H1('India Census')
    ], className='banner'),

    html.Div([
        html.Div([
            html.P('Selecciona el candidato', className='fix_label', style={'color': 'black', 'margin-top': '2px'}),
            dcc.RadioItems(id='india-radioitems',
                           labelStyle={'display': 'inline-block'},
                           options=[
                               {'label': 'Rural population', 'value': 'Rural population'},
                               {'label': 'Urban population', 'value': 'Urban population'}
                           ], value='Rural population',
                           style={'text-aling': 'center', 'color': 'black'}, className='dcc_compon'),
        ], className='create_container2 five columns', style={'margin-bottom': '20px'}),
    ], className='row flex-display'),

    html.Div([
        html.Div([
            dcc.Graph(id='my_graph', figure={})
        ], className='create_container2 eight columns'),

        html.Div([
            dcc.Graph(id='pie_graph', figure={})
        ], className='create_container2 five columns'),

        html.Div([
            dcc.Graph(id='Choropleth of India', figure=img)
        ], className='create_container2 five columns')
    ], className='row flex-display'),
], id='mainContainer', style={'display': 'flex', 'flex-direction': 'column'})


@app.callback(
    Output('my_graph', component_property='figure'),
    [Input('india-radioitems', component_property='value')])
def update_graph(value):
    if value == 'Rural population':
        fig = px.bar(
            data_frame=inf,
            x='State or union territory',
            y='Rural population')
    else:
        fig = px.bar(
            data_frame=inf,
            x='State or union territory',
            y='Urban population')
    return fig


@app.callback(
    Output('pie_graph', component_property='figure'),
    [Input('india-radioitems', component_property='value')])
def update_graph_pie(value):
    if value == 'Rural population':
        fig2 = px.pie(
            data_frame=inf,
            names='State or union territory',
            values='Rural population')
    else:
        fig2 = px.pie(
            data_frame=inf,
            names='State or union territory',
            values='Urban population'
        )
    return fig2


if __name__ == '__main__':
    app.run_server(debug=False)
