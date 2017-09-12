from flask import Flask, render_template, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    feature_requests = db.relationship('FeatureRequest', backref='client')

class ProductArea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    feature_requests = db.relationship('FeatureRequest', backref='product_area')

class FeatureRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    description = db.Column(db.Text)
    priority = db.Column(db.Integer)
    due = db.Column(db.DateTime)
    client = db.Column(db.Integer, db.ForeignKey('Client.id')) 
    product_area = db.Column(db.Integer, db.ForeignKey('ProductArea.id'))    
   
    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Name %r>' % self.title

def bad_request(message):
    response = jsonify({'error': message})
    response.status_code = 400
    return response

@app.route('/')
def home(name=None):
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
    		date = result['date']
    		productArea = result['productArea']

    	except KeyError, e:
    		return bad_request(str(e))
        return render_template('result.html', result=result)

