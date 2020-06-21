import sys

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as offline

valid_columns = ['FACET','PRINCIPLE','INDICATOR_ID','PRIORITY','METRIC','SCORE']

ceroColor = '#F6F6F6'
oneColor = '#D6D6D6'
twoColor = '#B6B6B6'
threeColor = '#969696'
fourColor = '#868686'
fiveColor = '#6E6E6E'
colors = [ceroColor,oneColor,twoColor,threeColor,fourColor,fiveColor]

ceroMaturityColor = 'grey'
oneMaturityColor = 'lightgoldenrodyellow'
twoMaturityColor = 'khaki'
threeMaturityColor = 'darkseagreen'
fourMaturityColor = 'darkolivegreen'

def get_level(df, facet):
    d = df[df['FACET'] == facet]

    def get_statistics(df, facet):
        df = df[['PRIORITY', 'SCORE']].groupby('PRIORITY').agg({'count', 'sum'})
        df.columns = df.columns.droplevel(0)
        df = df.reset_index()
        df['meets_50'] = df.apply(lambda x: x['sum'] >= x['count'] * 0.5, axis=1)
        df['meets_100'] = df.apply(lambda x: x['sum'] == x['count'], axis=1)
        return df

    d = get_statistics(d, facet)

    level = 0
    if 'Essential' in d['PRIORITY'].unique() and d.loc[d['PRIORITY'] == 'Essential', 'meets_100'].values[0] == False:
        return level
    else:
        level += 1
    if 'Important' in d['PRIORITY'].unique() and d.loc[d['PRIORITY'] == 'Important', 'meets_50'].values[0] == False:
        return level
    else:
        level += 1
    if 'Important' in d['PRIORITY'].unique() and d.loc[d['PRIORITY'] == 'Important', 'meets_100'].values[0] == False:
        return level
    else:
        level += 1
    if 'Useful' in d['PRIORITY'].unique() and d.loc[d['PRIORITY'] == 'Useful', 'meets_50'].values[0] == False:
        return level
    else:
        level += 1
    if 'Useful' in d['PRIORITY'].unique() and d.loc[d['PRIORITY'] == 'Useful', 'meets_100'].values[0] == False:
        return level
    else:
        level += 1
    return level


def get_level_table():
    fill_color = [colors]
    fig_table_levels = go.Figure(data=[
        go.Table(columnwidth=[50, 200], header=dict(height=0, fill_color='white', font_size=1), cells=dict(
            values=[['Level 0', 'Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5'],
                    ['<b>Not FAIR</b>', '<b>FAIR essential criteria only</b>',
                     '<b>FAIR essential criteria + 50 % of important criteria</b>',
                     '<b>FAIR essential criteria + 100 % of important criteria</b>',
                     '<b>FAIR essential criteria + 100 % of important criteria + 50 % of useful criteria</b>',
                     '<b>FAIR essential criteria + 100 % of important criteria + 100 % of useful criteria</b>']],
            height=25, font_size=12, fill_color=fill_color))])
    fig_table_levels.update_layout(title="Level of your digital object")
    return fig_table_levels

def get_maturity_level_table():
    fill_color=[[ceroMaturityColor, oneMaturityColor,twoMaturityColor,threeMaturityColor,fourMaturityColor]]
    fig_table = go.Figure(data=[go.Table(columnwidth=[50, 200], header=dict(height=0, fill_color='white', font_size=1),
                                         cells=dict(values=[[0, 1, 2, 3, 4], ['<b>Not applicable</b>',
                                                                              '<b>Not being considered this yet</b>',
                                                                              '<b>Under consideration or in planning phase</b>',
                                                                              '<b>In implementation phase</b>',
                                                                              '<b>Fully implemented</b>']], height=25,
                                                    font_size=12, fill_color=
                                                 fill_color))])
    fig_table.update_layout(title="Maturity level per indicator (per FAIR area)")
    return fig_table

def get_fair_level_plot(df,facets):
    levels = [get_level(df, facet) + 0.25 for facet in facets]
    fig_levels = go.Figure()
    fig_levels.add_trace(go.Bar(x=facets, y=levels, width=[0.4, 0.4, 0.4, 0.4], marker_color='darkblue'))
    fig_levels.add_shape(type="rect", x0=-0.5, y0=0, x1=3.5, y1=0.5, layer="below", fillcolor=colors[0],
                         line=dict(color='rgba(0,0,0,0)', width=1))
    fig_levels.add_shape(type="rect", x0=-0.5, y0=0.5, x1=3.5, y1=1.5, layer="below", fillcolor=colors[1],
                         line=dict(color='rgba(0,0,0,0)', width=1))
    fig_levels.add_shape(type="rect", x0=-0.5, y0=1.5, x1=3.5, y1=2.5, layer="below", fillcolor=colors[2],
                         line=dict(color='rgba(0,0,0,0)', width=1))
    fig_levels.add_shape(type="rect", x0=-0.5, y0=2.5, x1=3.5, y1=3.5, layer="below", fillcolor=colors[3],
                         line=dict(color='rgba(0,0,0,0)', width=1))
    fig_levels.add_shape(type="rect", x0=-0.5, y0=3.5, x1=3.5, y1=4.5, layer="below", fillcolor=colors[4],
                         line=dict(color='rgba(0,0,0,0)', width=1))
    fig_levels.add_shape(type="rect", x0=-0.5, y0=4.5, x1=3.5, y1=5.5, layer="below", fillcolor=colors[5],
                         line=dict(color='rgba(0,0,0,0)', width=1))

    fig_levels.update_layout(title="FAIRNESS LEVELS PER AREA", yaxis=dict(showgrid=False), yaxis_title="Level",
                             paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig_levels

def get_radar_plot(df,facets):
    num_cols = 2
    num_rows = int(np.ceil(len(facets) / 2))
    fig_radar = make_subplots(rows=num_rows, cols=2, specs=[[{'type': 'polar'}] * 2] * num_rows,
                              subplot_titles=tuple(facets), vertical_spacing=0.1, horizontal_spacing=0.3)
    facet_index = 0
    for i in range(num_rows):
        for j in range(num_cols):
            facet = facets[facet_index]
            df_temp = df[df['FACET'] == facet]
            fig_radar.add_trace(go.Scatterpolar(name=facet, r=df_temp.METRIC, theta=df_temp.INDICATOR_ID, mode='lines'),
                                i + 1, j + 1)
            facet_index += 1
    fig_radar.update_traces(fill='toself')
    fig_radar.update_layout(height=1000, width=1000, showlegend=False,
                            polar=dict(
                                radialaxis=dict(range=[0, 4], showticklabels=True, tickvals=list([0, 1, 2, 3, 4]))),
                            polar2=dict(
                                radialaxis=dict(range=[0, 4], showticklabels=True, tickvals=list([0, 1, 2, 3, 4]))),
                            polar3=dict(
                                radialaxis=dict(range=[0, 4], showticklabels=True, tickvals=list([0, 1, 2, 3, 4]))),
                            polar4=dict(
                                radialaxis=dict(range=[0, 4], showticklabels=True, tickvals=list([0, 1, 2, 3, 4]))))
    for i in range(len(facets)):
        fig_radar.layout.annotations[i].update(y=fig_radar.layout.annotations[i].y + 0.025)

    return fig_radar


def is_valid(file):
    df = pd.read_csv(file)
    for c in valid_columns:
        if c not in df.columns:
            return False
    return True

def main():
    sa = sys.argv
    if 'main.py' in sys.argv[0]:
        file = './data/FAIR_evaluation_out.csv'
    else:
        file = sys.argv[1:]
    if is_valid(file):
        df = pd.read_csv(file)
        facets = df['FACET'].unique()
        fig_table_levels = get_level_table()
        fig_fair_levels = get_fair_level_plot(df,facets)
        fig_maturity_level = get_maturity_level_table()
        fig_radar = get_radar_plot(df, facets)

        offline.plot(fig_table_levels, filename='./plots/table_levels.html')
        offline.plot(fig_fair_levels, filename='./plots/levels_plot.html')
        offline.plot(fig_maturity_level, filename='./plots/table_maturity.html')
        offline.plot(fig_radar, filename='./plots/radar_plot.html', image='jpeg', image_filename='abc')
if __name__ == "__main__":
    main()
