# Author:       Clinton Beasley
# Date:         April 16, 2016
# Name:         rest_api.py
# Description:  REST API for Office Lunch

from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_cors import CORS
from flask_mongoengine import MongoEngine


app = Flask(__name__)
CORS(app, resources=r'/api/*', headers='Content-Type')
# app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MONGODB_SETTINGS'] = {'db': 'officelunch'}

db = MongoEngine(app)

from models import User
from models import Lgroup

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


# Lunch Group information
def get_lunch_groups():
    # TODO: Get a list of all groups
    pass


def get_lunch_group_by_name(name):
    # TODO: Get a group by name
    pass


def get_lunch_group(gid):
    # TODO: Get a group by ID
    pass


def get_group_name(gid):
    # TODO: Get a group name by ID
    pass


def get_group_users(gid):
    # TODO: Get a group's users by ID
    pass


def get_group_origin(gid):
    # TODO: Get a group's origin by ID
    pass


def get_group_tags(gid):
    # TODO: Get a group's tags by ID
    pass


def group_dest_list(gid):
    # TODO: Get a group's destination list by ID
    pass


def group_final_dest(gid):
    # TODO: Get a group's final destination by ID
    pass


# User Information
@app.route('/api/users', methods=['GET'])
def get_users():
    # TODO: Get a list of all users
    for user in User.objects:
        print jsonify(user)
    pass


def get_user_by_email(email):
    # TODO: Get a user ID by email
    pass


def get_user_name(uid):
    # TODO: Get a user's name by ID
    pass

def get_user_email(uid):
    # TODO: Get a user's email by ID
    pass


def get_user_phone(uid):
    # TODO: Get a user's phone number by ID
    pass


def get_user_groups(uid):
    # TODO: Get a user's groups by ID
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
