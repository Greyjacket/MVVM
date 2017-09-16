from flask import Flask, render_template, request, Response, jsonify, g
from models import FeatureRequest, Client, Area
from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy
from shared_db import db
import datetime
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////usr/src/app/portfolio/MVVM/MVVM/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)

if __name__ == "__main__":
    app.run()
    
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

@app.route('/MVVM/submit')
def submit_feature_request(name=None):
    return render_template('feature_request.html', name=name)

@app.route('/MVVM/dashboard')
def dashboard(name=None):
    return render_template('dashboard.html', name=name)

@app.route('/feature-request', methods=['GET', 'POST'])
def handle_request():

    if request.method == 'GET':
        feature_obj = FeatureRequest.query.first()
        return prepare_json(feature_obj)

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

        #extract the priority number from the response
        priority = int(priority[0])

        # convert the received date into a datetime object
        due = datetime.datetime.strptime(due, '%Y-%m-%d')

        # get client + area object for foreign key id
        client_obj = Client.query.filter_by(name=client).first()
        area_obj = Area.query.filter_by(name=productArea).first()
        
        # check for any duplicate titles (titles are unique)
        try:
            fq = FeatureRequest(title, description, priority, due, client_obj.id, area_obj.id)
            db.session.add(fq)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return bad_request('duplicate')       

        return "OK"

def bad_request(message):
    response = jsonify({'error': message})
    response.status_code = 400
    return response

def prepare_json(obj):
    client_obj = Client.query.filter_by(id=obj.client).first()
    area_obj = Area.query.filter_by(id=obj.product_area).first()
    obj_dict = {'title': obj.title, 'description': obj.description, 'client': client_obj.name,
                'priority': obj.priority, 'due': obj.due, 'productArea': area_obj.name}
    return jsonify(obj_dict)

