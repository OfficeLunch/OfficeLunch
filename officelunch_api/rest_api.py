# Author:       Clinton Beasley
# Date:         April 16, 2016
# Name:         rest_api.py
# Description:  REST API for Office Lunch

from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources=r'/api/*', headers='Content-Type')
# app.config['CORS_HEADERS'] = 'Content-Type'

users = [
    {
        'id': 1,
        'name': 'Clinton Beasley',
        'username': 'clinton',
        'password': 'office_lunch'
    }
]


def get_user_id(username, password):
    user_id = '-1'
    for obj in users:
        if username == obj['username'] and password == obj['password']:
            user_id = obj['id']

    # print 'User ID: %s' % user_id
    return user_id


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/api/login', methods=['GET'])
def get_login():
    data = ''
    if 'username' in request.args and 'password' in request.args:
        username = request.args['username']
        password = request.args['password']

        data = jsonify({'user_id': get_user_id(username, password)})

    resp = make_response(data)
    resp.mimetype = "application/json"
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST', 'GET', 'OPTIONS'
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
