# Troisième version de l'appli, ajout d'autres variables d'analyse des distributions en plus de l'IQR
# Import packages
from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import base64

logo_filename = 'data/logo.png'
encoded_logo = base64.b64encode(open(logo_filename, 'rb').read())

df_instants_MT = pd.read_csv('data/df_instants_MT.csv')
df_quantiles_5_min = pd.read_csv('data/df_infos_distributions_5min.csv')
# df_quantiles_10_min = pd.read_csv('data/df_quantiles_10_min.csv')
df_quantiles_15_min = pd.read_csv('data/df_infos_distributions_15min.csv')

df_quantiles_5_min = df_quantiles_5_min.loc[((df_quantiles_5_min.min_fin_fenetre <= 45)|(df_quantiles_5_min.moment != 'MT1'))&(df_quantiles_5_min.min_fin_fenetre <= 45)]
# df_quantiles_10_min = df_quantiles_10_min.loc[(df_quantiles_10_min.min_fin_fenetre <= 50)]
df_quantiles_15_min = df_quantiles_15_min.loc[((df_quantiles_15_min.min_fin_fenetre <= 45)|(df_quantiles_15_min.moment != 'MT1'))&(df_quantiles_15_min.min_fin_fenetre <= 45)]


# Initialize the app
app = Dash(__name__)

# App layout
color_font = '#F9F3FF'
app.layout = html.Div([
    html.Div([
        html.H1('Analyse distributionnelle des matchs'),
        # html.Hr(),
        html.Div([
            html.Div([
                html.Label('Taille des fenêtres (en minutes)'),
                dcc.Dropdown(
                    id='taille-fenetre-dropdown',
                    options=['5','15'],
                    value='15',),
                
                html.Label('Variable mesurée à étudier'),
                dcc.Dropdown(
                    id='variable-mesuree-dropdown',
                    options=[
                        {'label': 'NormeGradAcc', 'value': 'NormeGradAcc'},
                        {'label': 'NormeGradGyro', 'value': 'NormeGradGyro'},
                        {'label': 'ACC X', 'value': 'ACC X'},
                        {'label': 'ACC Y', 'value': 'ACC Y'},
                        {'label': 'ACC Z', 'value': 'ACC Z'},
                        {'label': 'GYRO X', 'value': 'GYRO X'},
                        {'label': 'GYRO Y', 'value': 'GYRO Y'},
                        {'label': 'GYRO Z', 'value': 'GYRO Z'},
                    ],
                    value='NormeGradAcc',
                ),
                html.Label('Choix de la variable d\'analyse'),
                dcc.Dropdown(
                    id='variable-analyse-dropdown',
                    options=[
                        {'label': 'IQR', 'value': 'IQR'},
                        {'label': 'mean', 'value': 'mean'},
                        {'label': 'std', 'value': 'std'},
                        {'label': 'skewness', 'value': 'skewness'},
                        {'label': 'kurtosis', 'value': 'kurtosis'},
                        {'label': 'RMS', 'value': 'RMS'},
                        {'label': 'Q10', 'value': 'Q10'},
                        {'label': 'Q25', 'value': 'Q25'},
                        {'label': 'median', 'value': 'median'},
                        {'label': 'Q75', 'value': 'Q75'},
                        {'label': 'Q90', 'value': 'Q90'},
                    ],
                    value='IQR',
                )

            
                
            ], style={
                        'width':'45%',
                        'margin-left':'10px',
                        'text-align':'center',
                        'display':'inline-block'}),
            
            html.Div([
                html.Label('Choix du match'),
            
                dcc.Dropdown(
                    id='matchs-dropdown',
                    options=[{'label': k, 'value': k} for k in sorted(df_quantiles_15_min.date_match.unique())],
                    value=list(sorted(df_quantiles_15_min.date_match.unique()))[0]),
                
                html.Label('Choix du joueur'),
                dcc.Dropdown(id='joueurs-dropdown'),
                
                # html.Div(id='output-nb-matchs'),
            ], style={
                        'width':'45%',
                        'margin-left':'10px',
                        'text-align':'center',
                        'display':'inline-block'}),
        ], style={}),
        
        
        dcc.Graph(figure={}, id='graph-content'),
        dcc.Graph(figure={}, id='graph-quantiles-MT'),
        
        ], style={
                    'width':'50%',
                    'text-align':'center',
                    'display':'block'}),
    

    # html.Hr(),
    html.Div([
        html.Div([
            html.Div([
                html.Div('Toulouse FC',
                         style={'font-size': '40px'}),
                
                html.Img(src='data:image/png;base64,{}'.format(encoded_logo.decode()),
                         style={'height': '90px',
                                'margin-left': '20px'})
            ], style={'position': 'absolute',
                      'top': '0', 'right': '0',
                      'width': '40%',
                      'display': 'flex',
                      'align-items': 'center',
                      'justify-content': 'flex-end',
                      'padding': '10px'}),
        ], style={'display': 'flex',
                  'flex-direction': 'row',
                  'width': '100%',
                  'height': '90px'}),
        html.Div([
            html.Div([
                html.Div(id='debut-MT-1',
                         style={
                             'text-align':'center',
                             'height':'50%',
                             'display':'block',
                             'align-items':'center'
                            }),
                html.Div(id='fin-MT-1',
                         style={
                             'text-align':'center',
                             'height':'50%',
                             'display':'block',
                             'align-items':'center'
                            }),
            ], style={
                        'backgroundColor':'#D0A2F5',
                        'color':'black',
                        'height':'100px',
                        'margin-left':'10px',
                        'margin-top': '10px',
                        'width':'45%',
                        'text-align':'center',
                        'display':'inline-block',
                    }),
            
            html.Div([
                html.Div(id='debut-MT-2',
                         style={
                             'text-align':'center',
                             'height':'50%',
                             'display':'block',
                             'align-items':'center'
                            }),
                html.Div(id='fin-MT-2',
                         style={
                             'text-align':'center',
                             'height':'50%',
                             'display':'block',
                             'align-items':'center'
                            }),
            ], style={
                        'backgroundColor':'#D0A2F5',
                        'color':'black',
                        'height':'100px',
                        'margin-left':'10px',
                        'margin-top': '10px',
                        'width':'45%',
                        'text-align':'center',
                        'display':'inline-block'
                        }),
        ], style={}),
    html.Br(),
    html.Div([
        html.Div([
            html.Label('Début de la fenêtre (en minutes)'),
            dcc.Input(id='my-input-starting-range',
                      type='number',),
        ], style={
                        'width':'45%',
                        'text-align':'center',
                        'display':'inline-block'
                        }),
        html.Div([
            html.Label('Fin de la fenêtre (en minutes)'),
            dcc.Input(id='my-input-ending-range',
                      type='number',),
        ], style={
                        'width':'45%',
                        'text-align':'center',
                        'display':'inline-block'
                        })
    ], style={}),
    
    html.Div(id='output-container-range'),
    html.Br(),
    
    # html.Div(id='output-IQR-fenetre'),
    # html.Br(),
    dcc.Graph(figure={}, id='graph-duree-matchs'),
    ], style={
                'width':'50%',
                'text-align':'center',
                'display':'block'}),
], style={'display': 'flex', 
          'flex-direction': 'row',
          'background-color': color_font,
        #   'background-image': "url('/assets/fond_appli.png')",
          "font-family": "Roboto, Helvetica"})

@app.callback(
    Output('joueurs-dropdown', 'options'),
    [Input('matchs-dropdown', 'value')])
def set_joueurs_options(selected_match):
    return [{'label': i, 'value': i} for i in sorted(df_quantiles_15_min.loc[df_quantiles_15_min.date_match == selected_match].id_joueur.unique())]

@app.callback(
    Output('joueurs-dropdown', 'value'),
    [Input('matchs-dropdown', 'value'),
     Input('joueurs-dropdown', 'value')]
)
def set_joueurs_value(selected_match, selected_joueur):
    joueurs_options = sorted(df_quantiles_15_min.loc[df_quantiles_15_min.date_match == selected_match].id_joueur.unique())
    if selected_joueur in joueurs_options:
        return selected_joueur
    else:
        return joueurs_options[0]

@app.callback(
    Output('variable-analyse-dropdown', 'options'),
    Input('variable-mesuree-dropdown', 'value')
)
def update_variable_analyse_options(variable_mesuree):
    if variable_mesuree == 'NormeGradAcc':
        options = [{'label': 'IQR', 'value': 'IQR'},
                   {'label': 'mean', 'value': 'mean'},
                   {'label': 'std', 'value': 'std'},
                   {'label': 'skewness', 'value': 'skewness'},
                   {'label': 'kurtosis', 'value': 'kurtosis'},
                   {'label': 'RMS', 'value': 'RMS'},
                   {'label': 'Q10', 'value': 'Q10'},
                   {'label': 'Q25', 'value': 'Q25'},
                   {'label': 'median', 'value': 'median'},
                   {'label': 'Q75', 'value': 'Q75'},
                   {'label': 'Q90', 'value': 'Q90'},
                   {'label': 'prop_sup_seuil', 'value': 'prop_sup_seuil'}]
    else:
        options = [{'label': 'IQR', 'value': 'IQR'},
                   {'label': 'mean', 'value': 'mean'},
                   {'label': 'std', 'value': 'std'},
                   {'label': 'skewness', 'value': 'skewness'},
                   {'label': 'kurtosis', 'value': 'kurtosis'},
                   {'label': 'RMS', 'value': 'RMS'},
                   {'label': 'Q10', 'value': 'Q10'},
                   {'label': 'Q25', 'value': 'Q25'},
                   {'label': 'median', 'value': 'median'},
                   {'label': 'Q75', 'value': 'Q75'},
                   {'label': 'Q90', 'value': 'Q90'}]
    return options


@app.callback(
    Output('graph-content', 'figure'),
    Input('matchs-dropdown', 'value'),
    Input('joueurs-dropdown', 'value'),
    Input('taille-fenetre-dropdown', 'value'),
    Input('variable-mesuree-dropdown', 'value'),
    Input('variable-analyse-dropdown','value')
)
def update_graph(match, joueur, taille_fenetre, var_mesuree, var_analyse):
    if taille_fenetre == '5':
        x_MT = 47.5
        df_quantiles_matchs = df_quantiles_5_min
    # elif taille_fenetre == '10':
    #     x_MT = 50
    #     df_quantiles_matchs = df_quantiles_10_min
    elif taille_fenetre == '15':
        x_MT = 52.5
        df_quantiles_matchs = df_quantiles_15_min
        
    df_quantiles_matchs = df_quantiles_matchs.loc[df_quantiles_matchs.colonne == var_mesuree].reset_index(drop=True)
    df_joueur_qt_melanges = df_quantiles_matchs.loc[df_quantiles_matchs.id_joueur==joueur].reset_index(drop=True)
    df_joueur = df_joueur_qt_melanges.copy()
    df_joueur.loc[df_joueur.moment == 'MT2', 'min_fin_fenetre'] += 45
    df_plot = df_joueur.loc[df_joueur.date_match != match].groupby('min_fin_fenetre').mean(numeric_only = True).reset_index()
    df_plot = df_plot.rename(columns={var_analyse: "moyenne"})
    df_plot['st_d'] = df_joueur.loc[df_joueur.date_match != match].groupby('min_fin_fenetre').std(numeric_only = True).reset_index()[var_analyse].to_numpy()

    df_plot['nb_points'] = df_joueur.loc[df_joueur.date_match != match].groupby('min_fin_fenetre').count()[var_analyse].to_numpy()

    df_plot = df_plot.merge(df_joueur.loc[df_joueur.date_match == match,['min_fin_fenetre', var_analyse]], on='min_fin_fenetre', how='outer')

    df_plot['borne_sup'] = 1.96*df_plot['st_d']/np.sqrt(df_plot['nb_points']) + df_plot['moyenne']
    df_plot['borne_inf'] = -1.96*df_plot['st_d']/np.sqrt(df_plot['nb_points']) + df_plot['moyenne']

    min_plot = df_plot[['borne_sup', 'borne_inf', var_analyse, 'moyenne']].min(skipna=True).min()
    max_plot = df_plot[['borne_sup', 'borne_inf', var_analyse, 'moyenne']].max(skipna=True).max()
    fig = go.Figure([
        go.Scatter(
            name=match,
            x=df_plot['min_fin_fenetre'],
            y=df_plot[var_analyse],
            mode='lines',
            line=dict(color='red'),
        ),
        go.Scatter(
            name='moyenne',
            x=df_plot['min_fin_fenetre'],
            y=df_plot['moyenne'],
            mode='lines',
            line=dict(color='rgb(31, 119, 180)'),
        ),
        go.Scatter(
            name='Upper Bound',
            x=df_plot['min_fin_fenetre'],
            y=df_plot['borne_sup'],
            mode='lines',
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False
        ),
        go.Scatter(
            name='Lower Bound',
            x=df_plot['min_fin_fenetre'],
            y=df_plot['borne_inf'],
            marker=dict(color="#444"),
            line=dict(width=0),
            mode='lines',
            fillcolor='rgba(68, 68, 68, 0.3)',
            fill='tonexty',
            showlegend=False
        ),
        go.Scatter(
        name='mi-temps',
        x=[x_MT, x_MT],
        y=[min_plot, max_plot],
        mode='lines',
        line=dict(dash='dash', width=1, color='gray'),
        showlegend=True
    )
    ])
    fig.update_layout(
        yaxis_title=var_analyse,
        xaxis_title='minute de fin de fenêtre',
        title='Comparaison '+var_analyse+' '+var_mesuree+' match vs moyenne habituelle',
        hovermode="x"
    )
    fig.update_layout({
        'plot_bgcolor': '#FFFFFF',
        'paper_bgcolor': color_font})
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#C3C3C3')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#C3C3C3')
    return fig

@app.callback(
    Output('output-container-range', 'children'),
    Input('my-input-starting-range', 'value'),
    Input('my-input-ending-range', 'value'))
def update_output(debut, fin):
    if debut is None or fin is None or fin <= debut:
        return 'Merci de choisir une fenêtre valide'
    else:
        return 'La fenêtre choisie est : ['+str(debut)+'-'+str(fin)+']'



@app.callback(
    Output('graph-duree-matchs', 'figure'),
    Input('joueurs-dropdown', 'value')
)
def graph_duree_matchs(joueur):
    df_joueur_k = pd.DataFrame()
    for match in sorted(df_instants_MT.match.unique()):
        try:
            mini_df = df_instants_MT.loc[(df_instants_MT.joueur == joueur)&(df_instants_MT.match == match)]
            duree = (mini_df.fin_MT_1.to_numpy() - mini_df.debut_MT_1.to_numpy())[0] + (mini_df.fin_MT_2.to_numpy() - mini_df.debut_MT_2.to_numpy())[0]
        except:
            duree = 0
        df_2 = pd.DataFrame({'match':[match], 'duree estimee':[duree]})
        df_joueur_k = pd.concat([df_joueur_k,df_2] , axis=0, ignore_index=True)
    fig = px.bar(df_joueur_k, x='match', y='duree estimee')
    fig.update_layout({
        'plot_bgcolor': '#FFFFFF',
        'paper_bgcolor': color_font})
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#C3C3C3')
    return fig


@app.callback(
    Output('graph-quantiles-MT', 'figure'),
    Input('joueurs-dropdown', 'value'),
    Input('taille-fenetre-dropdown', 'value'),
    Input('variable-mesuree-dropdown', 'value'),
    Input('variable-analyse-dropdown', 'value')
)
def graph_boxplots(joueur, taille_fenetre, var_mesuree, var_analyse):
    if taille_fenetre == '5':
        df_quantiles_matchs = df_quantiles_5_min
    # elif taille_fenetre == '10':
    #     df_quantiles_matchs = df_quantiles_10_min
    elif taille_fenetre == '15':
        df_quantiles_matchs = df_quantiles_15_min
    
    df_quantiles_matchs = df_quantiles_matchs.loc[df_quantiles_matchs.colonne == var_mesuree].reset_index(drop=True)
    df_boxplots = df_quantiles_matchs.loc[df_quantiles_matchs.id_joueur==joueur]
    fig = px.box(df_boxplots, x='min_fin_fenetre', y=var_analyse, color='moment')
    fig.update_layout({
        'plot_bgcolor': '#FFFFFF',
        'paper_bgcolor': color_font,
        'xaxis_title': 'minutes',
        'yaxis_title': var_analyse + ' ' + var_mesuree})
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#C3C3C3')
    return fig

@app.callback(
    Output('debut-MT-1', 'children'),
    Input('matchs-dropdown', 'value'),
    Input('joueurs-dropdown', 'value'))
def print_debut_MT_1(match, joueur):
    temps = df_instants_MT.loc[(df_instants_MT.joueur == joueur)&(df_instants_MT.match == match),'debut_MT_1']
    return 'début mi-temps 1 estimé : '+str(temps.to_numpy()[0])+' min'

@app.callback(
    Output('fin-MT-1', 'children'),
    Input('matchs-dropdown', 'value'),
    Input('joueurs-dropdown', 'value'))
def print_fin_MT_1(match, joueur):
    temps = df_instants_MT.loc[(df_instants_MT.joueur == joueur)&(df_instants_MT.match == match),'fin_MT_1']
    return 'fin mi-temps 1 estimé : '+str(temps.to_numpy()[0])+' min'

@app.callback(
    Output('debut-MT-2', 'children'),
    Input('matchs-dropdown', 'value'),
    Input('joueurs-dropdown', 'value'))
def print_debut_MT_2(match, joueur):
    temps = df_instants_MT.loc[(df_instants_MT.joueur == joueur)&(df_instants_MT.match == match),'debut_MT_2']
    return 'début mi-temps 2 estimé : '+str(temps.to_numpy()[0])+' min'

@app.callback(
    Output('fin-MT-2', 'children'),
    Input('matchs-dropdown', 'value'),
    Input('joueurs-dropdown', 'value'))
def print_fin_MT_1(match, joueur):
    temps = df_instants_MT.loc[(df_instants_MT.joueur == joueur)&(df_instants_MT.match == match),'fin_MT_2']
    return 'fin mi-temps 2 estimé : '+str(temps.to_numpy()[0])+' min'


# @app.callback(
#     Output('graph-pentes', 'figure'),
#     Input('matchs-dropdown', 'value'),
#     Input('joueurs-dropdown', 'value'),
#     Input('taille-fenetre-dropdown', 'value'),
#     Input('variable-mesuree-dropdown', 'value'),
#     Input('variable-analyse-dropdown','value')
# )
# def GraphePentes(match, joueur, taille_fenetre, var_mesuree, var_analyse):
#     if taille_fenetre == '5':
#         x_MT = 47.5
#         df_quantiles_matchs = df_quantiles_5_min
#     # elif taille_fenetre == '10':
#     #     x_MT = 50
#     #     df_quantiles_matchs = df_quantiles_10_min
#     elif taille_fenetre == '15':
#         x_MT = 52.5
#         df_quantiles_matchs = df_quantiles_15_min
        
#     df_quantiles_matchs = df_quantiles_matchs.loc[df_quantiles_matchs.colonne == var_mesuree].reset_index(drop=True)
#     df_joueur_qt_melanges = df_quantiles_matchs.loc[df_quantiles_matchs.id_joueur==joueur].reset_index(drop=True)
#     df_joueur = df_joueur_qt_melanges.copy()
#     df_joueur.loc[df_joueur.moment == 'MT2', 'min_fin_fenetre'] += 45
#     df_plot = df_joueur.loc[df_joueur.date_match != match].groupby('min_fin_fenetre').mean(numeric_only = True).reset_index()
#     df_plot = df_plot.rename(columns={var_analyse: "moyenne"})
#     df_plot['st_d'] = df_joueur.loc[df_joueur.date_match != match].groupby('min_fin_fenetre').std(numeric_only = True).reset_index()[var_analyse].to_numpy()

#     df_plot['nb_points'] = df_joueur.loc[df_joueur.date_match != match].groupby('min_fin_fenetre').count()[var_analyse].to_numpy()

#     df_plot = df_plot.merge(df_joueur.loc[df_joueur.date_match == match,['min_fin_fenetre', var_analyse]], on='min_fin_fenetre', how='outer')

#     df_plot['borne_sup'] = 1.96*df_plot['st_d']/np.sqrt(df_plot['nb_points']) + df_plot['moyenne']
#     df_plot['borne_inf'] = -1.96*df_plot['st_d']/np.sqrt(df_plot['nb_points']) + df_plot['moyenne']

#     min_plot = df_plot[['borne_sup', 'borne_inf', var_analyse, 'moyenne']].min(skipna=True).min()
#     max_plot = df_plot[['borne_sup', 'borne_inf', var_analyse, 'moyenne']].max(skipna=True).max()
#     fig = go.Figure([
#         go.Scatter(
#             name=match,
#             x=df_plot['min_fin_fenetre'],
#             y=df_plot[var_analyse],
#             mode='lines',
#             line=dict(color='red'),
#         ),
#         go.Scatter(
#             name='moyenne',
#             x=df_plot['min_fin_fenetre'],
#             y=df_plot['moyenne'],
#             mode='lines',
#             line=dict(color='rgb(31, 119, 180)'),
#         ),
#         go.Scatter(
#             name='Upper Bound',
#             x=df_plot['min_fin_fenetre'],
#             y=df_plot['borne_sup'],
#             mode='lines',
#             marker=dict(color="#444"),
#             line=dict(width=0),
#             showlegend=False
#         ),
#         go.Scatter(
#             name='Lower Bound',
#             x=df_plot['min_fin_fenetre'],
#             y=df_plot['borne_inf'],
#             marker=dict(color="#444"),
#             line=dict(width=0),
#             mode='lines',
#             fillcolor='rgba(68, 68, 68, 0.3)',
#             fill='tonexty',
#             showlegend=False
#         ),
#         go.Scatter(
#         name='mi-temps',
#         x=[x_MT, x_MT],
#         y=[min_plot, max_plot],
#         mode='lines',
#         line=dict(dash='dash', width=1, color='gray'),
#         showlegend=True
#     )
#     ])
#     fig.update_layout(
#         yaxis_title='IQR',
#         xaxis_title='minute de fin de fenêtre',
#         title='Comparaison '+var_analyse+' '+var_mesuree+' match vs moyenne habituelle',
#         hovermode="x"
#     )
#     fig.update_layout({
#         'plot_bgcolor': '#FFFFFF',
#         'paper_bgcolor': color_font})
#     fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#C3C3C3')
#     fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#C3C3C3')
#     return fig


if __name__ == '__main__':
    app.run_server(debug=True)
