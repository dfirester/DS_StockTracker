import numpy as np
import bokeh
import requests
import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, TextInput
from bokeh.plotting import figure, output_file
from bokeh.layouts import widgetbox
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.embed import components
from bokeh.resources import INLINE




class Stockplot():

    def __init__(self):
        self.stock = None
        self.date = None
        self.data = None
        self.opens = []
        self.close = []
        self.dates = []
        self.api_key = 'TB30LW5U413LFEYU'
        
    def _url(self,stock):
        return 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + stock + '&outputsize=full&apikey=' + self.api_key


    def _onemonth(self):
        datevals = [self.date.split('/')[i] for i in range(2)]
        if datevals[0] == '12':
            datevals[0] = '01'
            datevals[1] = str(int(int(datevals[1]) + 1))
        else:
            datevals[0] = str(int(int(datevals[0]) + 1))
            if len(datevals[0]) == 1:
                datevals[0] = '0'+datevals[0]
        
        return datevals[0] + '/' + datevals[1]

    def _getstock(self,stock,date):
        if stock == self.stock: #We have already loaded this data set, no need to reload
            pass
        else: #Need to load in the new data set to memory
            self.stock = stock
            try:
                getting = requests.get(self._url(stock))
                jsondata = getting.json()
                self.data = pd.DataFrame(jsondata['Time Series (Daily)'])
                self.data = self.data.T
            except:
                return 'badstock'
    
            


        self.date = date
        st = date
        dateval = st.split('/')[1] + '-' + st.split('/')[0] + '-'

        datestorage = []
        value = []
        for j in range(4):
            for i in range(10):
                if j*10 + i < 32:
                    try:
                        value.append(self.data.loc[dateval+'%d%d'%(j,i)].values)
                        datestorage.append(st.split('/')[0]+'/%d%d'%(j,i))
                    except:
                        pass
        value = np.array(value)

        if len(datestorage) == 0:
            return 'baddate'
        
        self.opens = []
        self.close = []
        self.dates = []
        self.dates = datestorage
        self.opens = value.T[0]
        self.close = value.T[3]

    def generate_plot(self,stock,date,*args):
        switch = self._getstock(stock,date)
       
        
        if switch == 'badstock':
            title = 'No stock matching ' + stock + ' found'
        elif switch == 'baddate':
            title = 'No data for given date'
        else:
            title = stock+ ' Closing Price from ' + self.date + ' to ' + self._onemonth()
        N = len(self.close)
        x = np.arange(N)


        
        source = ColumnDataSource(data=dict(x=x,y=self.close))
        plot = figure(plot_height=400,plot_width=600,title=title,tools='crosshair,pan,reset,save,wheel_zoom')
        plot.xaxis.ticker = [i*2 for i in range(N//2)]
        dictionary = {int(i):j for i,j in zip(np.arange(N),self.dates)}
        plot.xaxis.major_label_overrides = dictionary

        plot.line('x','y',source=source,line_width=3,line_alpha=0.6,legend='Close Price')
        

        for arg in args:
            if arg:
                source2 = ColumnDataSource(data=dict(x=x,y=self.opens))
                plot.line('x','y',source=source2,line_width=3,line_alpha=0.6,color='red',legend='Open Price')

        plot.legend.location = "top_left"
        plot.legend.click_policy="hide"

        return components(plot)





