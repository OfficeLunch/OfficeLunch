import datetime
from officelunch_api import db

class User(db.Document):
    name = db.StringField(max_length=255, required=True)
    email = db.EmailField(required=True)
    password = db.StringField(max_length=255, required=True)
    phone = db.IntField() #Does this need to be required? This will need to be checked somewhere else in the application since there is no mongo field for phone numbers
    userid = db.IntField(required=True)
    member_of = db.ListField(db.IntField) #list of lgids that the user belongs to

class Lgroup(db.Document):
    name = db.StringField(max_length=255, required=True)
    lgid = db.IntField(required=True)
    users = db.ListField(db.DictField(), required=True) #TODO this will be a more complex list, currently just holds a list of strings
    origin = db.DictField(required=True) #This will be a python dictionary storing lat/long
    tags = db.ListField(db.StringField(max_length=255), required=True)
    dest_list = db.ListField(db.DictField()) #This is a list of dictionaries holding lat/long and # of votes
    final_dest = db.DictField() #dictionary with lat/long of voting winner
    admin = db.IntField(required=True) #id of the group admin
    start_time = db.DateTimeField(default=datetime.datetime.now, required=True)
    end_time = db.DateTimeField()#end date of the event
