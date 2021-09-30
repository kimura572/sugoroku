from datetime import datetime

from sqlalchemy.sql.sqltypes import Integer
 
from db import Base
 
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.dialects.mysql import INTEGER, BOOLEAN
 
import hashlib
 
SQLITE3_NAME = "./db.sqlite3"
 
 
class User(Base):
    """
    Userテーブル
 
    id       : 主キー
    username : ユーザネーム
    """
    __tablename__ = 'user'
    id = Column(
        'id',
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )
    username = Column('username', String(256))

    def __init__(self, username):
        self.username = username
 
    def __str__(self):
        return str(self.id) + ':' + self.username
 
 
class Task(Base):
    """
    toDoタスク
 
    id       : 主キー
    user_id  : 外部キー
    username : ユーザネーム
    position : 現在地
    remain : 残り
    """
    __tablename__ = 'task'
    id = Column(
        'id',
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )
 
    user_id = Column('user_id', ForeignKey('user.id'))
    user_name = Column('user_name', String(256))
    position = Column('position', Integer)
    remain = Column('remain', Integer)
 
    def __init__(self, user_id: int, user_name: str, position: int, remain: int):
        self.user_id = user_id
        self.user_name = user_name
        self.position = position
        self.remain = remain
 
    def __str__(self):
        return str(self.id) + \
               ': user_id -> ' + str(self.user_id) + \
               ': user_name -> ' + str(self.user_name) + \
               ', position -> ' + str(self.position) + \
               ', remain -> ' + str(self.remain)