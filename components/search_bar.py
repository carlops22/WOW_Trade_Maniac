import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, callback
from dash import html

def create_search_bar():
    search_bar = dbc.Col(
    dcc.Input(
        id='search-bar',
        type='text',
        placeholder="Search for an item",
        className="search-bar",
    ),
    width=8
)
    return search_bar
