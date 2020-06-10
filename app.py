from flask import Flask, render_template
app = Flask(__name__)
@app.route("/")
def home():
    return "Hello, Flask!"
@app.errorhandler(404)
def error404(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404