from flask import Flask, render_template
app = Flask(__name__)
@app.route("/")
def Home():
    return render_template('Home.html')

@app.route("/Base")
def base():
    return render_template('Base.html')

@app.route("/Explore.html")
def Explore():
    return render_template('Explore.html')

@app.errorhandler(404)
def error404(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404