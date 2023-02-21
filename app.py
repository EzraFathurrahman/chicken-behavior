from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('home.html')

@app.route("/aggressive")
def aggressive():
    return render_template('aggressive.html')

@app.route("/feed")
def feed():
    return render_template('feed.html')

@app.route("/anomaly")
def anomaly():
    return render_template('anomaly.html')

@app.route("/result", methods = ['POST'])
def result():
    return render_template('result.html')