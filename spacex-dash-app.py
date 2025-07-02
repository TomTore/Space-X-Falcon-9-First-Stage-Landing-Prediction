# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import os

os.chdir("./Desktop/DS/6.DSCapstone/3.Vis&Dashboards/")
# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

#create site options # Task1
options = [{'label': 'All Sites', 'value': 'ALL'}]
for Site in spacex_df["Launch Site"].value_counts().index.to_list():
    #Task1
    options.append({'label': Site, 'value': Site})

#sliders marks Task4
marks= {}
for step in list(range(0, 10001, 2500)):
    marks[step] = f'{step}'

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                    options= options,
                                    value='ALL',
                                    placeholder="place holder here",
                                    searchable=True
                                    ),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks= marks,
                                                 value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])




# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value')) #component id must be the same of the dropdown
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', #values needs to be an existing column
        names='Launch Site', 
        title='Success Rate of All sites')
    else:
        # filtro per il sito selezionato
        df_site = spacex_df[spacex_df['Launch Site'] == entered_site]
        # conto quante volte compare 0 e quante volte 1
        counts = df_site['class'].value_counts().reset_index()
        counts.columns = ['class', 'count']
        
        # costruisco la torta su count vs class
        fig = px.pie(
            counts,
            values='count',     # colonna con i numeri
            names='class',      # colonna con le etichette 0 e 1
            color='class',
            color_discrete_map={0:'#CB3234', 1:'#618E3C'},
            title=f"Success Rate for {entered_site}"
        )
    return fig

        # return the outcomes piechart for a selected site
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")]) #component id must be the same of the dropdown
def get_scatter(entered_site, slider_range):
    low, high = slider_range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df,
        x='Payload Mass (kg)', #Payload
        y='class',
        color= 'Booster Version Category',
        title='Scatterplot of Payload vs Success')
    else:
        # filtro per il sito selezionato
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        
        # costruisco la torta su count vs class
        fig = px.scatter(filtered_df,
        x='Payload Mass (kg)', #Payload
        y='class',
        color= 'Booster Version Category',
        title=f'Scatterplot of Payload vs Success: {entered_site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run()