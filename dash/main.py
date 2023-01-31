from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

app = Dash(__name__)

colors = {
    'background': '#e5e4e4',
    'h4': '#8b3201',
    'h1': '#f77f3c'
}

######## process data
def generate_table(dataframe, max_rows=5):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ],style={
            'width': '800px',
            'overflow-x': 'auto'
            #overflow-x: hidden; 
        }
    )

df = pd.read_csv('./data/sample.csv')
cnt = pd.DataFrame(df.groupby(["subcategory"])["subcategory"].count())
cnt['index'] = cnt.index
cnt['attack'] = [1,0,1,1]
li_attack = ['stime', 'flgs', 'sport', 'pkts', 'bytes', 'seq', 'dur', 'sbytes', 'srate', 'TnBPSrcIP', 'TnBPDstIP', 'TnP_PSrcIP', 'TnP_PDstIP', 'TnP_PerProto', 'AR_P_Proto_P_DstIP', 'Pkts_P_State_P_Protocol_P_DestIP', 'Pkts_P_State_P_Protocol_P_SrcIP']
li_cat = df.select_dtypes(['object']).columns.to_list()
li_num = [item for item in df.columns.to_list() if item not in li_cat]
num_df = df
le = LabelEncoder()
for col in li_cat:
        num_df[col] = le.fit_transform(num_df[col].astype(str))
correlation = list(np.array(num_df.corr()))


####### graphics
#fig = px.bar(cnt, x="index", y="subcategory", color="attack")
fig = px.pie(df, values='attack', names='subcategory')
fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['h4']
)

fig_corr = px.imshow(correlation, color_continuous_scale='RdYlBu', x=df.columns.to_list(), y=df.columns.to_list())
fig_corr.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['h4']
)

app.layout = html.Div(style={'backgroundColor': colors['background'],'text-align':'center'}, children=[
    html.H1(
        children='Dashboard',
        style={
            'textAlign': 'center',
            'color': colors['h1']
        }
    ),

    html.Div([
        html.H4(children='Data Overview',style={'color':colors['h4']}),
        generate_table(df[li_attack])
    ]),

    html.Div([
        html.H4(children='Graph - Target',style={'color':colors['h4']}),
        dcc.Graph(
            id='graph-1',
            figure=fig
        )
    ]),
    html.Div([html.H4(children='Graph - Category Data Distribution',style={'color':colors['h4']})
    ]),
    html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                li_cat,
                li_cat[0],
                id='xaxis-column'
            )
        ], style={'width': '48%', 'display': 'inline-block'})

    ]),
    dcc.Graph(id='indicator-graphic'),
]),
    html.Div([
        html.H4(children='Graph - Correlation',style={'color':colors['h4']}),
        dcc.Graph(
            id='graph-2',
            figure=fig_corr
        )
        
    ])
])


@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('xaxis-column', 'value'))
def update_graph(xaxis_column_name):
    dff = df
    #fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
    #                 y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
    #                 hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'])
    fig = px.histogram(df[xaxis_column_name], x=xaxis_column_name, marginal="rug")

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
