from flask import Flask, render_template
app = Flask(__name__)
@app.route("/")
def home():
    return render_template('home.html')
#@app.route("/Base")
#def base():
    #return render_template('Base.html')

@app.errorhandler(404)
def error404(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404