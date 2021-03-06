from flask import Flask, render_template, request, Response, jsonify, g
from models import FeatureRequest, Client, Area
from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy
from shared_db import db
import datetime
import sqlite3
import json

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

@app.route('/MVVM/overview')
def overview(name=None):
    return render_template('overview.html', name=name)

@app.route('/MVVM/submit')
def submit_feature_request(name=None):
    return render_template('feature_request.html', name=name)

@app.route('/MVVM/dashboard')
def dashboard(name=None):
    return render_template('dashboard.html', name=name)

@app.route('/MVVM/clients')
def clients(name=None):
    return render_template('clients.html', name=name)

@app.route('/feature-request', methods=['GET', 'POST'])
def handle_feature_request():

    if request.method == 'GET':

        sort_method = request.args.get('sort')
        client_sort = request.args.get('client')

        if(sort_method == 'Most Recent' and client_sort == 'All'):
            sorted = FeatureRequest.query.order_by(FeatureRequest.submit_date).limit(20).all()
        elif(sort_method == 'Priority' and client_sort == 'All'):
            sorted = FeatureRequest.query.order_by(FeatureRequest.priority).limit(20).all()
        elif(sort_method == 'Most Recent' and client_sort != 'All'):
            client = Client.query.filter_by(name=client_sort).first()
            sorted = FeatureRequest.query.filter_by(client=client.id).order_by(FeatureRequest.submit_date).limit(20).all()
        else:
            client = Client.query.filter_by(name=client_sort).first()
            sorted = FeatureRequest.query.filter_by(client=client.id).order_by(FeatureRequest.priority).limit(20).all()

        json_list = []
        
        for item in sorted:
            json_list.append(prepare_json(item))

        return jsonify(json_list)
        
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
        #get the current date
        submit_date = datetime.datetime.now()

        # get client + area object for foreign key id
        client_obj = Client.query.filter_by(name=client).first()
        area_obj = Area.query.filter_by(name=productArea).first()
        
        # check for any duplicate titles (titles are unique)
        try:
            fq = FeatureRequest(title, description, priority, due, client_obj.id, area_obj.id, submit_date)
            db.session.add(fq)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return bad_request('duplicate')       

        return "OK"

@app.route('/clients', methods=['GET', 'POST'])
def handle_client_request():

    if request.method == 'GET':

        clients = Client.query.all()
        json_list = []

        for client in clients:
            json_list.append(client.name)
        
        return jsonify(json_list)

def bad_request(message):
    response = jsonify({'error': message})
    response.status_code = 400
    return response

def prepare_json(obj):
    client_obj = Client.query.filter_by(id=obj.client).first()
    area_obj = Area.query.filter_by(id=obj.product_area).first()
    obj_dict = {'title': obj.title, 'description': obj.description, 'client': client_obj.name,
                'priority': obj.priority, 'due': obj.due, 'productArea': area_obj.name}
    return obj_dict

