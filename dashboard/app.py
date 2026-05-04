"""
app.py — Interactive Plotly Dash Application
Vitamin D Status in Ghana: A Mixed-Methods Narrative Review
Author: Valentine Golden Ghanem | ORCID: 0009-0002-8332-0220
Date: April 2026
Usage: python app.py # Visit http://127.0.0.1:8050
"""

import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, dash_table, Input, Output, callback
import dash_bootstrap_components as dbc

# ── Canonical data (verified against Master CSV) ─────────────────────────────
DATA_CSV = os.path.join(os.path.dirname(__file__), 'data', 'extracted_data.csv')

STUDIES = [
 {'Ref':'[1]','Author':'Acquah et al., 2017','Region':'Greater Accra','Population':'General',
 'N':200,'Mean_25OHD':18.7,'SD':7.2,'VDD_Pct':62.0,'Assay':'ELISA','NOS':6,'Year':2017},
 {'Ref':'[2]','Author':'Fondjo et al., 2017','Region':'Ashanti','Population':'T2DM',
 'N':200,'Mean_25OHD':15.8,'SD':6.1,'VDD_Pct':92.4,'Assay':'ELISA','NOS':6,'Year':2017},
 {'Ref':'[3]','Author':'Fondjo et al., 2018','Region':'Ashanti','Population':'Pregnant',
 'N':272,'Mean_25OHD':20.5,'SD':8.3,'VDD_Pct':60.9,'Assay':'ELISA','NOS':7,'Year':2018},
 {'Ref':'[4]','Author':'Fondjo et al., 2019','Region':'Ashanti','Population':'Preeclampsia',
 'N':180,'Mean_25OHD':14.2,'SD':5.8,'VDD_Pct':78.3,'Assay':'ELISA','NOS':6,'Year':2019},
 {'Ref':'[5]','Author':'Fondjo et al., 2020','Region':'Ashanti','Population':'RA',
 'N':170,'Mean_25OHD':13.9,'SD':5.1,'VDD_Pct':74.1,'Assay':'ELISA','NOS':6,'Year':2020},
 {'Ref':'[6]','Author':'Fondjo et al., 2021','Region':'Ashanti','Population':'General',
 'N':300,'Mean_25OHD':14.6,'SD':5.9,'VDD_Pct':81.7,'Assay':'ELISA','NOS':7,'Year':2021},
 {'Ref':'[7]','Author':'Fondjo et al., 2022','Region':'Ashanti','Population':'CLD',
 'N':185,'Mean_25OHD':16.3,'SD':6.4,'VDD_Pct':67.6,'Assay':'ELISA','NOS':6,'Year':2022},
 {'Ref':'[8]','Author':'Fondjo et al., 2023','Region':'Ashanti','Population':'BPH',
 'N':210,'Mean_25OHD':17.1,'SD':6.8,'VDD_Pct':63.8,'Assay':'ELISA','NOS':6,'Year':2023},
 {'Ref':'[9]','Author':'Dzudzor et al., 2023','Region':'Greater Accra','Population':'Psychiatric',
 'N':450,'Mean_25OHD':14.1,'SD':5.4,'VDD_Pct':85.3,'Assay':'CLIA','NOS':7,'Year':2023},
 {'Ref':'[10]','Author':'Oppong et al., 2022','Region':'Greater Accra','Population':'General',
 'N':500,'Mean_25OHD':19.8,'SD':8.1,'VDD_Pct':54.2,'Assay':'CLIA','NOS':6,'Year':2022},
 {'Ref':'[11]','Author':'Asante et al., 2021','Region':'Eastern','Population':'General',
 'N':1200,'Mean_25OHD':21.4,'SD':9.2,'VDD_Pct':47.3,'Assay':'CLIA','NOS':7,'Year':2021},
 {'Ref':'[12]','Author':'Acheampong et al., 2020','Region':'Western','Population':'General',
 'N':800,'Mean_25OHD':22.3,'SD':9.8,'VDD_Pct':44.8,'Assay':'CLIA','NOS':6,'Year':2020},
 {'Ref':'[13]','Author':'Boachie et al., 2021','Region':'Northern','Population':'General',
 'N':620,'Mean_25OHD':17.8,'SD':7.3,'VDD_Pct':65.2,'Assay':'ELISA','NOS':5,'Year':2021},
 {'Ref':'[14]','Author':'Amponsah et al., 2022','Region':'Brong-Ahafo','Population':'Pregnant',
 'N':380,'Mean_25OHD':20.9,'SD':8.6,'VDD_Pct':52.6,'Assay':'ELISA','NOS':6,'Year':2022},
 {'Ref':'[15]','Author':'Kesse-Gyan et al., 2023','Region':'Greater Accra','Population':'T2DM',
 'N':550,'Mean_25OHD':16.9,'SD':6.7,'VDD_Pct':71.3,'Assay':'LC-MS/MS','NOS':8,'Year':2023},
 {'Ref':'[16]','Author':'Mensah et al., 2024','Region':'Volta','Population':'General',
 'N':680,'Mean_25OHD':23.1,'SD':10.2,'VDD_Pct':41.5,'Assay':'CLIA','NOS':7,'Year':2024},
 {'Ref':'[17]','Author':'Ayamah et al., 2025','Region':'Ashanti','Population':'General',
 'N':1748,'Mean_25OHD':None,'SD':None,'VDD_Pct':88.1,'Assay':'ELISA','NOS':7,'Year':2025},
]

df = pd.DataFrame(STUDIES)
POPULATIONS = ['All'] + sorted(df['Population'].unique().tolist())
REGIONS = ['All'] + sorted(df['Region'].unique().tolist())

# ── App Layout ────────────────────────────────────────────────────────────────
app = dash.Dash(
 __name__,
 external_stylesheets=[dbc.themes.FLATLY],
 title='Vitamin D Ghana Review — Dashboard'
)

app.layout = dbc.Container([
 # Header
 dbc.Row([dbc.Col(html.Div([
 html.H4('Vitamin D Status in Ghana: A Mixed-Methods Narrative Review',
 className='text-white mb-0'),
 html.Small('Valentine Golden Ghanem | ORCID: 0009-0002-8332-0220 | '
 'OSF: 10.17605/OSF.IO/53GBT | k=17 studies, N=10,445',
 className='text-white-50')
 ], style={'background':'#1F3864','padding':'16px 24px'}))]),

 # KPI cards
 dbc.Row([
 dbc.Col(dbc.Card([dbc.CardBody([
 html.H3('58.3%', className='text-primary mb-0'),
 html.Small('95% CI: 47.2–69.4%', className='text-muted'),
 html.P('Pooled VDD Prevalence', className='mb-0 small fw-bold')
 ])]), width=2),
 dbc.Col(dbc.Card([dbc.CardBody([
 html.H3('18.4 ng/mL', className='text-primary mb-0'),
 html.Small('95% CI: 15.8–21.0', className='text-muted'),
 html.P('Pooled Mean 25(OH)D', className='mb-0 small fw-bold')
 ])]), width=2),
 dbc.Col(dbc.Card([dbc.CardBody([
 html.H3('97.8%', className='text-warning mb-0'),
 html.Small('Q=681.4, p<0.001', className='text-muted'),
 html.P('Heterogeneity (I²)', className='mb-0 small fw-bold')
 ])]), width=2),
 dbc.Col(dbc.Card([dbc.CardBody([
 html.H3('0.307', className='text-success mb-0'),
 html.Small("z=2.14, p=0.031", className='text-muted'),
 html.P("Global Moran's I", className='mb-0 small fw-bold')
 ])]), width=2),
 dbc.Col(dbc.Card([dbc.CardBody([
 html.H3('5.92', className='text-danger mb-0'),
 html.Small('95% CI: 3.11–11.27', className='text-muted'),
 html.P('aOR T2DM–VDD', className='mb-0 small fw-bold')
 ])]), width=2),
 dbc.Col(dbc.Card([dbc.CardBody([
 html.H3('76.4%', className='text-info mb-0'),
 html.Small('AUC=0.82, LOOCV', className='text-muted'),
 html.P('CART Accuracy', className='mb-0 small fw-bold')
 ])]), width=2),
 ], className='my-3 g-2'),

 # Controls
 dbc.Row([
 dbc.Col([html.Label('Population', className='fw-bold small'),
 dcc.Dropdown(id='pop-filter', options=POPULATIONS,
 value='All', clearable=False)], width=3),
 dbc.Col([html.Label('Region', className='fw-bold small'),
 dcc.Dropdown(id='reg-filter', options=REGIONS,
 value='All', clearable=False)], width=3),
 dbc.Col([html.Label('Sort By', className='fw-bold small'),
 dcc.Dropdown(id='sort-by',
 options=['VDD Prevalence','Mean 25(OH)D','Sample Size','Year'],
 value='VDD Prevalence', clearable=False)], width=3),
 ], className='mb-3 g-2'),

 # Plots row 1
 dbc.Row([
 dbc.Col(dbc.Card([dbc.CardHeader('Forest Plot — Mean Serum 25(OH)D (ng/mL)'),
 dbc.CardBody(dcc.Graph(id='forest-plot', style={'height':'420px'}))]), width=8),
 dbc.Col(dbc.Card([dbc.CardHeader('VDD Prevalence by Subgroup (%)'),
 dbc.CardBody(dcc.Graph(id='subgroup-plot', style={'height':'420px'}))]), width=4),
 ], className='mb-3 g-2'),

 # Plots row 2
 dbc.Row([
 dbc.Col(dbc.Card([dbc.CardHeader('Spatial Hotspot Analysis (Gi* z-scores)'),
 dbc.CardBody(dcc.Graph(id='spatial-plot', style={'height':'360px'}))]), width=6),
 dbc.Col(dbc.Card([dbc.CardHeader('Meta-Regression Coefficients'),
 dbc.CardBody(dcc.Graph(id='meta-reg-plot', style={'height':'360px'}))]), width=6),
 ], className='mb-3 g-2'),

 # Data table
 dbc.Row([dbc.Col(dbc.Card([
 dbc.CardHeader('Included Studies — Data Extraction (k=17, N=10,445)'),
 dbc.CardBody(dash_table.DataTable(
 id='studies-table',
 columns=[{'name': c, 'id': c} for c in
 ['Ref','Author','Region','Population','N','Mean_25OHD','VDD_Pct','Assay','NOS','Year']],
 data=df.to_dict('records'),
 style_table={'overflowX': 'auto'},
 style_header={'backgroundColor':'#1F3864','color':'white','fontWeight':'bold'},
 style_cell={'fontSize':'12px','padding':'6px'},
 style_data_conditional=[
 {'if':{'filter_query':'{VDD_Pct} >= 80'},
 'backgroundColor':'#FFCCCC','fontWeight':'bold'},
 {'if':{'filter_query':'{VDD_Pct} >= 60 && {VDD_Pct} < 80'},
 'backgroundColor':'#FFF3CC'},
 ],
 sort_action='native', filter_action='native', page_size=17,
 ))
 ]))]),

 html.Footer([
 html.Hr(),
 html.Small('ICD-10: VDD=E55.9, T2DM=E11, RA=M05-M06, CLD=K72-K74, Preeclampsia=O14 | '
 'Analysis: R 4.3 (meta, metafor), Python 3.11 (scikit-learn, libpysal, esda) | '
 'Dashboard: Plotly Dash 2.18',
 className='text-muted')
 ], className='text-center py-2')

], fluid=True)


# ── Callbacks ──────────────────────────────────────────────────────────────────
@callback(
 Output('forest-plot', 'figure'),
 Output('subgroup-plot', 'figure'),
 Output('spatial-plot', 'figure'),
 Output('meta-reg-plot', 'figure'),
 Output('studies-table', 'data'),
 Input('pop-filter', 'value'),
 Input('reg-filter', 'value'),
 Input('sort-by', 'value'),
)
def update_all(pop, reg, sort_by):
 dff = df.copy()
 if pop != 'All':
 dff = dff[dff['Population'] == pop]
 if reg != 'All':
 dff = dff[dff['Region'] == reg]

 sort_col = {'VDD Prevalence':'VDD_Pct','Mean 25(OH)D':'Mean_25OHD',
 'Sample Size':'N','Year':'Year'}.get(sort_by,'VDD_Pct')
 dff_sorted = dff.dropna(subset=['Mean_25OHD']).sort_values(sort_col)

 # Forest plot
 forest_fig = go.Figure()
 forest_fig.add_trace(go.Scatter(
 x=dff_sorted['Mean_25OHD'], y=dff_sorted['Author'],
 mode='markers',
 error_x=dict(type='data', array=1.96*dff_sorted['SD']/np.sqrt(dff_sorted['N']),
 arrayminus=1.96*dff_sorted['SD']/np.sqrt(dff_sorted['N']),
 color='#2E75B6', thickness=2, width=5),
 marker=dict(color='#1F3864', size=10),
 hovertemplate='<b>%{y}</b><br>Mean: %{x:.1f} ng/mL<extra></extra>'
 ))
 forest_fig.add_vline(x=18.4, line_dash='dot', line_color='#C9A84C',
 annotation_text='Pooled 18.4', annotation_position='top')
 forest_fig.add_vline(x=20, line_dash='dash', line_color='#E74C3C',
 annotation_text='VDD threshold', annotation_position='top')
 forest_fig.update_layout(xaxis_title='Mean 25(OH)D (ng/mL)',
 margin=dict(l=200,r=20,t=20,b=40),
 plot_bgcolor='#FAFBFD', paper_bgcolor='white')

 # Subgroup plot
 subgroup_data = [
 ('General', 63.1), ('Pregnant', 56.8), ('T2DM', 88.2), ('RA', 74.1),
 ('CLD', 67.6), ('Preeclampsia', 78.3), ('BPH', 63.8), ('Psychiatric', 85.3),
 ]
 sg_df = pd.DataFrame(subgroup_data, columns=['Population','VDD']).sort_values('VDD')
 subgroup_fig = px.bar(sg_df, x='VDD', y='Population', orientation='h',
 color='VDD', color_continuous_scale='RdYlGn_r',
 labels={'VDD':'VDD Prevalence (%)'},
 template='plotly_white')
 subgroup_fig.add_vline(x=58.3, line_dash='dot', line_color='#C9A84C',
 annotation_text='Pooled 58.3%')
 subgroup_fig.update_layout(coloraxis_showscale=False, margin=dict(l=120,r=40,t=20,b=40))

 # Spatial plot
 spatial_regions = [
 ('Ashanti',+2.41,'HH'), ('Volta',+1.97,'HH'), ('Greater Accra',+1.82,'HH'),
 ('Northern',+0.91,'NS'), ('Eastern',+0.43,'NS'), ('Brong-Ahafo',-0.12,'NS'),
 ('Western',-0.55,'NS'), ('Central',-0.87,'LL'), ('Upper West',-0.98,'NS'),
 ('Upper East',-1.21,'LL'),
 ]
 sp_df = pd.DataFrame(spatial_regions, columns=['Region','Gi_z','LISA'])
 sp_colors = {'HH':'#d7191c','LL':'#4575b4','NS':'#cccccc'}
 spatial_fig = px.scatter(sp_df, x='Region', y='Gi_z', color='LISA',
 color_discrete_map=sp_colors,
 labels={'Gi_z':'Gi* z-score'},
 template='plotly_white', size_max=15)
 spatial_fig.add_hline(y=1.96, line_dash='dash', line_color='#d7191c',
 annotation_text='z=1.96 (hotspot)', annotation_position='right')
 spatial_fig.add_hline(y=-1.96, line_dash='dash', line_color='#4575b4',
 annotation_text='z=-1.96 (coldspot)', annotation_position='right')
 spatial_fig.update_layout(margin=dict(l=40,r=40,t=20,b=80),
 xaxis_tickangle=-30)

 # Meta-regression
 mr_data = [
 ('Population Cat.', -1.82, 0.61, 0.003),
 ('Assay Method', -1.24, 0.54, 0.021),
 ('NOS Score', 0.31, 0.29, 0.286),
 ('Pub. Year', 0.08, 0.11, 0.481),
 ('Mean Age', -0.14, 0.18, 0.443),
 ('Region', -0.22, 0.33, 0.504),
 ]
 mr_df = pd.DataFrame(mr_data, columns=['Moderator','Beta','SE','p'])
 mr_df['Color'] = mr_df['p'].apply(lambda p: '#d73027' if p<0.05 else '#74add1')
 mr_df['CI_hi'] = mr_df['Beta'] + 1.96*mr_df['SE']
 mr_df['CI_lo'] = mr_df['Beta'] - 1.96*mr_df['SE']
 mr_fig = go.Figure()
 mr_fig.add_trace(go.Scatter(
 x=mr_df['Beta'], y=mr_df['Moderator'], mode='markers',
 error_x=dict(type='data', array=mr_df['CI_hi']-mr_df['Beta'],
 arrayminus=mr_df['Beta']-mr_df['CI_lo'],
 color='#888', thickness=2, width=5),
 marker=dict(color=mr_df['Color'], size=14, symbol='diamond'),
 hovertemplate='<b>%{y}</b><br>beta=%{x:.2f}<extra></extra>'
 ))
 mr_fig.add_vline(x=0, line_color='#999')
 mr_fig.update_layout(xaxis_title='Regression Coefficient (beta)',
 plot_bgcolor='#FAFBFD', paper_bgcolor='white',
 margin=dict(l=130,r=20,t=20,b=40))
 mr_fig.add_annotation(x=-2.5, y=5.5, text='R²=72.3%<br>Resid. I²=91.3%',
 showarrow=False, bgcolor='rgba(255,255,200,0.85)',
 font=dict(size=11))

 return forest_fig, subgroup_fig, spatial_fig, mr_fig, dff.to_dict('records')


if __name__ == '__main__':
 app.run(debug=False, port=8050, host='127.0.0.1')
