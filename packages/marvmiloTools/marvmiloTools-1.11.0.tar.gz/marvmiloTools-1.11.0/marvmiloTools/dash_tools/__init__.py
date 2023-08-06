import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import string
import random

#import other scripts
from . import browsertime
from . import nav
 
#meta tags for mobile optimization
mobile_optimization = {"name": "viewport", "content": "width=device-width, initial-scale=1"}
 
#function for flex style
def flex_style(additional_dict = dict()):
    flex_style_dict = {
        "display": "flex",
        "justifyContent": "center",
        "alignItems": "center"
    }
    return {**flex_style_dict, **additional_dict}
 
#function for creating content div with specified width
def content_div(width, padding, children):
    return html.Div(
        html.Div(
            children = [
                *children,
                html.Div(style = {"width": width, "width": "100%"})
            ],
            style = {"maxWidth": width, "width": width}
        ),
        style = flex_style({"padding": padding})
    )
 
#function for creating modal header with close button
def modal_header_close(title, close_id , color = None):
    return html.Div(
        children = [
            html.H5(
                title,
                className = "modal-title"
            ),
            dbc.Button(
                className = "btn-close",
                id = close_id
            )  
        ],
        className = "modal-header",
        style = {
            "background": color,
            "borderColor": color
        }
    )

#function for creating random dash id
def random_ID(length):
    return "".join(random.choice(string.ascii_letters) for i in range(length))

#function for creating picture
def picture(path, width = "100%", aspect_ratio = "16 / 9", children = [], additional_style = {}):
    style = {
        "backgroundImage": f"url(/assets/{path})",
        "backgroundSize": "cover",
        "aspectRatio": aspect_ratio,
        "width": width
    }
    
    style = style | additional_style
    
    return html.Div(
        children = children,
        style = style
    )