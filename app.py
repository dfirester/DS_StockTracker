from flask import Flask, render_template, request, redirect
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import bokeh
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, TextInput
from bokeh.plotting import figure, output_file
from bokeh.layouts import widgetbox
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.embed import components
from bokeh.resources import INLINE
import numpy as np
import requests
import stock_plot
from stock_plot import Stockplot



app = Flask(__name__)
stock_handler = Stockplot()


@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')


@app.route('/stock_index',methods=['GET','POST'])
def displaystock():
   
    stock = request.form['stockindex']
    date = request.form['date']
    unpack = stock_handler.generate_plot(stock,date)
    script, div = unpack

    kwargs = {'script':script,'div':div}
    kwargs['title'] = stock + ' Close Price'

    return render_template('plot.html',stockval=stock,dateval=date,**kwargs)
        
    


if __name__ == '__main__':
  app.run(debug=True)
