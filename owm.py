import os
import requests
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
app = dash.Dash(__name__)


API_KEY=os.environ.get('API_KEY')
lis_cities = ['Banjul','Yundum','Bansang','Kerewan', 'Niamey','Agadez', 'Dakar']
def get_city(cities):
  dict_cities = []
  for i in cities:
    dict_cities.append({'label':i,'value':i})
  return dict_cities
    

    

app.layout = html.Div(children=[
html.Div(className='row',  # Define the row element
children=[
  # Define the left element
html.Div(className='four columns div-user-controls',
      children = [
      html.H2('Dash - Met Dash Board'),
      html.P('''Visualising time series with Plotly - Dash'''),
      html.P('''Pick one or more stocks from the dropdown below.'''),
      html.Div(className='div-for-dropdown',
          children=[
              dcc.Dropdown(id='city',
                           options=get_city(lis_cities),
                           multi=False,
                           value='Banjul',
                           style={'backgroundColor': '#1E1E1E'},
                           className='stockselector')
                    ],
          style={'color': '#1E1E1E'}),
      

  ]
      ),  

# Define the right element
html.Div(className='eight columns div-for-charts bg-grey', 
  children = [
    html.Div(
      dcc.Graph(id='temp',
          config={'displayModeBar': True}, 
        ),
    ),
    
    html.Div(
      dcc.Graph(id='humidity',
          config={'displayModeBar': True}, 
        ),
    ),
  ]
  )  
])
])

@app.callback([Output('temp', 'figure'),
              Output('humidity', 'figure')],
              [Input('city', 'value')])

def update_graphs(city):
  city = city
  url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid={}'
  r = requests.get(url.format(city, API_KEY)).json()

  main = []
  i = 0
  for val in r['list']:
      main.append(val['main'])
      main[i]['visibility']=val['visibility']
      main[i]['wind speed']=val['wind']['speed']
      main[i]['time']=val['dt_txt']
      i+=1
      
  df = pd.DataFrame(main)
  df['time']=pd.to_datetime(df['time'])
  df.set_index('time', inplace=True)

  sample = df.resample('D').agg({'temp_max':'max','temp_min':'min', 'temp':'mean', 'pressure':'mean','visibility':'mean','wind speed':'mean'})
  #figure
  fig1 = px.line(
          sample,
          y = ['temp_max', 'temp_min','temp'],
          x= list(sample.index),
          # color = 'Location',
          template='plotly_dark',
  )
  fig1.update_layout(title={'text':city,"font": {"size": 25}})
  fig1.update_traces(line=dict(dash="dot", width=4))

  fig2 = px.line(
        sample,
        y = 'pressure',
        x = list(sample.index),
        # color = 'Location',
        template='plotly_dark')
  fig2.update_layout(title={'text':city,"font": {"size": 25}})
  
  return fig1, fig2



if __name__ == '__main__':
    app.run_server(debug=True)