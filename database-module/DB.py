import datetime
import json

from getmac import get_mac_address as gma

import getpass

import secrets

import cryptocode

from Crypto.PublicKey import RSA

from Crypto.Cipher import PKCS1_OAEP

from playhouse.apsw_ext import *

db_proxy = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = db_proxy


class User(BaseModel):
    id = AutoField()
    name = CharField()
    passw = TextField()
    token = TextField()
    encK = CharField()


class Tweet(BaseModel):
    content = CharField(null=False)
    timestamp = DateTimeField(default=datetime.datetime.now, null=False)
    likes = BigIntegerField(default=0, constraints=[Check('likes>=0')], null=False)
    user_id = ForeignKeyField(User, backref='tweets', constraints=[Check('user_id>=0')], null=False)
    ret_id = IntegerField(null=True, default=None)


class Friends(BaseModel):
    user_id = ForeignKeyField(User, backref='friends', constraints=[Check('user_id>=0')], null=False)
    friend_id = ForeignKeyField(User, backref='friends2', constraints=[Check('friend_id>=0')], null=False)


class Likes(BaseModel):
    origin_user_id = IntegerField(constraints=[Check('origin_user_id>=0')], null=False)
    tweet_id = IntegerField(constraints=[Check('tweet_id>=0')], null=False)
    user_id = ForeignKeyField(User, backref='tweets', constraints=[Check('user_id>=0')], null=False)


def create_db(initial_id: int = 1):
    db = APSWDatabase('DB1')
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


def user_register(name, password: str):
    db = db_connect()
    user = User.select().where(User.name == name)
    if (len(user) > 0):
        return False
    new_passw = cryptocode.encrypt(secrets.token_urlsafe(20), password)
    User.create(name=name, passw=new_passw, token=secrets.token_urlsafe(5), enck=secrets.token_urlsafe(5))
    user = User.get(User.name == name)
    user[0].token = token_creation(user[0].id, str(user[0].id) + new_passw)
    user.save()
    user[0].encK = cryptocode.encrypt(user[0].encK,
                                      cryptocode.decrypt(str(user[0].id) + user[0].token, str(user[0].id + new_passw)))
    user.save()
    db.close()
    return True


def user_login(name, password):
    db = db_connect()
    user = User.select().where(User.name == name)
    if len(user) < 0:
        return False
    passw = cryptocode.decrypt(user[0].passw, password)

    if passw is False:
        return False

    tok = cryptocode.decrypt(user[0].token, password)

    if tok is False:
        user[0].token = token_creation(user[0].id, str(user[0].id + passw))
        user[0].encK = cryptocode.encrypt(user[0].encK,
                                          cryptocode.decrypt(str(user[0].id) + user[0].token, str(user[0].id + passw)))

    db.close()

    return True


def tweet(user_id: int, text, ret_id=0, db_name: str = 'DB1'):
    db = db_connect(db_name)
    user = User.filter(User.id == user_id)
    Tweet.create(text=text, user_id=user[0].id, ret_id=ret_id)
    db.close()


def like(user_id, tweet_id, tweet_user_id, db_name: str = 'DB1'):
    db = db_connect(db_name)
    dislike = False
    if len(Likes.filter(
            Likes.origin_user_id == user_id and Likes.tweet_id == tweet_id and Likes.user_id == tweet_user_id)) != 0:
        dislike = True
    try:
        tweet = Tweet.get(Tweet.id == tweet_id and Tweet.user_id == user_id)
        Tweet.update(likes=Tweet.likes + 1 if not dislike else -1).where(Tweet.id == tweet_id and Tweet.user_id == user_id).execute()
    except:
        return False
    db.close()
    return True


def execute_order(json_file):
    json_f = json.load(json_file)
    order = json_f[0]
    if order is 0:
        return user_register(json_f[1], json_f[2])

    if order is 1:
        return user_login(json_f[1], json_f[2])

    if order is 2:
        return tweet(json_f[1], json_f[2], json_f[3])


create_db(2000)
