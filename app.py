from dash import Dash, dcc, html, Input, Output, callback
# import dash
from pages import onglet_1, onglet_2
import base64

def LayoutPageAccueil():
    color_font = '#F9F3FF'
    encoded_logo = base64.b64encode(open('data/logo.png', 'rb').read())
    layout = html.Div([
                html.Div([
                    html.H1('Page d\'accueil', style={'flex-grow':'2'}),
                    html.Div([
                        html.H1('Toulouse FC', style={'flex-grow':'1',
                                                    'text-align':'right'}),
                            
                        html.Img(src='data:image/png;base64,{}'.format(encoded_logo.decode()),
                                    style={'height': '90px',
                                            'margin-left': '20px'}),
                    ], style={'display':'flex',
                            'flex-direction':'row',
                            'flex-grow':'1'}),
                
                ], style={
                        # 'width':'100%',
                        'display':'flex',
                        'flex-direction': 'row'}),
                html.Br(),
                html.Br(),
                html.Div([
                        html.H2("Menu :"),
                        dcc.Link("Analyse distributionnelle", href='/onglet_1'),
                        html.Br(),
                        dcc.Link("Dashboard", href='/onglet_2')
                    ], style={'display':'flex',
                            'flex-direction':'column',
                            'flex-grow':'1',
                            'text-align':'center'}),
                html.Hr(),
                html.Div([
                    html.Div([
                        html.P('La partie \'Analyse distributionnelle\' se concentre sur un seul joueur.'+ 
                            ' Elle permet d\'étudier le comportement du joueur sélectionné par rapport à son comportement habituel.'+
                            ' Des informations sur son temps de jeu sont disponibles, ainsi qu\'une comparaison des 2 mi-temps de ses matchs.'),
                    ], style={"margin": "0 auto",
                            'width':'70%'}),
                    html.Div([
                        html.P('La partie \'Dashboard\' permet d\'étudier tous les joueurs d\'un match en même temps.'+ 
                            ' Cette analyse simultanée permet de distinguer un comportement anormal pour un joueur en le mettant en relief avec le comportement des autres joueurs au même moment.'+
                            ' Un gradient de couleurs allant du vert pour le positif au rouge pour le négatif permet de voir d\'un coup d\'oeil les joueurs n\'étant pas en forme.'+
                            ' 5 seuils personnalisables permettent de choisir quelles différences sont jugées significatives.'),
                    ], style={"margin": "0 auto",
                            'width':'70%'}),
                ], style={'flex-grow':'1',
                            'align-items': 'center'}),
                
    ], style={'display': 'flex', 
          'flex-direction': 'column',
          'background-color': color_font,
          "font-family": "Roboto, Helvetica",
          'text-align':'center',
          'height':'100vh'
          })
    return layout

app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/onglet_1':
        return onglet_1.layout
    elif pathname == '/onglet_2':
        return onglet_2.layout
    else:
        return LayoutPageAccueil()

if __name__ == '__main__':
    app.run_server(debug=True)