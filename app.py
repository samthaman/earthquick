import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import os
import visualizations as vis

pre= os.path.dirname(os.path.realpath(__file__))
fname = 'all_month.csv'
path = os.path.join(pre, fname)
df = pd.read_csv(path)

#Add Columns
dff = df.copy()
dff['Clock']=pd.DatetimeIndex(dff['time']).hour
dff['Month'] = pd.DatetimeIndex(dff['time']).month
add_ones_column = dff.loc[:,'ones'] = 1


#prepare slider
mag_list = set(int(i) for i in sorted(df['mag'].dropna().unique()) if i>=0)
dd_mag = [{'label':str(int(i)), 'value':int(i)} for i in mag_list]
slider = {num:{'label':str(num), 'style':{'color': 'white'}} for num in mag_list}


#prepare dropdown
lands = list(set([i.split(', ')[0] if len(i.split(', '))==1 else i.split(', ')[1] for i in df['place']]))
dd_land = [{'label':i, 'value':i} for i in sorted(lands)]
sorted_lands = sorted(lands)

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

server = app.server

#=====================
# START PAGE LAYOUT
#=====================

#navbar
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        #dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Earthquick", className="ms-2")),
                    ],
                    align="left",
                    className="g-0",
                ),
            ),

            # Button
            dbc.Col(
                dbc.Button(
                    'über das Dashboard',
                    outline=False,
                    color="primary",
                    className="me-1",
                    id='infoButton',
                    n_clicks=0),
                className="d-grid gap-2 pr-2 row align-items-center",
            ),

            # modal contents
            dbc.Modal(
                [
                    dbc.ModalHeader(
                        html.H4('Willkommen auf dem Dashboard zur Visualisierung von Erdbebendaten')
                    ),

                    dbc.ModalBody(html.Div([
                        html.P([
                            dcc.Markdown('''
                Auf diesem Dashboard werden Daten zu Erdbeben der USGS (https://earthquake.usgs.gov/) in verschiedenen 
                Diagrammen visualisiert. Mithilfe einer Magnitude-Slide lassen sich die Daten in den Diagrammen 
                einheitlich anpassen. Im Diagramm zur Visualisierung der durchschnittlichen Erdbebentiefe pro Land 
                lassen sich zudem durch manuelle Anpassungen verschiedene Länder bezüglich ihrer durchschnittlichen 
                Erdbebentiefe vergleichen. 
                Wir hoffen sehr, mit diesem Dashboard einen interessanten Einblick in die Welt der Seismologie geben zu können.
                
                ##### Landkarte
                Die Landkarte visualisiert die weltweit vorkommenden Erdbeben, gefiltert nach der in der Slide ausgewählten Magnitude-Stärke. Die unterschiedliche Colorierung der Punkte bezieht sich auf die unterschiedliche Magnitude-Stärken. Die jeweilige Farbverteilung ist auf der rechten Seite der Landkarte ersichtlich.
                                
                ##### Durchschnittliche Erdbebentiefe pro Länder
                In dem Diagramm zum Vergleich der durchschnittlichen Erdbebentiefe in Kilometern können beliebig viele Länder gleichzeitig miteinander verglichen werden. Die Auswahl der Länder erfolgt mithilfe einer Drop-Down Liste; links neben dem Symbol für die Drop-Down Liste ist zudem ein Reset-Kreuz für das Löschen der aktuellen Auswahl vorhanden. Auch ein Re-Load der gesamten Website setzt das Diagramm wieder auf den Ausgangspunkt zurück. Die Erdbebentiefe in km ist auf der y-Achse; die Länderauswahl auf der x-Achse ersichtlich.
                
                ##### Durchschnittliche Magnitude pro Uhrzeit
                In dem Diagramm Durchschnittliche Magnitude pro Uhrzeit ist der Zusammenhang zwischen den beiden Variablen "Durchschnittliche Magnitude" sowie "Uhrzeit" visualisiert mithilfe eines Liniendiagramms visualisiert. Die Uhrzeit befindet sich auf der x-Achse, die Magnitude auf der y-Achse.
                
                ##### Zusammenhang zwischen Erdbebendauer und Magnitude
                In dem Diagramm " Zusammenhang zwischen Erdbebendauer und Magnitude" wird mithilfe einer linearen Regression ein möglicher Zusammenhang zwischen den beiden Variablen (Duration/rms – y-Achse) sowie der Magnitude (x-Achse) visualisiert. Die rote Linie, welche sich durch die Punktewolke zieht, stellt die Regressionsgerade dar. 
                
                ##### Boxplot zur Datenverteilung Gap / Monat
                Mithilfe des Boxplots wird nun die Datenverteilung zwischen Gap sowie dem jeweiligen Monat im Jahr dargestellt. Für eine genauere Erklärung bezüglich der Funktion des Boxplots verweisen wir gerne auf diesen Link:
                https://www.statisticshowto.com/probability-and-statistics/descriptive-statistics/box-plot/
                
                ##### Abkürzungen
                Sollten gewisse Werte aus den Diagrammen nicht direkt verständlich sein oder möchten Sie noch weitere Informationen zu den in den Erdbeben-Daten verwendeten Werten erhalten, so können Sie unter dem folgenden Link präzisiere Erklärungen bzw. Darlegungen der Abkürzungen vorfinden:
                https://earthquake.usgs.gov/data/comcat/index.php

                
                ''')])

                    ])),

                    dbc.ModalFooter(
                        [html.P(
                            'Developed by I.Kilchenmann, S.Weber-Martin and M.Hemila 2021-2022',
                            style={'margin-left': 0, 'margin-right': 'auto'}),
                            html.P(''),
                            dbc.Button(
                                "Close", id="close", className="ms-auto", n_clicks=0
                            )]  # close html.p
                    )  # close footer

                ],

                # modal options
                id="modal",
                scrollable=True,
                is_open=False,
                size="lg"

            )  # close modal




        ],
    fluid=True
    ),
    color="dark",
    dark=True,

) # close navebar

#Slider with modal button => slider controls all diagramms
slider = dbc.Row(
    [

        # Slider
        dbc.Col(['Magnitude',
            dcc.RangeSlider(
                id='mag_num',
                min=min([x['value'] for x in dd_mag]),
                max=max([x['value'] for x in dd_mag]),
                marks=slider,
                value=[min([x['value'] for x in dd_mag]), max([x['value'] for x in dd_mag])]
            )
        ], width={"size": 4, 'offset':4}),

    ],

#options slider column
style={'background-color':'grey', 'margin-right':0, 'color':'white'},
className='py-3 mb-3'
) # close


#=====================
# START DIAGRAMMS
#=====================

# diagramm mag hour
mag_hour = dbc.Row(
    dbc.Col(
        dcc.Graph(
            id='mag_hour'
        ),
        width={"size": 12}
    )
)

# diagramm regions
regions = dbc.Col([

    dbc.Row([
        dbc.Col(['Regionen auswählen',
            dcc.Dropdown(
                id='lands',
                options=dd_land,
                value=[sorted_lands[0],sorted_lands[1]],
                multi=True
            )],
        width={"size": 8, "offset": 2}
        )
    ]),

    dbc.Row(
        dbc.Col(
            dcc.Graph(
                id='land_depth',
                config={'displayModeBar': False}
            ),
        width={"size": 12})
    )
])

#diagramm map
map = dcc.Graph(id='haupt_vis')

# diagramm rms
rms=dcc.Graph(id='mag_rms')

#diagramm box_plot
box_plot = dcc.Graph(id='box_plot')



# layout for diagramms
visualisation = html.Div(
    [
        dbc.Row([
            dbc.Col( # First column
                [
                    dbc.Col(
                        [regions],
                        className='bg.light shadow p-3 mb-5 bg-body rounded'
                    ),

                    dbc.Col(
                        [mag_hour],
                        className='bg.light shadow p-3 mb-5 bg-body rounded'
                        )
                ],
                className='col-3'

            ), # End first column

            dbc.Col( # start second column
                dbc.Col(
                    [map],
                    className='bg.light shadow p-3 mb-5 bg-body rounded',
                )
            ),

            dbc.Col( # start third column
                [
                    dbc.Col(
                        [rms],
                        className='bg.light shadow p-3 mb-5 bg-body rounded'
                    ),

                    dbc.Col(
                        [box_plot],
                        className='bg.light shadow p-3 mb-5 bg-body rounded'
                    )
                ],
                className='col-3'
            ),  # End third column

        ]), # Row end

    ]
)

# building app layout
app.layout = html.Div([navbar, slider, visualisation])

#========================================
# End of App-Layout / Start of Callbacks
#========================================

@app.callback(
    [Output('haupt_vis', 'figure'),
     Output('mag_hour', 'figure'),
     Output('mag_rms', 'figure'),
     Output('box_plot', 'figure')],
    [Input('mag_num', 'value')])
def get_figures(mag_list):
    ff_df = dff[(dff['mag'] >= int(mag_list[0])) &  (dff['mag'] <= int(mag_list[1]))]

    return vis.h_diagram(ff_df),\
           vis.hours_mags(ff_df),\
           vis.mag_rms(ff_df),\
           vis.box_month_gab(ff_df)

@app.callback(
    Output('land_depth', 'figure'),
    [Input('lands', 'value'),
     Input('mag_num', 'value')]
)
def get_lands(lands_dd, mag_list):
    return vis.lands_vis(lands_dd, mag_list)

@app.callback(
    Output("modal", "is_open"),
    [Input("infoButton", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_info(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

#=============
#End Callbacks
#=============

if __name__ == '__main__':
    app.run_server(debug=True)