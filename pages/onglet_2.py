from dash import Dash, html, dcc, Output, Input, dash_table, callback
import pandas as pd
import numpy as np
import base64

encoded_logo = base64.b64encode(open('data/logo.png', 'rb').read())

df_quantiles_5_min = pd.read_csv('data/df_infos_distributions_5min.csv')
df_quantiles_15_min = pd.read_csv('data/df_infos_distributions_15min.csv')

df_quantiles_5_min = df_quantiles_5_min.loc[((df_quantiles_5_min.min_fin_fenetre <= 45)|(df_quantiles_5_min.moment != 'MT1'))&(df_quantiles_5_min.min_fin_fenetre <= 45)].reset_index(drop=True)
df_quantiles_15_min = df_quantiles_15_min.loc[((df_quantiles_15_min.min_fin_fenetre <= 45)|(df_quantiles_15_min.moment != 'MT1'))&(df_quantiles_15_min.min_fin_fenetre <= 45)].reset_index(drop=True)

# Définir la couleur des cases du tableau 
def DefineStyleConditional(df, seuil_1, seuil_2, seuil_3, seuil_4, seuil_5):
    res = []
    for minute in df.columns:
        res.append({
            'if': {
                'filter_query': f'{{{minute}}} > {seuil_1}',
                'column_id': minute
            },
            'backgroundColor': 'green',
            'color': 'black'
        })
        res.append({
            'if': {
                'filter_query': f'{{{minute}}} > {seuil_2} && {{{minute}}} <= {seuil_1}',
                'column_id': minute
            },
            'backgroundColor': '#16DC40',
            'color': 'black'
        })
        res.append({
            'if': {
                'filter_query': f'{{{minute}}} > {seuil_3} && {{{minute}}} <= {seuil_2}',
                'column_id': minute
            },
            'backgroundColor': '#A4FE06',
            'color': 'black'
        })
        res.append({
            'if': {
                'filter_query': f'{{{minute}}} > {seuil_4} && {{{minute}}} <= {seuil_3}',
                'column_id': minute
            },
            'backgroundColor': '#FAFE06',
            'color': 'black'
        })
        res.append({
            'if': {
                'filter_query': f'{{{minute}}} > {seuil_5} && {{{minute}}} <= {seuil_4}',
                'column_id': minute
            },
            'backgroundColor': '#FFAC2C',
            'color': 'black'
        })
        res.append({
            'if': {
                'filter_query': f'{{{minute}}} < {seuil_5}',
                'column_id': minute
            },
            'backgroundColor': 'red',
            'color': 'black'
        })
        res.append({
            'if': {
                'filter_query': f'{{{minute}}} = ""',
                'column_id': minute
            },
            'backgroundColor': 'white',
            'color': 'black'
        })
    return res


# Ajouter le tableau à l'application Dash
color_font = '#F9F3FF'
layout = html.Div([
    html.Div([
        html.Div([
            html.H2("Menu :"),
            dcc.Link("Analyse distributionnelle", href='/onglet_1'),
            html.Br(),
            dcc.Link("Page d'accueil", href='/'),
            
        ], style={'display':'flex',
                  'flex-direction':'column',
                  'flex-grow':'1',
                  'text-align':'left',
                  'margin-left':'10px'}),
        
        html.H1('Dashboard', style={'flex-grow':'2'}),
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
        html.Div([
            html.Label('Taille des fenêtres (en minutes)'),
            dcc.Dropdown(
                    id='taille-fenetre-dropdown-dashboard',
                    options=['5','15'],
                    value='15',),
        ], style={
                'flex-grow':'1',
                'margin-left':'10px'
                }),
        html.Div([
            html.Label('Variable mesurée'),
            dcc.Dropdown(
                    id='variable-mesuree-dropdown-dashboard',
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
        ], style={
                'flex-grow':'1',
                'margin-left':'10px'
                }),
        html.Div([
            html.Label('Variable d\'analyse'),
            dcc.Dropdown(
                    id='variable-analyse-dropdown-dashboard',
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
                'flex-grow':'1',
                'margin-left':'10px'
                }),
             
        html.Div([
            html.Label('Date du match'),
            dcc.Dropdown(
            id='matchs-dropdown-dashboard',
            options=[{'label': k, 'value': k} for k in sorted(df_quantiles_15_min.date_match.unique())],
            value=list(sorted(df_quantiles_15_min.date_match.unique()))[0]
        ),
        ], style={
                'flex-grow':'1',
                'margin-left':'10px'
                }),
        
    ], style={
                'width':'100%',
                'display':'flex',
                'flex-direction': 'row'}),
    html.Br(),
    html.Br(),
    html.Div([    
        html.Div(id='tableau')
    ], style={
                'display':'block'}),
    html.Br(),
    html.Div([   
                html.Div([
                    html.Div([
                        html.Label('seuil 1 :'),
                        dcc.Input(id='seuil-1',
                      type='number',
                      value=25),
                    ], style={
                        'display':'flex',
                        'flex-direction':'row'
                        }),
                    html.Div([
                        html.Label('seuil 2 :'),
                        dcc.Input(id='seuil-2',
                      type='number',
                      value=10),
                    ], style={
                        'display':'flex',
                        'flex-direction':'row'
                        }),
                    html.Div([
                        html.Label('seuil 3 :'),
                        dcc.Input(id='seuil-3',
                      type='number',
                      value=0),
                    ], style={
                        'display':'flex',
                        'flex-direction':'row'
                        }),
                    html.Div([
                        html.Label('seuil 4 :'),
                        dcc.Input(id='seuil-4',
                      type='number',
                      value=-10),
                    ], style={
                        'display':'flex',
                        'flex-direction':'row'
                        }),
                    html.Div([
                        html.Label('seuil 5 :'),
                        dcc.Input(id='seuil-5',
                      type='number',
                      value=-25),
                    ], style={
                        'display':'flex',
                        'flex-direction':'row',
                        'margin-right':'20px'
                        }),
                 
        ], style={
                        'display':'flex',
                        'flex-direction':'column'
                        }),
               
               html.Div(id='tableau-exemple-couleurs'),
               html.Div(
            [
                html.P('Les valeurs à l\'intérieur du tableau représentent l\'écart en pourcentage par rapport à la moyenne.'+
                        ' Par exemple, un joueur ayant une valeur moyenne à 1 et une valeur à 1.2 pour le match sélectionné aura une valeur dans le tableau de 20.',
           ),
            ],
            style={
                "flex-grow": "1",
                "width": "40%",
                "margin": "0 auto",  # Pour centrer horizontalement le texte
                "text-align": "center",  # Pour centrer verticalement le texte
            },
        ),
               
    ], style={"flex-grow": "1", "display": "flex", "flex-direction": "row", "align-items": "center",
                'margin-left':'10px'}),
    
], style={'display': 'flex', 
          'flex-direction': 'column',
          'background-color': color_font,
          "font-family": "Roboto, Helvetica",
          'text-align':'center',})


@callback(
    Output('variable-analyse-dropdown-dashboard', 'options'),
    Input('variable-mesuree-dropdown-dashboard', 'value')
)
def update_variable_analyse_options(variable_mesuree):
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
    if variable_mesuree == 'NormeGradAcc':
        options = [{'label': 'prop_sup_seuil', 'value': 'prop_sup_seuil'}] + options
    return options


@callback(
    Output('tableau', 'children'),
    Input('matchs-dropdown-dashboard', 'value'),
    Input('taille-fenetre-dropdown-dashboard', 'value'),
    Input('variable-mesuree-dropdown-dashboard', 'value'),
    Input('variable-analyse-dropdown-dashboard','value'),
    Input('seuil-1', 'value'),
    Input('seuil-2', 'value'),
    Input('seuil-3', 'value'),
    Input('seuil-4', 'value'),
    Input('seuil-5', 'value')
)
def UpdateTable(selected_match, taille_fenetre, var_mesuree, var_analyse, seuil_1, seuil_2, seuil_3, seuil_4, seuil_5):
    if taille_fenetre == '5':
        x_MT = 47.5
        df_quantiles_matchs = df_quantiles_5_min.copy()
    elif taille_fenetre == '15':
        x_MT = 52.5
        df_quantiles_matchs = df_quantiles_15_min.copy()
    
    df_quantiles_matchs.loc[df_quantiles_matchs.moment=='MT2','min_fin_fenetre'] += 45
    df = df_quantiles_matchs.loc[(df_quantiles_matchs.date_match==selected_match)&(df_quantiles_matchs.colonne == var_mesuree)].copy().reset_index(drop=True)
    
    df = df.loc[:, df.columns.isin(['id_joueur','date_match','min_fin_fenetre',var_analyse])]
    
    df_moyennes = df_quantiles_matchs.loc[(df_quantiles_matchs.date_match!=selected_match)&
                                          (df_quantiles_matchs.colonne == var_mesuree)].copy().reset_index(drop=True).groupby(['id_joueur','min_fin_fenetre']).mean(numeric_only=True).reset_index().rename(columns={var_analyse:'moyenne'})
    df = df.merge(df_moyennes)
    
    
    id_joueurs = sorted(df.id_joueur.unique())
    min_fin_fenetres = sorted(df.min_fin_fenetre.unique())

    table_data = np.empty((len(id_joueurs), len(min_fin_fenetres)), dtype=object)
    for i, joueur in enumerate(df.id_joueur.unique()):
        for j, min_fin_fenetre in enumerate(sorted(df.min_fin_fenetre.unique())):
            joueur_data = df.loc[(df.date_match==selected_match) & (df.id_joueur == joueur) & (df.min_fin_fenetre == min_fin_fenetre), var_analyse]
            joueur_moyenne = df.loc[(df.date_match==selected_match) & (df.id_joueur == joueur) & (df.min_fin_fenetre == min_fin_fenetre), 'moyenne']
            
            
            if len(joueur_moyenne.to_numpy()) > 0 and len(joueur_data.to_numpy()) > 0:
                table_data[i, j] = np.round(100*(joueur_data.to_numpy()[0]-joueur_moyenne.to_numpy()[0])/joueur_moyenne.to_numpy()[0],2)
            else :
                   table_data[i, j] = ""  
                          
    noms_min_fin_fenetres = ['minute_'+ str(min_fin_fenetre) for min_fin_fenetre in min_fin_fenetres]
    df_table = pd.DataFrame(table_data, columns=noms_min_fin_fenetres, index=id_joueurs)
    style_data = DefineStyleConditional(df_table, seuil_1, seuil_2, seuil_3, seuil_4, seuil_5)
    df_table.insert(0, "id_joueur", id_joueurs)
    return dash_table.DataTable(
        columns=[{'name': str(column), 'id': str(column)} for column in df_table.columns],
        data=df_table.to_dict('records'),
        editable=True,
    style_data_conditional=style_data
    )


@callback(
    Output('seuil-1', 'value'),
    Output('seuil-2', 'value'),
    Output('seuil-3', 'value'),
    Output('seuil-4', 'value'),
    Output('seuil-5', 'value'),
    Input('seuil-1', 'value'),
    Input('seuil-2', 'value'),
    Input('seuil-3', 'value'),
    Input('seuil-4', 'value'),
    Input('seuil-5', 'value'))
def update_seuils(seuil_1, seuil_2, seuil_3, seuil_4, seuil_5):
    liste_seuils = [seuil_1, seuil_2, seuil_3, seuil_4, seuil_5]
    for k in range(0,4):
        if liste_seuils[k] < liste_seuils[k+1]:
            liste_seuils[k+1], liste_seuils[k] = liste_seuils[k], liste_seuils[k+1]
    return liste_seuils

@callback(
    Output('tableau-exemple-couleurs', 'children'),
    Input('seuil-1', 'value'),
    Input('seuil-2', 'value'),
    Input('seuil-3', 'value'),
    Input('seuil-4', 'value'),
    Input('seuil-5', 'value'))
def DefineStyleConditionalExemple(seuil_1, seuil_2, seuil_3, seuil_4, seuil_5):
    df_correspondances_couleurs = pd.DataFrame({'Correspondance des couleurs':["augmentation supérieure à "+str(seuil_1)+"%",
                                                                                "augmentation entre "+str(seuil_2)+" et "+str(seuil_1)+"%",
                                                                                "augmentation entre "+str(seuil_3)+" et "+str(seuil_2)+"%",
                                                                                "diminution de "+str(seuil_4)+" à "+str(seuil_3)+"%",
                                                                                "diminution de "+str(seuil_5)+" à "+str(seuil_4)+"%",
                                                                                "diminution supérieure à "+str(seuil_5)+"%",
                                                                                "Pas de données"]})
    res = []
    for colonne in df_correspondances_couleurs.columns:
        res.append({
            'if': {
                'filter_query': f'{{{colonne}}} = "augmentation supérieure à {str(seuil_1)}%"',
                'column_id': colonne
            },
            'backgroundColor': 'green',
            'color': 'black'
        })
        res.append({
            'if': {
                'filter_query': f'{{{colonne}}}  = "augmentation entre {str(seuil_2)} et {str(seuil_1)}%"',
                'column_id': colonne
            },
            'backgroundColor': '#16DC40',
            'color': 'black'
        })
        res.append({
            'if': {
                'filter_query': f'{{{colonne}}}  = "augmentation entre {str(seuil_3)} et {str(seuil_2)}%"',
                'column_id': colonne
            },
            'backgroundColor': '#A4FE06',
            'color': 'black'
        })
        res.append({
            'if': {
                'filter_query': f'{{{colonne}}}  = "diminution de {str(seuil_4)} à {str(seuil_3)}%"',
                'column_id': colonne
            },
            'backgroundColor': '#FAFE06',
            'color': 'black'
        })
        res.append({
            'if': {
                'filter_query': f'{{{colonne}}} = "diminution de {str(seuil_5)} à {str(seuil_4)}%"',
                'column_id': colonne
            },
            'backgroundColor': '#FFAC2C',
            'color': 'black'
        })
        res.append({
            'if': {
                'filter_query': f'{{{colonne}}} = "diminution supérieure à {str(seuil_5)}%"',
                'column_id': colonne
            },
            'backgroundColor': 'red',
            'color': 'black'
        })
        res.append({
            'if': {
                'filter_query': f'{{{colonne}}} = "Pas de données"',
                'column_id': colonne
            },
            'backgroundColor': 'white',
            'color': 'black'
        })
    return dash_table.DataTable(
                    columns=[{'name': str(column), 'id': str(column)} for column in df_correspondances_couleurs.columns],
                    data=df_correspondances_couleurs.to_dict('records'),
                    editable=True,
                    style_data_conditional=res
            ) 
