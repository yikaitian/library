# -*- coding: utf-8 -*-

from peewee import MySQLDatabase, Model, CharField, IntegerField,  DateTimeField
import json
from conf.config import config
import os

cfg = config[os.getenv('FLASK_CONFIG') or 'default']

db = MySQLDatabase(host=cfg.DB_HOST, user=cfg.DB_USER, passwd=cfg.DB_PASSWD, database=cfg.DB_DATABASE)


class BaseModel(Model):
    class Meta:
        database = db

    def __str__(self):
        r = {}
        for k in self.__data__.keys():
            try:
                r[k] = str(getattr(self, k))
            except:
                r[k] = json.dumps(getattr(self, k))
        # return str(r)
        return json.dumps(r, ensure_ascii=False)



class Publisher(BaseModel):
    Name = CharField(primary_key=True)
    Address = CharField()
    Phone = CharField()


class Author(BaseModel):
    AuthorId = IntegerField(primary_key=True)
    AuthorName = CharField()


class Book(BaseModel):
    BookId = IntegerField(primary_key=True)
    Title = CharField()
    PublisherName = CharField()
    Author = CharField()


class LibraryBranch(BaseModel):
    BranchId = IntegerField(primary_key=True)
    BranchName = CharField()
    Address = ()

    class Meta:
        table_name = "library_branch"


class BookCopies(BaseModel):
    BookId = IntegerField(primary_key=True)
    BranchId = IntegerField()
    No_Of_Copies = IntegerField()

    class Meta:
        table_name = "book_copies"


class BookLoans(BaseModel):
    BookId = IntegerField(primary_key=True)
    BranchId = IntegerField()
    CardNo = IntegerField()
    DateOut = DateTimeField()
    DueDate = DateTimeField()
    returned = IntegerField()

    class Meta:
        table_name = "book_loans"


class Borrower(BaseModel):
    CardNo = IntegerField(primary_key=True)
    Name = CharField()
    Address = CharField()
    Phone = CharField()


# 建表
def create_table():
    db.connect()
    db.create_tables([Publisher, Author, Borrower, BookLoans, Book, BookCopies, Publisher,])


if __name__ == '__main__':
    create_table()
