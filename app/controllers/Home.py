from app.classes.Database import Database
from flask import Blueprint, render_template, flash

bp = Blueprint('home', __name__, url_prefix='', static_folder='../static')

# Load the index page
@bp.route('/')
def index():

    error = None
    latest_images = []
    try:
        database = Database()
        latest_images = database.get_latest_images()
    except Exception as err:
        error = err

    if error:
        flash(error)

    return render_template('home.html', latest_images=latest_images)

@bp.errorhandler(404)
def error404(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404