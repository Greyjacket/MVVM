from flask import Flask, render_template, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username
        
def bad_request(message):
    response = jsonify({'error': message})
    response.status_code = 400
    return response

@app.route('/')
def hello_world(name=None):
	return render_template('feature_request.html', name=name)

@app.route('/admin', methods=['GET', 'POST'])
def print_users():
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

    '''
    user = User.query.filter_by(username='admin').first_or_404()
	'''
