from MVVM import Client, Area, db 


db.create_all()

client_a = Client('Client A')
client_b= Client('Client B')
client_c = Client('Client C')

policies = Area('Policies')
billing = Area('Billing')
claims = Area('Claims')
reports = Area('Reports')

db.session.add(client_a)
db.session.add(client_b)
db.session.add(client_c)
db.session.add(policies)
db.session.add(billing)
db.session.add(claims)
db.session.add(reports)

db.session.commit()
