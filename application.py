import dash
from dash import dcc, html
import dash.dependencies
import pandas as pd
import plotly.express as px

# Load COVID-19 data
url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
df = pd.read_csv(url)
df['date'] = pd.to_datetime(df['date'])

# Prepare global data
latest_df = df[df['date'] == df['date'].max()]
world_data = latest_df[['location', 'total_cases', 'total_deaths', 'iso_code']]
world_data = world_data[world_data['iso_code'].str.len() == 3]

# Global time-series data
global_df = df[df['location'] == 'World']
fig_cases = px.line(global_df, x='date', y='total_cases',
                    title='Global COVID-19 Cases Over Time')

# World choropleth map
fig_map = px.choropleth(world_data,
                        locations="iso_code",
                        color="total_cases",
                        hover_name="location",
                        color_continuous_scale="Reds",
                        title="COVID-19 Total Cases by Country")

# Country dropdown options
countries = df['location'].dropna().unique()

# Dash app layout
app = dash.Dash(__name__)
app.title = "COVID-19 Dashboard"

app.layout = html.Div([
    html.H1("COVID-19 Dashboard", style={'textAlign': 'center'}),
    
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': c, 'value': c} for c in countries],
        value='India',
        style={'width': '60%', 'margin': 'auto'}
    ),

    dcc.Graph(id='country-graph'),
    dcc.Graph(figure=fig_map),
    dcc.Graph(figure=fig_cases)
])

# Callback for country-specific graph
@app.callback(
    dash.dependencies.Output('country-graph', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value')]
)
def update_country_graph(selected_country):
    country_df = df[df['location'] == selected_country]
    fig = px.line(country_df, x='date', y='total_cases',
                  title=f'{selected_country} COVID-19 Cases Over Time')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
