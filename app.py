from flask import Flask, render_template, request, redirect, url
from flask_wtf import FlaskForm
import quandl
import pandas as pd
from bokeh.embed import components
from boheh.plotting import figure
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['FLASK_SECRET']


class InputForm(FlaskForm):
  ticker = StringField('Ticker', validators=[DataRequired()])
  features = StringField('features')
  submit = SubmitField('Submit')


def get_data(form):
  quandl.ApiConfig.api_key = os.environ['QUANDL_API_KEY']
  colors = ['blue', 'red', 'orange', 'red']

  data = quandl.get_table('WIKI/PRICES', ticker = request.form.get('ticker'),
  qopts = {'columns': ['ticker', 'date', 'close', 'adj_close', 'open', 'adj_open' ]},\
  date = {'gte': '2015-12-31', 'lte': '2016-12-31'},pageinate = True)
  data = data.set_index('date')

  return data


  '''p3 = figure(x_axis_type='datetime', title = 'Showing Price For: '+ request.form.get('ticker') + ' 2016')
  c = 0
  for feature in request.form.get_list('features'):'''


@app.route('/index', method = ['GET', 'POST'])
def index():
  if request.method == 'GET':
    return render_template('index.html')

  #get data from input
  data = request.form.get('submit')
  #plot data returned

  #render plot





@app.route('/about')
def about():
  return render_template('about.html')

if __name__ == '__main__':
  app.run(port=33507)
