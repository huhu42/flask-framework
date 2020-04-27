import quandl
from flask import Flask, render_template, request, redirect
import numpy as np
import bokeh
from bokeh.embed import components
from bokeh.plotting import figure
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['FLASK_SECRET']

quandl.ApiConfig.api_key = os.environ['QUANDL_API_KEY']


bv = bokeh.__version__

app.vars = {}
feat = ['Open', 'Close', 'High', 'Low']


@app.route('/')
def main():
    return redirect('/index')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    app.vars['ticker'] = request.form['ticker'].upper()
    app.vars['features'] = [feat[i] for i in range(4) if feat[i] in request.form.values()]

    return redirect('/graph')

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    #get the data frame
    df = quandl.get_table('WIKI/PRICES', ticker=app.vars['ticker'],
                          qopts={'columns': ['ticker', 'date', 'open', 'high', 'low', 'close']},
                          date={'gte': '2015-12-31', 'lte': '2016-12-31'})

    p = figure(plot_width=450, plot_height=450, title=app.vars['ticker'], x_axis_type="datetime")


    if 'High' in app.vars['features']:
        p.line(df.date, df.high, line_width=2, line_color='#00cc00', legend_label='Daily Highs')
    if 'Low' in app.vars['features']:
        p.line(df.date, df.low, line_width=2, line_color="#ffff00", legend_label='Daily Lows')
    if 'High' in app.vars['features'] and 'Low' in app.vars['features']:
        x_ = np.array([df.date, df.date[::-1]]).flatten()
        y_ = np.array([df.high, df.low[::-1]]).flatten()
        p.patch(x_, y_, alpha=0.3, color="gray", legend_label='Range (High/Low)')
    if 'Open' in app.vars['features']:
        p.line(df.date, df.open, line_width=2, legend_label='Opening price')
    if 'Close' in app.vars['features']:
        p.line(df.date, df.close, line_width=2, line_color="#FB8072", legend_label='Closing price')

    p.legend.location = "bottom_right"

    p.xaxis.axis_label = "Date"
    p.yaxis.axis_label = "Price ($)"

    script, div = components(p)
    return render_template('graph.html', bv=bv, ticker=app.vars['ticker'],
                         yrtag='2015',
                         script=script, div=div)


@app.errorhandler(500)
def error_handler(e):
    return render_template('error.html')


if __name__ == '__main__':
    app.run(port=33507, debug=True)
