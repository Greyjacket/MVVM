from flask import Flask, render_template, request, Response, jsonify, g
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from models import FeatureRequest, Client, Area
from shared_db import db
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.route('/')
def submit_feature_request(name=None):
    return render_template('feature_request.html', name=name)

@app.route('/feature-request', methods=['GET', 'POST'])
def handle_request():
    if request.method == 'POST':
        result = request.get_json()
        try:
            title = result['title'] 
            description = result['description']
            client = result['selectedClient']
            priority = result['selectedPriority']
            due = result['due']
            productArea = result['productArea']
        except KeyError, e:
            return bad_request(str(e))

        due = datetime.datetime.strptime(due, '%Y-%m-%d')

        fq = FeatureRequest(title, description, priority, due, client, productArea)
        db.session.add(fq)
        db.session.commit()
        # return render_template('result.html', result=result)

def bad_request(message):
    response = jsonify({'error': message})
    response.status_code = 400
    return response



