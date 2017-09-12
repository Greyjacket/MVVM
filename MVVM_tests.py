import os
import MVVM
import unittest
import tempfile
import datetime
from flask import jsonify
import json 

class MVVMTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, MVVM.app.config['DATABASE'] = tempfile.mkstemp()
        MVVM.app.testing = True
        self.app = MVVM.app.test_client()    
        with MVVM.app.app_context():
            MVVM.init_db()
            
    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(MVVM.app.config['DATABASE'])

    def create_feature_request(self, data):
        response = self.app.post('/feature-request', data=data, content_type='application/json')
        print response.get_data(as_text=True)
        assert b'200' in response.data

    def test_feature_request(self):
        title = 'test1'
        description = 'this is a test'
        priority = 2
        client = "Client A"
        product_area = 'Billing'
        date = str(datetime.date.today())
        data = dict(title = title, description = description, selectedPriority = priority, date=date, selectedClient = client, productArea = product_area)
        data = json.dumps(data)
        self.create_feature_request(data)

if __name__ == '__main__':
    unittest.main()