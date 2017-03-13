from datetime import datetime
from tinydb import TinyDB, Query
from tinydb_serialization import Serializer, SerializationMiddleware

class DateTimeSerializer(Serializer):
    OBJ_CLASS = datetime  # The class this serializer handles

    def encode(self, obj):
        return obj.strftime('%Y-%m-%dT%H:%M:%S')

    def decode(self, s):
        return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')

class Storage:
    def __init__(self):
        serialization = SerializationMiddleware()
        serialization.register_serializer(DateTimeSerializer(), 'TinyDate')

        self.db = TinyDB('db.json', storage=serialization)
        self.users = self.db.table('users')

    def get_user(self, id, default):
        if default is None:
            default = {'id': id, 'name': '', 'last_report': None}

        query = Query()
        user = self.users.get(query.id == id)

        if not user:
            user = default
            self.users.insert(user)

        return user

    def get_users_for_daily_meeting(self):
        query = Query()
        return self.users.search(
            (~ query.last_report.exists()) |
            (query.last_report.test(lambda d:
                                    not d or
                                    d.date() < datetime.today().date()))
        )

    def save_user(self, user):
        if not user and not 'id' in user:
            raise Exception("Not a valid user")

        query = Query()
        self.users.update(user, query.id == user['id'])
