from flask import render_template

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
    		date = result['date']
    		productArea = result['productArea']
    	except KeyError, e:
    		return bad_request(str(e))

        print "TEST"
        return "Hello"
        # return render_template('result.html', result=result)

def bad_request(message):
    response = jsonify({'error': message})
    response.status_code = 400
    return response