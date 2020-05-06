# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from CovidHackNewWithFuture import covid_writer, graph_maker_day, graph_maker_week, graph_maker_five_day, graph_maker_seven_day
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt

GRAPHS_FOLDER = os.path.join('static', 'graphs')

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = GRAPHS_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'svg'])

dir_to_date = {

    "2020_03_26" : "March 26",
    "2020_03_27" : "March 27",
    "2020_03_29" : "March 29",
    "2020_03_30" : "March 30",
    "2020_03_31.1" : "March 31",
    "2020_04_01.2" : "April 1",
    "2020_04_05.08.all" : "April 5",
    "2020_04_07.06.all"	: "April 7",
    "2020_04_09.04"	: "April 9",
    "2020_04_12.02"	: "April 12",
    "2020_04_16.05"	: "April 16",
    "2020_04_20.02.all"	: "April 20",
    "2020_04_21.08"	: "April 21",
    "2020_04_26.08"	: "April 26",
    "2020_04_27.05.c" : "April 27",
    "2020_04_28.02"	: "April 28",
    "2020_05_04" : "May 4"

    }

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("display_graph.html")

@app.route('/graph', methods=["GET", "POST"])
def show_graph():

    for root, dirs, files in os.walk(F'/home/ajiang10224/mysite/static/graphs'):
        for filename in files:
            if 'with_future' in filename:
                os.remove(os.path.join(F'/home/ajiang10224/mysite/static/graphs', filename))

    dirs = request.form.get('dirs')
    state = request.form.get('states')
    style = request.form.get('style')

    matplotlib.use("Agg")

    if 'Daily' in style:
        covid_writer(dirs, state)
        graph_maker_day(dirs, state)
        filename = os.path.join(app.config['UPLOAD_FOLDER'], F'{dirs}_{state}_with_future_daily.png')

    elif 'Weekly' in style:
        covid_writer(dirs, state)
        graph_maker_week(dirs, state)
        filename = os.path.join(app.config['UPLOAD_FOLDER'], F'{dirs}_{state}_with_future_weekly.png')

    elif '5 Day Avg' in style:
        covid_writer(dirs, state)
        graph_maker_five_day(dirs, state)
        filename = os.path.join(app.config['UPLOAD_FOLDER'], F'{dirs}_{state}_with_future_5_day_average.png')

    elif '7 Day Avg' in style:
        covid_writer(dirs, state)
        graph_maker_seven_day(dirs, state)
        filename = os.path.join(app.config['UPLOAD_FOLDER'], F'{dirs}_{state}_with_future_7_day_average.png')

    return render_template("display_graph.html", graph=filename, text=F'Real {style} Deaths Compared to Predictions for {state} on {dir_to_date[dirs]}')