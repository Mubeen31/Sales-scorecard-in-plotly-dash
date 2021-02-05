import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import dash_table as dt

sales = pd.read_csv('train.csv')
sales['Order Date'] = pd.to_datetime(sales['Order Date'])
sales['Year'] = sales['Order Date'].dt.year
sales['Month'] = sales['Order Date'].dt.month_name()


app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

app.layout = html.Div((

    html.Div([
        html.Div([
            html.Div([
                html.H3('Sales Scorecard', style = {'margin-bottom': '0px', 'color': 'white'}),
            ])
        ], className = "one third column", id = "title1"),

        html.Div([
            html.P('Year', className = 'fix_label', style = {'color': 'white'}),
            dcc.Slider(id = 'select_year',
                       included = False,
                       updatemode = 'drag',
                       tooltip = {'always_visible': True},
                       min = 2015,
                       max = 2018,
                       step = 1,
                       value = 2018,
                       marks = {str(yr): str(yr) for yr in range(2015, 2018)},
                       className = 'dcc_compon'),

        ], className = "one-half column", id = "title2"),

        html.Div([
            html.P('Segment', className = 'fix_label', style = {'color': 'white'}),
            dcc.RadioItems(id = 'radio_items',
                           labelStyle = {"display": "inline-block"},
                           value = 'Consumer',
                           options = [{'label': i, 'value': i} for i in sales['Segment'].unique()],
                           style = {'text-align': 'center', 'color': 'white'}, className = 'dcc_compon'),

        ], className = "one-third column", id = 'title3'),

    ], id = "header", className = "row flex-display", style = {"margin-bottom": "25px"}),

    html.Div([
        html.Div([
            dcc.RadioItems(id = 'radio_items1',
                           labelStyle = {"display": "inline-block"},
                           value = 'Sub-Category',
                           options = [{'label': 'Sub-Category', 'value': 'Sub-Category'},
                                      {'label': 'Region', 'value': 'Region'}],
                           style = {'text-align': 'center', 'color': 'white'}, className = 'dcc_compon'),
            dcc.Graph(id = 'bar_chart1',
                      config = {'displayModeBar': 'hover'}, style = {'height': '350px'}),

        ], className = 'create_container2 three columns', style = {'height': '400px'}),

        html.Div([
            dcc.Graph(id = 'donut_chart',
                      config = {'displayModeBar': 'hover'}, style = {'height': '350px'}),

        ], className = 'create_container2 three columns', style = {'height': '400px'}),

        html.Div([
            dcc.Graph(id = 'line_chart',
                      config = {'displayModeBar': 'hover'}, style = {'height': '350px'}),

        ], className = 'create_container2 four columns', style = {'height': '400px'}),


        html.Div([
              html.Div(id='text1'),
              html.Div(id='text2'),
              html.Div(id='text3'),

         ], className = 'create_container2 two columns', style = {'width': '260px'}),

    ], className = "row flex-display"),

    html.Div((
        html.Div([
            dt.DataTable(id = 'my_datatable',
                         columns = [{'name': i, 'id': i} for i in
                                    sales.loc[:, ['Order Date', 'Customer ID', 'Customer Name',
                                                  'Segment', 'City', 'State', 'Region',
                                                  'Category', 'Sub-Category', 'Product Name',
                                                  'Sales', 'Year', 'Month']]],
                         # page_action='native',
                         # page_size=20,
                         # editable=False,
                         sort_action = "native",
                         sort_mode = "multi",
                         # column_selectable="single",
                         # fill_width=False,
                         # style_table={
                         #         "width": "100%",
                         #         "height": "100vh"},
                         virtualization = True,
                         style_cell = {'textAlign': 'left',
                                       'min-width': '100px',
                                       'backgroundColor': '#1f2c56',
                                       'color': '#FEFEFE',
                                       'border-bottom': '0.01rem solid #19AAE1',
                                       },
                         style_as_list_view = True,
                         style_header = {
                             'backgroundColor': '#1f2c56',
                             'fontWeight': 'bold',
                             'font': 'Lato, sans-serif',
                             'color': 'orange',
                             'border': '#1f2c56',
                         },
                         style_data = {'textOverflow': 'hidden', 'color': 'white'},
                         fixed_rows = {'headers': True},
                         )

        ], className = 'create_container2 three columns'),

        html.Div([
            dcc.RadioItems(id = 'radio_items2',
                           labelStyle = {"display": "inline-block"},
                           value = 'State',
                           options = [{'label': 'State', 'value': 'State'},
                                      {'label': 'City', 'value': 'City'}],
                           style = {'text-align': 'center', 'color': 'white'}, className = 'dcc_compon'),
            dcc.Graph(id = 'bar_chart3',
                      config = {'displayModeBar': 'hover'}),

        ], className = 'create_container2 three columns'),

        html.Div([
            dcc.Graph(id = 'bubble_chart',
                      config = {'displayModeBar': 'hover'}),

        ], className = 'create_container2 six columns'),

    ), className = "row flex-display"),

), id= "mainContainer", style={"display": "flex", "flex-direction": "column"})


@app.callback(Output('bar_chart1', 'figure'),
              [Input('select_year', 'value')],
              [Input('radio_items1', 'value')],
              [Input('radio_items', 'value')])
def update_graph(select_year, radio_items1, radio_items):
    sales1 = sales.groupby(['Year', 'Segment', 'Sub-Category'])['Sales'].sum().reset_index()
    sales2 = sales1[(sales1['Year'] == select_year) & (sales1['Segment'] == radio_items)].sort_values(by = ['Sales'], ascending = False).nlargest(5, columns = ['Sales'])
    sales3 = sales.groupby(['Year', 'Segment', 'Region'])['Sales'].sum().reset_index()
    sales4 = sales3[(sales3['Year'] == select_year) & (sales3['Segment'] == radio_items)].sort_values(by = ['Sales'], ascending = False)

    if radio_items1 == 'Sub-Category':

     return {
        'data':[go.Bar(
                    x=sales2['Sales'],
                    y=sales2['Sub-Category'],
                    text = sales2['Sales'],
                    texttemplate = '$' + '%{text:.2s}',
                    textposition = 'auto',
                    orientation = 'h',
                    marker = dict(color='#19AAE1 '),

                    hoverinfo='text',
                    hovertext=
                    '<b>Year</b>: ' + sales2['Year'].astype(str) + '<br>' +
                    '<b>Segment</b>: ' + sales2['Segment'].astype(str) + '<br>' +
                    '<b>Sub-Category</b>: ' + sales2['Sub-Category'].astype(str) + '<br>' +
                    '<b>Sales</b>: $' + [f'{x:,.2f}' for x in sales2['Sales']] + '<br>'



              )],


        'layout': go.Layout(
             plot_bgcolor='#1f2c56',
             paper_bgcolor='#1f2c56',
             title={
                'text': 'Sales by Sub-Category in year' + ' ' + str((select_year)),

                'y': 0.99,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={
                        'color': 'white',
                        'size': 12},

             hovermode='closest',
             margin = dict(t = 40, r = 0),

             xaxis=dict(title='<b></b>',
                        color = 'orange',
                        showline = True,
                        showgrid = True,
                        showticklabels = True,
                        linecolor = 'orange',
                        linewidth = 1,
                        ticks = 'outside',
                        tickfont = dict(
                            family = 'Arial',
                            size = 12,
                            color = 'orange ')


                ),

             yaxis=dict(title='<b></b>',
                        autorange = 'reversed',
                        color = 'orange ',
                        showline = False,
                        showgrid = False,
                        showticklabels = True,
                        linecolor = 'orange',
                        linewidth = 1,
                        ticks = 'outside',
                        tickfont = dict(
                            family = 'Arial',
                            size = 12,
                            color = 'orange')

                ),

            legend = {
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'x': 0.5,
                'y': 1.25,
                'xanchor': 'center',
                'yanchor': 'top'},

            font = dict(
                family = "sans-serif",
                size = 15,
                color = 'white'),


                 )

    }

    elif radio_items1 == 'Region':


     return {
        'data':[go.Bar(
                    x=sales4['Sales'],
                    y=sales4['Region'],
                    text = sales4['Sales'],
                    texttemplate = '$' + '%{text:.2s}',
                    textposition = 'auto',
                    orientation = 'h',
                    marker = dict(color='#19AAE1 '),

                    hoverinfo='text',
                    hovertext=
                    '<b>Year</b>: ' + sales4['Year'].astype(str) + '<br>' +
                    '<b>Segment</b>: ' + sales4['Segment'].astype(str) + '<br>' +
                    '<b>Sub-Category</b>: ' + sales4['Region'].astype(str) + '<br>' +
                    '<b>Sales</b>: $' + [f'{x:,.2f}' for x in sales4['Sales']] + '<br>'



              )],


        'layout': go.Layout(
             plot_bgcolor='#1f2c56',
             paper_bgcolor='#1f2c56',
             title={
                'text': 'Sales by Region in year' + ' ' + str((select_year)),

                'y': 0.99,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={
                        'color': 'white',
                        'size': 12},

             hovermode='closest',
             margin = dict(t = 40, r = 0),

             xaxis=dict(title='<b></b>',
                        color = 'orange',
                        showline = True,
                        showgrid = True,
                        showticklabels = True,
                        linecolor = 'orange',
                        linewidth = 1,
                        ticks = 'outside',
                        tickfont = dict(
                            family = 'Arial',
                            size = 12,
                            color = 'orange')


                ),

             yaxis=dict(title='<b></b>',
                        autorange = 'reversed',
                        color = 'orange',
                        showline = False,
                        showgrid = False,
                        showticklabels = True,
                        linecolor = 'orange',
                        linewidth = 1,
                        ticks = 'outside',
                        tickfont = dict(
                            family = 'Arial',
                            size = 12,
                            color = 'orange')

                ),

            legend = {
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'x': 0.5,
                'y': 1.25,
                'xanchor': 'center',
                'yanchor': 'top'},

            font = dict(
                family = "sans-serif",
                size = 15,
                color = 'white'),


                 )

    }

@app.callback(Output('donut_chart', 'figure'),
             [Input('select_year', 'value')],
             [Input('radio_items', 'value')])
def update_graph(select_year, radio_items):
        sales8 = sales.groupby(['Year', 'Segment', 'Category'])['Sales'].sum().reset_index()
        furniture_sales = sales8[(sales8['Year'] == select_year) & (sales8['Segment'] == radio_items) & (sales8['Category'] == 'Furniture')]['Sales'].sum()
        office_sales = sales8[(sales8['Year'] == select_year) & (sales8['Segment'] == radio_items) & (sales8['Category'] == 'Office Supplies')]['Sales'].sum()
        technology_sales = sales8[(sales8['Year'] == select_year) & (sales8['Segment'] == radio_items) & (sales8['Category'] == 'Technology')]['Sales'].sum()
        colors = ['#30C9C7', '#7A45D1', 'orange']

        return {
            'data': [go.Pie(labels = ['Furniture', 'Office Supplies', 'Technology'],
                            values = [furniture_sales, office_sales, technology_sales],
                            marker = dict(colors = colors),
                            hoverinfo = 'label+value+percent',
                            textinfo = 'label+value',
                            textfont = dict(size = 13),
                            texttemplate = '%{label} <br>$%{value:,.2f}',
                            textposition = 'auto',
                            hole = .7,
                            rotation = 160,
                            insidetextorientation='radial',

                            )],

            'layout': go.Layout(
                plot_bgcolor = '#1f2c56',
                paper_bgcolor = '#1f2c56',
                hovermode = 'x',
                title = {
                    'text': 'Sales by Category in Year' + ' ' + str((select_year)),

                    'y': 0.93,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                titlefont = {
                    'color': 'white',
                    'size': 15},
                legend = {
                    'orientation': 'h',
                    'bgcolor': '#1f2c56',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.15},

                font = dict(
                    family = "sans-serif",
                    size = 12,
                    color = 'white')
            ),

        }

@app.callback(
    Output('text1', 'children'),
    [Input('select_year', 'value')])

def update_text(select_year):
    sales6 = sales.groupby(['Year'])['Sales'].sum().reset_index()
    current_year = sales6[sales6['Year'] == select_year]['Sales'].sum()

    return [

               html.H6(children = 'Current Year',
                       style = {'textAlign': 'center',
                                'color': 'white'}
                       ),

               html.P('${0:,.2f}'.format(current_year),
                      style={'textAlign': 'center',
                             'color': '#19AAE1',
                             'fontSize': 15,
                             'margin-top': '-10px'
                             }
                      ),
    ]

@app.callback(
    Output('text2', 'children'),
    [Input('select_year', 'value')])

def update_text(select_year):
    sales6 = sales.groupby(['Year'])['Sales'].sum().reset_index()
    sales6['PY'] = sales6['Sales'].shift(1)
    previous_year = sales6[sales6['Year'] == select_year]['PY'].sum()

    return [

               html.H6(children = 'Previous Year',
                       style = {'textAlign': 'center',
                                'color': 'white'}
                       ),

               html.P('${0:,.2f}'.format(previous_year),
                      style={'textAlign': 'center',
                             'color': '#19AAE1',
                             'fontSize': 15,
                             'margin-top': '-10px'
                             }
                      ),
    ]

@app.callback(
    Output('text3', 'children'),
    [Input('select_year', 'value')])

def update_text(select_year):
    sales6 = sales.groupby(['Year'])['Sales'].sum().reset_index()
    sales6['PY'] = sales6['Sales'].shift(1)
    sales6['YOY Growth'] = sales6['Sales'].pct_change()
    sales6['YOY Growth'] = sales6['YOY Growth'] * 100
    previous_year_growth = sales6[sales6['Year'] == select_year]['YOY Growth'].sum()

    return [

               html.H6(children = 'YOY Growth',
                       style = {'textAlign': 'center',
                                'color': 'white'}
                       ),

               html.P('{0:,.2f}%'.format(previous_year_growth),
                      style={'textAlign': 'center',
                             'color': '#19AAE1',
                             'fontSize': 15,
                             'margin-top': '-10px'}
                      ),
    ]

@app.callback(Output('line_chart', 'figure'),
              [Input('select_year', 'value')],
              [Input('radio_items', 'value')])
def update_graph(select_year, radio_items):
    sales6 = sales.groupby(['Year', 'Segment', 'Month'])['Sales'].sum().reset_index()
    sales7 = sales6[(sales6['Year'] == select_year) & (sales6['Segment'] == radio_items)]



    return {
        'data':[
            go.Scatter(
                x = sales7['Month'],
                y = sales7['Sales'],
                name = 'Sales',
                text = sales7['Sales'],
                texttemplate = '%{text:.2s}',
                textposition = 'bottom left',
                mode = 'markers+lines+text',
                line = dict(width = 3, color = 'orange'),
                marker = dict(size = 10, symbol = 'circle', color = '#19AAE1',
                              line = dict(color = '#19AAE1', width = 2)
                              ),

                hoverinfo = 'text',
                hovertext =
                '<b>Year</b>: ' + sales7['Year'].astype(str) + '<br>' +
                '<b>Month</b>: ' + sales7['Month'].astype(str) + '<br>' +
                '<b>Segment</b>: ' + sales7['Segment'].astype(str) + '<br>' +
                '<b>Sales</b>: $' + [f'{x:,.2f}' for x in sales7['Sales']] + '<br>'

            )],


        'layout': go.Layout(
             plot_bgcolor='#1f2c56',
             paper_bgcolor='#1f2c56',
             title={
                'text': 'Sales Trend in year' + ' ' + str((select_year)),

                'y': 0.99,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={
                        'color': 'white',
                        'size': 15},

             hovermode='closest',
             margin = dict(t = 5, l = 0, r = 0),

             xaxis = dict(title = '<b></b>',
                          visible = True,
                          color = 'orange',
                          showline = True,
                          showgrid = False,
                          showticklabels = True,
                          linecolor = 'orange',
                          linewidth = 1,
                          ticks = 'outside',
                          tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'orange')

                         ),

             yaxis = dict(title = '<b></b>',
                          visible = True,
                          color = 'orange',
                          showline = False,
                          showgrid = True,
                          showticklabels = False,
                          linecolor = 'orange',
                          linewidth = 1,
                          ticks = '',
                          tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'orange')

                         ),

            legend = {
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'x': 0.5,
                'y': 1.25,
                'xanchor': 'center',
                'yanchor': 'top'},

            font = dict(
                family = "sans-serif",
                size = 12,
                color = 'white'),

        )

    }

@app.callback(
    Output('my_datatable', 'data'),
    [Input('select_year', 'value')],
    [Input('radio_items', 'value')])
def display_table(select_year, radio_items):
    data_table = sales[(sales['Year'] == select_year) & (sales['Segment'] == radio_items)]
    return data_table.to_dict('records')


@app.callback(Output('bar_chart3', 'figure'),
              [Input('select_year', 'value')],
              [Input('radio_items2', 'value')],
              [Input('radio_items', 'value')])
def update_graph(select_year, radio_items2, radio_items):
    sales1 = sales.groupby(['Year', 'Segment', 'State'])['Sales'].sum().reset_index()
    sales2 = sales1[(sales1['Year'] == select_year) & (sales1['Segment'] == radio_items)].sort_values(by = ['Sales'], ascending = False).nlargest(10, columns = ['Sales'])
    sales3 = sales.groupby(['Year', 'Segment', 'City'])['Sales'].sum().reset_index()
    sales4 = sales3[(sales3['Year'] == select_year) & (sales3['Segment'] == radio_items)].sort_values(by = ['Sales'], ascending = False).nlargest(10, columns = ['Sales'])

    if radio_items2 == 'State':



     return {
        'data':[go.Bar(
                    x=sales2['Sales'],
                    y=sales2['State'],
                    text = sales2['Sales'],
                    texttemplate = '$' + '%{text:.2s}',
                    textposition = 'auto',
                    orientation = 'h',
                    marker = dict(color='#19AAE1 '),

                    hoverinfo='text',
                    hovertext=
                    '<b>Year</b>: ' + sales2['Year'].astype(str) + '<br>' +
                    '<b>Segment</b>: ' + sales2['Segment'].astype(str) + '<br>' +
                    '<b>State</b>: ' + sales2['State'].astype(str) + '<br>' +
                    '<b>Sales</b>: $' + [f'{x:,.2f}' for x in sales2['Sales']] + '<br>'



              )],


        'layout': go.Layout(
             plot_bgcolor='#1f2c56',
             paper_bgcolor='#1f2c56',
             title={
                'text': 'Sales by State in year' + ' ' + str((select_year)),

                'y': 0.99,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={
                        'color': 'white',
                        'size': 12},

             hovermode='closest',
             margin = dict(l = 130, t = 40, r = 0),

             xaxis=dict(title='<b></b>',
                        color = 'orange',
                        showline = True,
                        showgrid = True,
                        showticklabels = True,
                        linecolor = 'orange',
                        linewidth = 1,
                        ticks = 'outside',
                        tickfont = dict(
                            family = 'Arial',
                            size = 12,
                            color = 'orange')


                ),

             yaxis=dict(title='<b></b>',
                        autorange = 'reversed',
                        color = 'orange',
                        showline = False,
                        showgrid = False,
                        showticklabels = True,
                        linecolor = 'orange',
                        linewidth = 1,
                        ticks = 'outside',
                        tickfont = dict(
                            family = 'Arial',
                            size = 12,
                            color = 'orange')

                ),

            legend = {
                'orientation': 'h',
                'bgcolor': '#F2F2F2',
                'x': 0.5,
                'y': 1.25,
                'xanchor': 'center',
                'yanchor': 'top'},

            font = dict(
                family = "sans-serif",
                size = 15,
                color = 'white'),


                 )

    }


    elif radio_items2 == 'City':


     return {
        'data':[go.Bar(
                    x=sales4['Sales'],
                    y=sales4['City'],
                    text = sales4['Sales'],
                    texttemplate = '$' + '%{text:.2s}',
                    textposition = 'auto',
                    orientation = 'h',
                    marker = dict(color='#19AAE1 '),

                    hoverinfo='text',
                    hovertext=
                    '<b>Year</b>: ' + sales4['Year'].astype(str) + '<br>' +
                    '<b>Segment</b>: ' + sales4['Segment'].astype(str) + '<br>' +
                    '<b>City</b>: ' + sales4['City'].astype(str) + '<br>' +
                    '<b>Sales</b>: $' + [f'{x:,.2f}' for x in sales4['Sales']] + '<br>'



              )],


        'layout': go.Layout(
             plot_bgcolor='#1f2c56',
             paper_bgcolor='#1f2c56',
             title={
                'text': 'Sales by City in year' + ' ' + str((select_year)),

                'y': 0.99,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={
                        'color': 'white',
                        'size': 12},

             hovermode='closest',
             margin = dict(l = 130, t = 40, r = 0),
             xaxis=dict(title='<b></b>',
                        color = 'orange',
                        showline = True,
                        showgrid = True,
                        showticklabels = True,
                        linecolor = 'orange',
                        linewidth = 1,
                        ticks = 'outside',
                        tickfont = dict(
                            family = 'Arial',
                            size = 12,
                            color = 'orange')


                ),

             yaxis=dict(title='<b></b>',
                        autorange = 'reversed',
                        color = 'orange',
                        showline = False,
                        showgrid = False,
                        showticklabels = True,
                        linecolor = 'orange',
                        linewidth = 1,
                        ticks = 'outside',
                        tickfont = dict(
                            family = 'Arial',
                            size = 12,
                            color = 'orange')

                ),

            legend = {
                'orientation': 'h',
                'bgcolor': '#F2F2F2',
                'x': 0.5,
                'y': 1.25,
                'xanchor': 'center',
                'yanchor': 'top'},

            font = dict(
                family = "sans-serif",
                size = 15,
                color = 'white'),


                 )

    }


@app.callback(Output('bubble_chart', 'figure'),
              [Input('select_year', 'value')],
              [Input('radio_items', 'value')])
def update_graph(select_year, radio_items):
    sales9 = sales.groupby(['Year', 'Segment', 'State', 'City', 'Month'])['Sales'].sum().reset_index()
    sales10 = sales9[(sales9['Year'] == select_year) & (sales9['Segment'] == radio_items)]

    return {
        'data': [go.Scatter(
            x = sales10['Month'],
            y = sales10['Sales'],
            mode = 'markers',
            marker = dict(
                size = sales10['Sales'] / 250,
                color = sales10['Sales'],
                colorscale = 'HSV',
                showscale = False,
                line = dict(
                    color = 'MediumPurple',
                    width = 2
                )),
            hoverinfo = 'text',
            hovertext =
            '<b>Year</b>: ' + sales10['Year'].astype(str) + '<br>' +
            '<b>Month</b>: ' + sales10['Month'].astype(str) + '<br>' +
            '<b>Segment</b>: ' + sales10['Segment'].astype(str) + '<br>' +
            '<b>State</b>: ' + sales10['State'].astype(str) + '<br>' +
            '<b>City</b>: ' + sales10['City'].astype(str) + '<br>' +
            '<b>Sales</b>: $' + [f'{x:,.0f}' for x in sales10['Sales']] + '<br>'

        )],

        'layout': go.Layout(
            plot_bgcolor = '#1f2c56',
            paper_bgcolor = '#1f2c56',
            title = {
                'text': 'Sales by State and City in year' + ' ' + str((select_year)),

                'y': 0.99,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont = {
                'color': 'white',
                'size': 15},
            margin = dict(t = 40, r = 0, l = 0),

            hovermode = 'closest',

            xaxis = dict(title = '<b></b>',
                         color = 'orange',
                         showline = False,
                         showgrid = False,
                         showticklabels = True,
                         linecolor = 'orange',
                         linewidth = 1,
                         ticks = '',
                         tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'orange')

                         ),

            yaxis = dict(title = '<b></b>',
                         color = 'orange',
                         visible = True,
                         showline = False,
                         showgrid = True,
                         showticklabels = False,
                         linecolor = 'orange',
                         linewidth = 1,
                         ticks = '',
                         tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'orange')

                         ),

            legend = {
                'orientation': 'h',
                'bgcolor': '#F2F2F2',
                'x': 0.5,
                'y': 1.25,
                'xanchor': 'center',
                'yanchor': 'top'},

            font = dict(
                family = "sans-serif",
                size = 12,
                color = 'white'),

        )

    }

if __name__ == '__main__':
    app.run_server(debug=True)
