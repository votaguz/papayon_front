import os
import requests
from flask import Flask
from flask import render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'R~XHH!Zr98j/3yXjmN]LWX/,?RTA0'

HOST_URL = 'http://4igc.localtunnel.com'

@app.route('/logout/', methods=['POST'])
def logout():
    payload = {
        'session_token': session['session_token']
    }
    response = requests.post('%s/extranet_services/logout/' % HOST_URL, data=payload)
    return redirect(url_for('login'))


@app.route('/', methods=['POST', 'GET'])
def login():
    data = {}
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        payload = {'email': email, 'password':password}
        response = requests.post('%s/extranet_services/login/' % HOST_URL, data=payload )
        print response
        response = response.json()
        print response
        if response['success'] == True:
            session['session_token'] = response['session_token']
            return redirect(url_for('order_list'))
            # return redirect(url_for('order_list', session_token=session['session_token']))
    return render_template('login.html', data=data)


@app.route('/order_list/', methods=['GET'])
def order_list():
    data = {}
    payload = {
        'session_token': session['session_token']
    }
    response = requests.post('%s/extranet_services/list_purchase_orders/' % HOST_URL, data=payload)
    try:
        data = response.json()
    except Exception, e:
        data = {'success': False, 'message': 'User not Logged in'}

    return render_template('order_list.html', data=data)



    # STATUS_CHOICES = (
    #     (1, 'En espera'),
    #     (2, 'Aceptada'),
    #     (3, 'Denegada'),
    # )


@app.route('/update_order_status/', methods=['POST'])
def update_order_status():
    payload = {
        'session_token': session['session_token']        
    }
    
    payload['order_id'] = request.form['order_id']
    payload['status'] = request.form['status']

    response = requests.post('%s/extranet_services/update_status_purchase_order/' % HOST_URL, data=payload)
    try:
        data = response.json()
    except Exception, e:
        data = {'success': False, 'message': 'User not Logged in'}

    return render_template('order_list.html', data=data)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', debug=True, port=port)
