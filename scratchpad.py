from MVVM import Client, FeatureRequest, Area, db 

title = 'test1'
description = 'this is a test'
priority = 2
client = "Client A"
product_area = 'Billing'
def add_entry():
    db = get_db()
    db.execute('insert into FeatureRequest (title, description, priority, due, client, product_area) values (?, ?, ?, ?, ?, ?)',
                 (title, description, priority, due, client, product_area)
    #db.commit()
    print 'New entry was successfully posted'
    # return redirect(url_for('show_entries'))