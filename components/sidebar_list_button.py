from dash import html

def create_sidebar_list_button(top_text, bottom_text, icon_path):
    return html.Button([
        html.Div([
            html.Img(src=icon_path, style={'width': '24px', 'height': '24px'})  
        ], className="icon-circle"),
        html.Div([
            html.Span(top_text, className="small-title"),
            html.Span(bottom_text, className="large-title")
        ], className="title-container")
    ], className="sidebar-list-button", n_clicks=0)
