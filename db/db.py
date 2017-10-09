import json
import datetime
from pymongo import MongoClient
from bson import ObjectId


class DB:

    def __init__(self):
        self.db = 'blah'

    def insertUser(self, user):

        user = {
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'apn_token': user['apn_token'],
            'session_token' : user['session_token']
        }

        return self.deserialize(self.db['users'].insert(user))

    # Helpers

    def deserialize(self, object):
        return json.loads(JSONEncoder().encode(object))


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, (datetime.datetime, datetime.date)):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


db = DB()
