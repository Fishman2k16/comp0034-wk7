from pathlib import Path
from dash import html
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.express as px

event_data = Path(__file__).parent.parent.parent.joinpath("data", "paralympic_events.csv")
location_data = Path(__file__).parent.parent.parent.joinpath("data", "latlon.csv")

def line_chart(feature):
    """ Creates a line chart with data from paralympics_events.csv

    Data is displayed over time from 1960 onwards.
    The figure shows separate trends for the winter and summer events.

     Parameters
     feature: events, sports or participants

     Returns
     fig: Plotly Express line figure
     """

    # take the feature parameter from the function and check it is valid
    if feature not in ["sports", "participants", "events", "countries"]:
        raise ValueError(
            'Invalid value for "feature". Must be one of ["sports", "participants", "events", "countries"]')
    else:
        # Make sure it is lowercase to match the dataframe column names
        feature = feature.lower()

    # Read the data from pandas into a dataframe
    cols = ["type", "year", "host", "events", "sports", "participants", "countries"]
    line_chart_data = pd.read_csv(event_data, usecols=cols)

    title_text = f"How has the number of {feature} changed over time?"

    # Create a Plotly Express line chart with the following parameters
    #  line_chart_data is the DataFrane
    #  x="year" is the column to use as a x-axis
    #  y=feature is the column to use as the y-axis
    # color="type" indicates if winter or summer
    fig = px.line(line_chart_data,
                  x = "year",
                  y = feature,
                  color = "type",
                  title = title_text,
                  labels = {'year': 'Year',
                            feature: '', 'type': ''},
                  template = "simple_white"
                  )
    return fig

def bar_gender(event_type):
    """
    Creates a stacked bar chart showing change in the number of sports in the summer and winter paralympics
    over time
    An example for exercise 2.

    :param event_type: str Winter or Summer
    :return: Plotly Express bar chart
    """
    cols = ['type', 'year', 'host', 'participants_m', 'participants_f', 'participants']
    df_events = pd.read_csv(event_data, usecols=cols)
    # Drop Rome as there is no male/female data
    df_events.drop([0], inplace=True, )
    df_events.reset_index(drop=True)
    # Add new columns that each contain the result of calculating the % of male and female participants
    df_events['M%'] = df_events['participants_m'] / df_events['participants']
    df_events['F%'] = df_events['participants_f'] / df_events['participants']
    # Sort the values by Type and Year
    df_events.sort_values(['type', 'year'], ascending=(True, True), inplace=True)
    # Create a new column that combines Location and Year to use as the x-axis
    df_events['xlabel'] = df_events['host'] + ' ' + df_events['year'].astype(str)
    # Create the stacked bar plot of the % for male and female
    df_events = df_events.loc[df_events['type'] == event_type]

    fig = px.bar(df_events,
                 x='xlabel',
                 y=['M%', 'F%'],
                 title='How has the ratio of female:male participants changed?',
                 labels={'xlabel': '', 'value': '', 'variable': ''},
                 color_discrete_map={'M%': 'blue', 'F%': 'green'},
                 template="simple_white"
                 )
    
    fig.update_xaxes(ticklen=0)
    return fig

"""
def scatter_geo():
    # create database connection
    df_locs = pd.read_csv(location_data)
    df_names = pd.read_csv(event_data)
    # The lat and lon are stored as string but need to be floats for the scatter_geo
    df_locs['lon'] = df_locs['lon'].astype(float)
    df_locs['lat'] = df_locs['lat'].astype(float)
    # Adds a new column that concatenates the city and year e.g. Barcelona 2012
    df_names['name'] = df_names['host'] + ' ' + df_names['year'].astype(str)

    fig = px.scatter_geo(df_locs,
                         lat = df_locs.lat,
                         lon = df_locs.lon,
                         hover_name = df_names.name,
                         title="Where have the paralympics been held?",
                         )
    return fig"""

def create_card(event_id):
    """
    Generate a card for the event specified by event_id.

    Uses the REST API route.

    Args:
        event_id:

    Returns:
        card: dash boostrap components card for the event
    """
    # Use python requests to access your REST API on your localhost
    # Make sure you run the REST APP first and check your port number if you changed it from the default 5000
    url = f"http://127.0.0.1:5000/events/{event_id}"
    event_response = requests.get(url)
    ev = event_response.json()

    # Variables for the card contents
    logo = f'logos/{ev['year']}_{ev['host']}.jpg'
    dates = f'{ev['start']} to {ev['end']}'
    host = f'{ev['host']} {ev['year']}'
    highlights = f'Highlights: {ev['highlights']}'
    participants = f'{ev['participants']} athletes'
    events = f'{ev['events']} events'
    countries = f'{ev['countries']} countries'

    card = dbc.Card([
        dbc.CardBody(
            [
                html.H4([html.Img(src=app.get_asset_url(logo), width=35, className="me-1"),
                         host]),
                html.Br(),
                html.H6(dates, className="card-subtitle"),
                html.P(highlights, className="card-text"),
                html.P(participants, className="card-text"),
                html.P(events, className="card-text"),
                html.P(countries, className="card-text"),
            ]
        ),
    ],
        style={"width": "18rem"},
    )
    return card


# Set to display event 12, this will be changed next week using a callback
card = create_card(12)