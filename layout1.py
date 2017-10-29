import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from flask import send_from_directory
from plotly import graph_objs as go
from datetime import datetime, date
import calendar
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
#%matplotlib inline


# DataFrame from external CSV file
df_fund_data = pd.read_csv('https://plot.ly/~jackp/17534.csv')
df_perf_summary = pd.read_csv('https://plot.ly/~jackp/17530.csv')
df_cal_year = pd.read_csv('https://plot.ly/~jackp/17528.csv')
df_perf_pc = pd.read_csv('https://plot.ly/~jackp/17532.csv')

# Making table
def make_dash_table(df):
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append( html.Td([  row[i]  ]) )
        table.append( html.Tr( html_row ) )
    return table

# Datatime
t = date.today()
t_day = t.day
t_month = t.month
t_year = t.year

month_index = {}
for i, v in enumerate(calendar.month_abbr):
    month_index[i] = v


# Table
modifed_perf_table = make_dash_table(df_perf_summary)
modifed_perf_table.insert(
    0, html.Tr( [
                    html.Td([]),
                    html.Td(['Cumulative'],  colSpan=4,  style=dict(textAlign="center")),
                    html.Td(['Annualized'], colSpan=4, style=dict(textAligh="center")),
             ], style= dict (background='white', fontweight=600)
    )
)

# CSV
df_fund_info = pd.read_csv('https://plot.ly/~jackp/17544.csv')
df_fund_characteristics = pd.read_csv('https://plot.ly/~jackp/17542.csv')
df_fund_facts = pd.read_csv('https://plot.ly/~jackp/17540.csv')
df_bond_allocation = pd.read_csv('https://plot.ly/~jackp/17538.csv')


app = dash.Dash()

#Descibe the layout, UI of the app

app.layout = html.Div([

    html.Div([ #page 1
         html.A([ 'Print PDF' ],
            className="button no-print",
            style=dict(position="absolute", top=-40, right=0)),

         html.Div([ #subpage 1
            # Row 1 (Header) #7F90AC
            html.Div([
                html.Div([
                    html.H4('YJ Trading  |  Daily Position & PL Report'),
                    html.Div('A subsidiary of Yahoo Japan!', style=dict(color='#7F90AC')),
                ], className='nine columns padded'),

                html.Div([
                    html.H1([html.Span(t_day, style=dict(opacity=0.5)), html.Span(month_index[t_month])]),
                    html.H6('Daily Update')
                ], className = "three columns gs-header gs-accent-header padded", style=dict(float='right')),
            ], className= "row gs-header gs-text-header"),

            html.Br([]),

            # Row 2
            html.Div([
                # Columns1
                html.Div([
                    html.H6('Daily Profit & Loss', className = "gs-header gs-text-header padded"),
                    html.Table( make_dash_table(df_perf_pc), className='tiny-header'),

                    html.Strong('The fund is designed for:'),
                    html.P('The fund is designed for investors who are looking for a flexible \
                            global investment and sub-investment grade fixed income portfolio \
                            that has the ability to alter its exposure with an emphasis on interest \
                            rates, currencies .', className = 'blue-text' ),

                ], className='five columns'),

                html.Div([
                    html.H6(["Performance (indexed)"], className= "gs-header gs-text gs-table-header padded"),
                    html.Iframe(src="https://plot.ly/~jackp/17553.embed?modebar=false&link=false&autosize=true", \
                        seamless="seamless", style=dict(border=0), width="100%", height="320")
                ], className="seven columns"),

            ], className="row"),

            # Row 2.5
            html.Div([
                html.Div([
                    html.H6('Performance (%)', className="gs-header gs-text-header padded"),
                    html.Table( make_dash_table(df_perf_pc), className='tiny-header')
                ], className="five columns"),

                html.Div([
                    html.P("This is an actively managed fund that is not designed to track its reference benchmark. \
                        Therefore the performance of the fund and."),
                ], className="seven columns"),
            ], className="row"),

            # Row 3
            html.Div([
                html.Div([
                    html.H6('Transaction Details', className="gs-header gs-text-header padded"),
                    html.Table(make_dash_table( df_fund_data ))
                ], className="five columns"),

                html.Div([
                    html.H6("Performance Summary (%)", className = "gs-header gs-table-header padded"),
                    html.Table( modifed_perf_table, className = "reversed" ),

                    html.H6("Position Summary(%)", className = "gs-header gs-table-header padded"),
                    html.Table( make_dash_table( df_cal_year ) )
                ], className="seven columns"),
            ], className= "row"),

         ], className="subpage"),
    ], className="page"),

    html.Div([ # page 2
        html.A([ 'Print PDF'],
            className="button no-print",
            style=dict(position="absolute", top=-40, right=0)),

        html.Div([ # subpage 2
            # Row 1 (Header)
            html.Div([
                html.Div([
                    html.H5('Goldman Sachs Strategic  Absolute Return Bond II Portfolio'),
                    html.H6('A sub-fund Goldman Sachs Funds, SICAV', style=dict(color='#7F90AC')),
                ], className="nine columns padded"),

                html.Div([
                    html.H1([html.Span(t_day, style=dict(opacity=0.5)), html.Span(month_index[t_month])]),
                    html.H6('Monthly Fund Update')
                ], className="three columns gs-header gs-accent-header padded", style=dict(float='right') ),
            ], className="row gs-header gs-text-header"),

            # Row 2
            html.Div([
                # Data tables on this page:
                # ---
                # df_fund_info = pd.read_csv('https://plot.ly/~jackp/17544/.csv')
                # df_fund_characteristics = pd.read_csv('https://plot.ly/~jackp/17542/.csv')
                # df_fund_facts = pd.read_csv('https://plot.ly/~jackp/17540/.csv')
                # df_bond_allocation = pd.read_csv('https://plot.ly/~jackp/17538/')

                # Column 1
                html.Div([
                    html.H6('Financial Information', className="gs-header gs-text-header padded"),
                    html.Table( make_dash_table( df_fund_info ) ),

                    html.H6('Fund Characteristics', className="gs-header gs-text-header padded"),
                    html.Table( make_dash_table( df_fund_characteristics ) ),

                    html.H6('Fund Facts', className = "gs-header gs-text-header padded"),
                    html.Table( make_dash_table( df_fund_facts ) ),
                ], className="four columns") ,

                # Columns 2
                html.Div([
                    html.H6('Sector Allocation (%)', className="gs-header gs-text-header padded"),
                    html.Iframe(src="https://plot.ly/~jackp/17560.embed?modebar=false&link=false&autosize=true", \
                        seamless="seamless", style=dict(border=0), width="100%", height="300"),
                    html.H6('Country Bond Allocation (%)', className="gs-header gs-text-header padded"),
                    html.Table( make_dash_table( df_bond_allocation ) ),
                ], className="four columns"),

                # Column 3
                html.Div([
                    html.H6('Top 10 Currency Weight (%)', className="gs-header gs-text-header padded"),
                    html.Iframe(src="https://plot.ly/~jackp/17555.embed?modebar=false&link=false&autosize=true", \
                        seamless="seamless", style=dict(border=0), width="100%", height="300"),

                    html.H6('Credit Allocation (%)', className = "gs-header gs-table-header padded"),
                    html.Iframe(src="https://plot.ly/~jackp/17557.embed?modebar=false&link=false&autosize=true", \
                        seamless="seamless", style=dict(border=0), width="100%", height="250"),
                ], className="four columns"),

            ], className="row"),

        ], className="subpage"),

    ], className="page")

])



# External CSS & js
external_css = [
        "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
        "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
        "//fonts.googleapis.com/css?family=Raleway:400,300,600",
        "https://codepen.io/koby1211/pen/MOWqjE.css",
        "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

for css in external_css:
    app.css.append_css({"external_url": css })


external_js = ["https://code.jquery.com/jquery-3.2.1.min.js", "https://codepen.io/plotly/pen/KmyPZr.js"]

for js in external_js:
    app.scripts.append_script({"external_url": js })

# app.css.config.serve_locally = True
# app.scripts.config.serve_locally = True
#
# @app.server.route('/static/<path:path>')
# def static_file(path):
#     static_folder = os.path.join(os.getcwd(), 'static')
#     return send_from_directory(static_folder, path)


# Run Server
if __name__ == "__main__":
    app.server.run()
