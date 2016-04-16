import datetime
from officelunch_api import db

class User(db.Document):
    name = db.StringField(max_length=255, required=True)
    email = db.EmailField(required=True)
    password = db.StringField(max_length=255, required=True)
    phone = db.StringField() #Does this need to be required? This will need to be checked somewhere else in the application since there is no mongo field for phone numbers
    userid = db.StringField(max_length=255, required=True)
    member_of = db.ListField(db.StringField()) #list of lgids that the user belongs to

class Lgroup(db.Document):
    name = db.StringField(max_length=255, required=True)
    lgid = db.StringField(required=True)
    users = db.ListField(db.DictField(), required=True)
    origin = db.DictField(required=True) #This will be a python dictionary storing lat/long
    tags = db.ListField(db.StringField(max_length=255), required=True)
    dest_list = db.ListField(db.DictField()) #This is a list of dictionaries holding lat/long and # of votes
    final_dest = db.DictField() #dictionary with lat/long of voting winner
    admin = db.StringField(max_length=255, required=True) #id of the group admin
    start_time = db.DateTimeField(default=datetime.datetime.now, required=True)
    end_time = db.DateTimeField()#end date of the event
