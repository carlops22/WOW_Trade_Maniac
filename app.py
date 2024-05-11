import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd

from components.search_bar import create_search_bar
from components.sidebar_categeory_dropdown import create_category_dropdown
from components.sidebar_list_button import create_sidebar_list_button

#PLACER HODLER DATAAA cambiarr
df = pd.DataFrame({
    'Item': ['Rune Cloth', 'Arcane Crystal', 'Elixir of Giants'],
    'Current Price': [20, 120, 15],
    'Historical Prices': [[18, 19, 20, 21, 20], [110, 115, 118, 120, 122], [12, 13, 14, 15, 16]]
})

dropdown_categories = ['Weapons', 'Armor', 'Consumables', 'Materials', 'Miscellaneous']
dropdown_items = ['Swords', 'Axes', 'Maces', 'Daggers', 'Staves', 'Bows', 'Crossbows', 'Guns', 'Wands']

# Create a Dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://use.fontawesome.com/releases/v5.8.1/css/all.css'])

# Layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([ 
            create_sidebar_list_button("precios","ACTUALES","/assets/icons/price-tag.png"), 
            create_sidebar_list_button("precios","HISTORICOS","/assets/icons/price-tag.png"), 
            *[create_category_dropdown(category, dropdown_items) for category in dropdown_categories],
        ], width=3, className = "col1"),
        dbc.Col([
            dbc.Row([
                dbc.Col(html.Div([
                    html.H2("WOW TRADE MANIAC", className="tm-h2"),
                    html.H2("Plataforma para tradear y craftear.", className="tm-h2-subtitle"),
                ]), width=4),
                create_search_bar(),
            ], class_name="top-bar"),
            dbc.Card([
            html.H2(id='item-title', style={'color': 'white'}),
                #dbc.CardImg(id='item-image'),  
                dbc.CardBody([
                    html.H4('Current Prices', style={'color': 'white'}),
                    html.P(id='current-prices', style={'color': 'white'}),
                    dcc.Graph(id='price-history-graph'),
                ])
            ], class_name="item_card")
        ], width=8 , className = "col2",  style = {"margin-left": "100px;"})
    ], className = "column-style")
])

# Callbacks
@callback(
    Output('item-title', 'children'),
    Output('current-prices', 'children'),
    Output('price-history-graph', 'figure'),
    Input('search-bar', 'value')
)
def update_item_details(search_value):
    if search_value is None:
        search_value = 'Rune Cloth'
    filtered_df = df[df['Item'].str.contains(search_value, case=False, na=False)]
    if filtered_df.empty:
        return "No Item Found", "", {}
    item = filtered_df.iloc[0]
    return item['Item'], f"${item['Current Price']}", {
        'data': [{'x': [1, 2, 3, 4, 5], 'y': item['Historical Prices'], 'type': 'line'}],
        'layout': {'title': 'Price History'}
    }

# app run!
if __name__ == '__main__':
    app.run_server(debug=True)
