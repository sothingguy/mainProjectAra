from flask import Flask, render_template
app = Flask(__name__)

@app.route("/") #login.html
def login():
    return render_template('login.html')

@app.route("/register") #login.html
def register():
    return render_template('register.html')

@app.route("/home") #Home.html
def home():
    return render_template('Home.html')

@app.route("/explore") #Explore.html
def explore():
    return render_template('Explore.html')

@app.errorhandler(404) #404.html
def error404(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route("/base") #base.html
def base():
    return render_template('Base.html')

if __name__ == '__main__': #running flask
  app.run(debug=True)