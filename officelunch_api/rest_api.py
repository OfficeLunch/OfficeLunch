# Author:       Clinton Beasley
# Date:         April 16, 2016
# Name:         rest_api.py
# Description:  REST API for Office Lunch

from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_cors import CORS
from flask_mongoengine import MongoEngine

import datetime

app = Flask(__name__)
CORS(app, resources=r'/api/*', headers='Content-Type')
# app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MONGODB_SETTINGS'] = {'db': 'officelunch'}

db = MongoEngine(app)


class User(db.Document):
    name = db.StringField(max_length=255, required=True)
    email = db.EmailField(required=True)
    password = db.StringField(max_length=255, required=True)
    phone = db.StringField()  # Does this need to be required? This will need to be checked somewhere else in the application since there is no mongo field for phone numbers
    userid = db.StringField(max_length=255, required=True)
    member_of = db.ListField(db.StringField())  # list of lgids that the user belongs to


class Lgroup(db.Document):
    name = db.StringField(max_length=255, required=True)
    lgid = db.StringField(required=True)
    users = db.ListField(db.DictField(), required=True)
    origin = db.DictField(required=True)  # This will be a python dictionary storing lat/long
    tags = db.ListField(db.StringField(max_length=255), required=True)
    dest_list = db.ListField(db.DictField())  # This is a list of dictionaries holding lat/long and # of votes
    final_dest = db.DictField()  # dictionary with lat/long of voting winner
    admin = db.StringField(max_length=255, required=True) # id of the group admin
    start_time = db.DateTimeField(default=datetime.datetime.now, required=True)
    end_time = db.DateTimeField()  # end date of the event


def auth_user(usr_email, pwd):

    user = User.objects(email=usr_email, password=pwd)

    if not user:
        return {"exists": "no"}
    else:
        return user[0]


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/api/login', methods=['GET'])
def get_login():
    data = ''
    if 'username' in request.args and 'password' in request.args:
        username = request.args['username']
        password = request.args['password']

        user = auth_user(username, password)
        data = jsonify({'user': user})

    resp = make_response(data)
    resp.mimetype = "application/json"
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST', 'GET', 'OPTIONS'
    return resp


# Lunch Group information
@app.route('/api/groups', methods=['GET'])
def get_lunch_groups():
    # Get a list of all groups
    if not Lgroup.objects:
        # Database empty
        return {}

    grp_lst = []
    for grp in Lgroup.objects:
        grp_lst.append(grp)

    data = jsonify({'group_list': grp_lst})

    resp = make_response(data)
    resp.mimetype = "application/json"
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST', 'GET', 'OPTIONS'
    return resp


@app.route('/api/group_by_name/<string:name>', methods=['GET'])
def get_lunch_group_by_name(name):
    # Get a group by name
    group = Lgroup.objects(name=name)

    if not group:
        data = jsonify({"exists": "no"})
    else:
        data = jsonify({"group": group[0]})

    resp = make_response(data)
    resp.mimetype = "application/json"
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST', 'GET', 'OPTIONS'
    return resp


@app.route('/api/group/<string:gid>', methods=['GET'])
def get_lunch_group(gid):
    # Get a group by ID
    group = Lgroup.objects(lgid=gid)

    if not group:
        data = jsonify({"exists": "no"})
    else:
        data = jsonify({"group": group[0]})

    resp = make_response(data)
    resp.mimetype = "application/json"
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST', 'GET', 'OPTIONS'
    return resp


@app.route('/api/group', methods=['POST'])
def post_lunch_group():
    # Create a new lunch group
    if not request.json or'email' not in request.json:
        abort(400)
    group = {
        "name": request.json['name'] if request.json['name'] != -1 else "",
        "lgid": str(int(Lgroup.objects[-1].lgid) + 1),
        "users": request.json['users'] if request.json['users'] != -1 else [],
        "origin": request.json['origin'] if request.json['origin'] != -1 else {},
        "tags": request.json['tags'] if request.json['tags'] != -1 else [],
        "dest_list": request.json['dest_list'] if request.json['dest_list'] != -1 else [],
        "final_dest": request.json['final_dest'] if request.json['final_dest'] != -1else [],
        "admin": request.json['admin'] if request.json['admin'] != -1 else "",
        "start_time": request.json['start_time'] if request.json['start_time'] != -1 else "",
        "end_time:": request.json['end_time'] if request.json['end_time'] != -1 else ""
    }

    post = Lgroup(group)
    post.save()
    return jsonify({'group': group}), 201


@app.route('/api/group/<string:gid>/name', methods=['GET'])
def get_group_name(gid):
    # Get a group name by ID
    group = Lgroup.objects(lgid=gid)

    if not group:
        data = jsonify({"exists": "no"})
    else:
        data = jsonify({"name": group[0].name})

    resp = make_response(data)
    resp.mimetype = "application/json"
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST', 'GET', 'OPTIONS'
    return resp


@app.route('/api/group/<string:gid>/users', methods=['GET'])
def get_group_users(gid):
    # Get a group's users by ID
    group = Lgroup.objects(lgid=gid)

    if not group:
        data = jsonify({"exists": "no"})
    else:
        data = jsonify({"users": group[0].users})

    resp = make_response(data)
    resp.mimetype = "application/json"
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST', 'GET', 'OPTIONS'
    return resp


@app.route('/api/group/<string:gid>/origin', methods=['GET'])
def get_group_origin(gid):
    # Get a group's origin by ID
    group = Lgroup.objects(lgid=gid)

    if not group:
        data = jsonify({"exists": "no"})
    else:
        data = jsonify({"origin": group[0].origin})

    resp = make_response(data)
    resp.mimetype = "application/json"
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST', 'GET', 'OPTIONS'
    return resp


@app.route('/api/group/<string:gid>/tags', methods=['GET'])
def get_group_tags(gid):
    # Get a group's tags by ID
    group = Lgroup.objects(lgid=gid)

    if not group:
        data = jsonify({"exists": "no"})
    else:
        data = jsonify({"tags": group[0].tags})

    resp = make_response(data)
    resp.mimetype = "application/json"
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST', 'GET', 'OPTIONS'
    return resp


@app.route('/api/group/<string:gid>/dest_list', methods=['GET'])
def get_group_dest_list(gid):
    # Get a group's destination list by ID
    group = Lgroup.objects(lgid=gid)

    if not group:
        data = jsonify({"exists": "no"})
    else:
        data = jsonify({"dest_list": group[0].dest_list})

    resp = make_response(data)
    resp.mimetype = "application/json"
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST', 'GET', 'OPTIONS'
    return resp


@app.route('/api/group/<string:gid>/final_dest', methods=['GET'])
def get_group_final_dest(gid):
    # Get a group's final destination by ID
    group = Lgroup.objects(lgid=gid)

    if not group:
        data = jsonify({"exists": "no"})
    else:
        data = jsonify({"final_dest": group[0].final_dest})

    resp = make_response(data)
    resp.mimetype = "application/json"
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST', 'GET', 'OPTIONS'
    return resp


@app.route('/api/group/<string:gid>/admin', methods=['GET'])
def get_group_admin(gid):
    # Get a group's admin
    group = Lgroup.objects(lgid=gid)

    if not group:
        data = jsonify({"exists": "no"})
    else:
        data = jsonify({"admin": group[0].admin})

    resp = make_response(data)
    resp.mimetype = "application/json"
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST', 'GET', 'OPTIONS'
    return resp


@app.route('/api/group/<string:gid>/start_time', methods=['GET'])
def get_group_start_time(gid):
    # Get a group's start time
    group = Lgroup.objects(lgid=gid)

    if not group:
        data = jsonify({"exists": "no"})
    else:
        data = jsonify({"start_time": group[0].start_time})

    resp = make_response(data)
    resp.mimetype = "application/json"
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST', 'GET', 'OPTIONS'
    return resp


@app.route('/api/group/<string:gid>/end_time', methods=['GET'])
def get_group_end_time(gid):
    # Get a group's end_time
    group = Lgroup.objects(lgid=gid)

    if not group:
        data = jsonify({"exists": "no"})
    else:
        data = jsonify({"end_time": group[0].end_time})

    resp = make_response(data)
    resp.mimetype = "application/json"
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST', 'GET', 'OPTIONS'
    return resp


# User Information
@app.route('/api/users', methods=['GET'])
def get_users():
    # Get a list of all users
    if not User.objects:
        # Database empty
        return {}

    user_lst = []
    for user in User.objects:
        print user
        user_lst.append(user)

    data = jsonify({'users': user_lst})

    resp = make_response(data)
    resp.mimetype = "application/json"
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST', 'GET', 'OPTIONS'
    return resp


@app.route('/api/user_by_email/<string:usr_email>', methods=['GET'])
def get_user_by_email(usr_email):
    # Get a user ID by email
    if not User.objects:
        # Database empty
        return {}

    user = User.objects(email=usr_email)
    data = jsonify({'user': user})

    resp = make_response(data)
    resp.mimetype = "application/json"
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST', 'GET', 'OPTIONS'
    return resp


@app.route('/api/user/<string:uid>', methods=['GET'])
def get_user(uid):
    # Get a user by uid
    if not User.objects:
        # Database empty
        return {}

    user = User.objects(userid=uid)
    data = jsonify({'user': user})

    resp = make_response(data)
    resp.mimetype = "application/json"
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST', 'GET', 'OPTIONS'
    return resp


@app.route('/api/user', methods=['POST'])
def post_user():
    # Create a new lunch group
    if not request.json or'email' not in request.json:
        abort(400)
    user = {
        "name": request.json['name'] if 'name' in request.json else "",
        "email": request.json['email'] if 'email' in request.json else "",
        "password": request.json['password'] if 'password' in request.json else "",
        "phone": request.json['phone'] if 'phone' in request.json else "",
        "uid": str(int(User.objects[-1].uid) + 1),
        "member_of": request.json['member_of'] if 'member_of' in request.json else []
    }

    print user

    post = User(user)
    post.save()
    return jsonify({'user': user}), 201


@app.route('/api/user/<string:uid>/name', methods=['GET'])
def get_user_name(uid):
    # Get a user's name by ID
    user = User.objects(userid=uid)

    if not user:
        data = jsonify({"exists": "no"})
    else:
        data = jsonify({"username": user[0].name})

    resp = make_response(data)
    resp.mimetype = "application/json"
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST', 'GET', 'OPTIONS'
    return resp


@app.route('/api/user/<string:uid>/email', methods=['GET'])
def get_user_email(uid):
    # Get a user's email by ID
    user = User.objects(userid=uid)

    if not user:
        data = jsonify({"exists": "no"})
    else:
        data = jsonify({"email": user[0].email})

    resp = make_response(data)
    resp.mimetype = "application/json"
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST', 'GET', 'OPTIONS'
    return resp


@app.route('/api/user/<string:uid>/phone', methods=['GET'])
def get_user_phone(uid):
    # Get a user's phone number by ID
    user = User.objects(userid=uid)

    if not user:
        data = jsonify({"exists": "no"})
    else:
        data = jsonify({"phone": user[0].phone})

    resp = make_response(data)
    resp.mimetype = "application/json"
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST', 'GET', 'OPTIONS'
    return resp


@app.route('/api/user/<string:uid>/groups', methods=['GET'])
def get_user_groups(uid):
    # Get a user's groups by ID
    user = User.objects(userid=uid)

    if not user:
        data = jsonify({"exists": "no"})
    else:
        data = jsonify({"groups": user[0].member_of})

    resp = make_response(data)
    resp.mimetype = "application/json"
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST', 'GET', 'OPTIONS'
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
