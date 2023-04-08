from sqlalchemy import MetaData, Table, Column, String, Integer

meta = MetaData()

students = Table(
  'students',
  meta,
  Column('id', Integer, primary_key=True),
  Column('name', String),
  Column('gender', String),
  Column('brithday', String),
  Column('address', String),
)

classes = Table('classes', meta, Column('id', Integer, primary_key=True),
                Column('name', Integer), Column('grade', String))
