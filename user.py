from peewee import *
try:
    db=PostgresqlDatabase('complete',user='postgres',host='localhost',password='33408828')
    print('successfully connected')
except:
    print('unsuccessful connection')

class User(Model):
    names = CharField()
    reg_no = CharField(unique=True)
    email = CharField(unique=True)
    dob = DateField()
    password = CharField()
    course = CharField()
    department = CharField()
    phone_no = IntegerField()
    address = CharField()
    role = CharField()
    class Meta:
        table_name = "users"
        database = db


User.create_table(fail_silently=True)

