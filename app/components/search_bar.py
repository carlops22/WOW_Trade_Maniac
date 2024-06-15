import dash_bootstrap_components as dbc
from dash import dcc

def create_search_bar(items):
    search_bar = dbc.Col(
        dcc.Dropdown(
            id='search-bar',
            options=[{'label': item, 'value': item} for item in items],
            placeholder="Search for an item",
            className="search-bar",
        ),
        width=8
    )
    return search_bar
