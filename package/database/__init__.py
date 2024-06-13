from peewee import (
    TextField,
    Model,
    IntegerField,
    SqliteDatabase,
    ForeignKeyField,
    BooleanField, FloatField
)

from pathlib import Path
from os import getcwd


path = Path(getcwd()).joinpath('odds_portal_db.db')
db = SqliteDatabase(path)
print(path)


class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):
    user_id = IntegerField(primary_key=True, null=False)


class LinksBetters(BaseModel):
    user = ForeignKeyField(Users)
    better_nickname = TextField(default='', null=False)
    link = TextField(default='', null=False)
    keyword = TextField(default='', null=True)
    current_better = BooleanField(default=False)
    on_off = BooleanField(default=False)
    roi = IntegerField(default=-1111)


class BetControl(BaseModel):
    eg_or_rus = TextField(default='')
    scaner_name = TextField(default='')
    bettors_name = TextField(default='')
    timeStart = TextField(default='')
    players = TextField(default='')
    bet = TextField(default='')
    coefficient = FloatField(default=0)
    sport = IntegerField(default=0)


def init():
    Users.create_table(safe=True)
    LinksBetters.create_table(safe=True)
    BetControl.create_table(safe=True)