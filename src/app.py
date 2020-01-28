import dash

# dash visualization
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css', "./assets/x.css"
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True
