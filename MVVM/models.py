from shared_db import db

class FeatureRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    description = db.Column(db.Text)
    priority = db.Column(db.Integer)
    due = db.Column(db.DateTime)
    client = db.Column(db.Integer, db.ForeignKey('client.id')) 
    product_area = db.Column(db.Integer, db.ForeignKey('area.id'))    
   
    def __init__(self, title, description, priority, due, client, product_area):
        self.title = title
        self.description = description
        self.priority = priority
        self.due = due
        self.client = client
        self.product_area = product_area

    def __repr__(self):
        return '<Name %r>' % self.title

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    feature_requests = db.relationship('FeatureRequest', backref=db.backref('Client'))

    def __init__(self, name):
        self.name = name

class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    feature_requests = db.relationship('FeatureRequest', backref=db.backref('Area'))

    def __init__(self, name):
        self.name = name