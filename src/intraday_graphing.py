import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from src.intraday_data import minute_candlesticks

app = dash.Dash(__name__)

fig = go.Figure(data=go.Ohlc(x=minute_candlesticks['minute'],
                             open=minute_candlesticks['open'],
                             high=minute_candlesticks['high'],
                             low=minute_candlesticks['low'],
                             close=minute_candlesticks['close']),
                name='OHLC-graph')

app.layout = html.Div([
    dcc.Graph(id='live-graph', figure=fig, animate=True),  # need id to update objects in js
    dcc.Interval(
        id='graph-update',
        interval=1000
    ),
])


@app.callback(Output('live-graph', 'figure'),
              Input('graph-update', 'interval'))
def update_graph():
    return {
        'data': fig,
        'layout': go.Layout(xaxis=range(0, len(minute_candlesticks)))  # might need to update yaxis as well
    }


if __name__ == '__main__':
    app.run_server(debug=True)

