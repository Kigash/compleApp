from peewee import *
db = PostgresqlDatabase('complete',user='postgres',host='localhost',password='33408828')
class Lecture(Model):
    course = CharField()
    unit = CharField()
    date = DateField()
    status = BooleanField(default=False)
    user_id = IntegerField()
    start_time = TimeField()
    end_time = TimeField()
    department = CharField()
    lecturer = CharField()
    unit_code = CharField()
    class Meta:
        table_name = "lectures"
        database = db
Lecture.create_table(fail_silently=True)
