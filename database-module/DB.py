import datetime
import json
from datetime import datetime

from getmac import get_mac_address as gma

import getpass

import secrets

import cryptocode

from Crypto.PublicKey import RSA

from Crypto.Cipher import PKCS1_OAEP

from playhouse.apsw_ext import *
from playhouse.shortcuts import model_to_dict
from playhouse.sqlite_ext import basestring

db_proxy = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = db_proxy


class User(BaseModel):
    id = BigIntegerField(primary_key=True)
    name = CharField(null=None, constraints=[Check('len(name)<=8')])
    passw = TextField()
    token = TextField()
    encK = CharField(null=True)


class Tweet(BaseModel):
    content = CharField(null=False)
    timestamp = DateTimeField(default=datetime.now, null=False)
    likes = BigIntegerField(default=0, constraints=[Check('likes>=0')], null=False)
    user_id = ForeignKeyField(User, backref='tweets', constraints=[Check('user_id>=0')], null=False)
    ret_id = IntegerField(null=True, default=0)
    ret_user_id = ForeignKeyField(User, backref='tweets', constraints=[Check('user_id>=0')], default=0)
    ret_user_name = CharField(default=None)


class Friends(BaseModel):
    user_id = ForeignKeyField(User, backref='friends', constraints=[Check('user_id>=0')], null=False)
    friend_id = ForeignKeyField(User, backref='friends2', constraints=[Check('friend_id>=0')], null=False)


class Likes(BaseModel):
    origin_user_id = IntegerField(constraints=[Check('origin_user_id>=0')], null=False)
    tweet_id = IntegerField(constraints=[Check('tweet_id>=0')], null=False)
    user_id = ForeignKeyField(User, backref='tweets', constraints=[Check('user_id>=0')], null=False)


def create_db(name: str = 'DB1', initial_id: int = 1):
    db = APSWDatabase(name)
    db_proxy.initialize(db)
    db.connect()
    db.create_tables([User, Tweet, Friends, Likes])

    new_passw = secrets.token_urlsafe(20)
    key = RSA.generate(2048)
    encrypted_key = key.export_key(passphrase=new_passw, pkcs=8,
                                   protection="scryptAndAES256-CBC")
    file_out = open("receiver.pem", "wb")
    file_out.write(encrypted_key)
    file_out.close()

    str_encoded = cryptocode.encrypt(new_passw, getpass.getuser() + str(gma()) + str(initial_id))
    User.create(id=initial_id, name='foo', passw=str_encoded, token=token_creation(initial_id, new_passw),
                encK=secrets.token_urlsafe(5))
    user = User.select().limit(1)
    user[0].encK = cryptocode.encrypt(user[0].encK, str(user[0].id) + str(user[0].token))
    user[0].save()
    db.close()

    return db


def db_connect(db_name: str = 'DB1'):
    db = APSWDatabase(db_name)
    db_proxy.initialize(db)
    db.connect()

    return db


def get_token(id: int, passw: str):
    user = User.select().where(User.id == id)
    if len(user) < 0:
        return None
    passw = cryptocode.decrypt(user[0].passw, passw)

    if passw is False:
        return None

    tok = cryptocode.decrypt(user[0].token, passw)
    return tok


def token_creation(id: int, passw):
    token = str(secrets.token_urlsafe(10)) + str(id)
    tok_encoded = cryptocode.encrypt(token, passw)
    return tok_encoded


def user_register(name, password: str, user_id: int, db_name: str = 'DB1'):
    db = db_connect(db_name)
    user = User.select().where(User.name == name)
    if (len(user) > 0):
        return False
    new_passw = cryptocode.encrypt(secrets.token_urlsafe(20), password)
    User.create(id=user_id, name=name, passw=new_passw, token=secrets.token_urlsafe(5), encK=secrets.token_urlsafe(5))
    user = User.get(User.name == name)
    user[0].token = token_creation(user[0].id, str(user[0].id) + new_passw)
    user.save()
    user[0].encK = cryptocode.encrypt(user[0].encK,
                                      cryptocode.decrypt(str(user[0].id) + user[0].token, str(user[0].id + new_passw)))
    user.save()
    db.close()
    return True


def user_login(name, password, user_id=None, db_name: str = 'DB1'):
    db = db_connect(db_name)
    if (user_id is None):
        user = User.select().where(User.name == name)
    else:
        try:
            user = User.get_by_id(user_id)
            if (user[0].name != name):
                return False
        except:
            return False

    if len(user) < 0:
        return (False, 0)
    passw = cryptocode.decrypt(user[0].passw, password)

    if passw is False:
        return (False, 0)

    tok = cryptocode.decrypt(user[0].token, password)

    if tok is False:
        tok = token_creation(user[0].id, str(user[0].id + passw))
        user[0].token = tok
        user[0].encK = cryptocode.encrypt(user[0].encK,
                                          cryptocode.decrypt(str(user[0].id) + user[0].token, str(user[0].id + passw)))
    db.close()

    return (True, tok)


def follow(user_id, followed_id, db_name: str = 'DB1'):
    db = db_connect(db_name)
    Friends.get_or_create(user_id=user_id, friend_id=followed_id)
    db.close()
    return True


def like(user_id, tweet_id, tweet_user_id, db_name: str = 'DB1'):
    db = db_connect(db_name)
    dislike = False
    if len(Likes.filter(
            Likes.origin_user_id == user_id and Likes.tweet_id == tweet_id and Likes.user_id == tweet_user_id)) != 0:
        dislike = True
    try:
        tweet = Tweet.get(Tweet.id == tweet_id and Tweet.user_id == user_id)
        Tweet.update(likes=Tweet.likes + 1 if not dislike else -1).where(
            Tweet.id == tweet_id and Tweet.user_id == user_id).execute()
    except:
        return False
    db.close()
    return True


def get_random_tweets(quantity: int, db_name='DB1'):
    db = db_connect(db_name)
    answ = Tweet.select().order_by(fn.Random()).limit(quantity)
    db.close()
    return answ


def get_followed_updated_tweets(followed_id_list, db_name: str = 'DB1'):
    followed_tweets = Tweet.Select().where(Tweet.ret_user_id.in_(followed_id_list))
    followed_tweets = followed_tweets.having(fn.COUNT(Tweet.user_id) == 10)
    return followed_tweets


def tweet(user_id: int, text, ret_id=0, db_name: str = 'DB1'):
    db = db_connect(db_name)
    user = User.filter(User.id == user_id)
    Tweet.create(content=text, user_id=user[0].id, ret_id=ret_id)
    db.close()
    return True


def execute_order(json_file):
    json_f = json.load(json_file)
    order = json_f[0]
    if order == 0:
        return user_register(json_f[1], json_f[2], json_f[3], json_f[4] if len(json_f) == 5 else 'DB1')

    elif order == 1:
        return user_login(json_f[1], json_f[2], json_f[3] if len(json_f) >= 4 else 'DB1',
                          json_f[4] if len(json_f) == 5 else 'DB1')

    elif order == 2:
        return tweet(json_f[1], json_f[2], json_f[3], json_f[4] if len(json_f) == 5 else 'DB1')

    elif order == 3:
        return like(json_f[1], json_f[2], json_f[3], json_f[4] if len(json_f) == 5 else 'DB1')

    elif order == 4:
        return get_followed_updated_tweets(json_f[1], json_f[2] if len(json_f) == 3 else 'DB1')

    elif order == 5:
        return get_random_tweets(json_f[1], json_f[2] if len(json_f) == 3 else 'DB1')

    elif order == 6:
        return follow(json_f[1], json_f[2] if len(json_f) == 3 else 'DB1')


"""------------------------Utils---------------------------------"""


def get_user_name(user_id, db_name: str = 'DB1'):
    db = db_connect(db_name)
    answ = User.get_by_id(user_id)[0].name
    db.close()
    return answ


def get_friends(user_id, db_name: str = 'DB1'):
    db = db_connect(db_name)
    answ = Friends.select(Friends.friend_id).where(Friends.user_id == user_id)
    db.close()
    r_answ = []
    for element in answ:
        r_answ.append(r_answ[0].friend_id)
    return answ


def user_exist_name(name):
    db = db_connect()
    try:
        User.get(name == name)
        return True
    except:
        return False
    finally:
        db.close()


def user_exist(user_id):
    db = db_connect()
    try:
        User.get_by_id(user_id)
        return True
    except:
        return False
    finally:
        db.close()


def load_with_datetime(pairs, format='%Y-%m-%dT%H:%M:%S.%f'):
    """Load with date and time"""
    d = {}
    for k, v in pairs:
        if isinstance(v, str):
            try:
                d[k] = datetime.strptime(v, format).date()
            except ValueError:
                d[k] = v
        else:
            d[k] = v
    return d


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    try:
        if isinstance(obj, (datetime, datetime.date)):
            return obj.isoformat()
        raise TypeError("Type %s not serializable" % type(obj))
    except:
        pass


def export_models_to_json(model: Model):
    return json.dumps([model], default=json_serial)


def export_databse_to_json(db_name='DB1'):
    db = db_connect(db_name)
    user = list(User.select().dicts())
    tweet_ = list(Tweet.select().dicts())
    friends_ = list(Friends.select().dicts())
    likes_ = list(Likes.select().dicts())
    db.close()

    return json.dumps([user, tweet_, friends_, likes_], default=json_serial)


def load_json_to_database(json_string, db_name='DB1', tables=None):
    arra = json.loads(json_string, object_pairs_hook=load_with_datetime)
    db = db_connect(db_name)
    tables = [User, Tweet, Friends, Likes] if tables is None else tables
    count = 0
    with db.atomic():
        for element in arra:
            for idx in range(0, len(element), 100):
                tables[count].insert_many(element[idx:idx + 100]).on_conflict_ignore().execute()
            count += 1
    db.close()


