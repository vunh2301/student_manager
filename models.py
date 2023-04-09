from sqlalchemy import MetaData, Table, Column, String, Integer, DateTime

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
entities = Table('entities', meta, Column('id', Integer, primary_key=True),
                 Column('title', Integer), Column('type', String),
                 Column('value', String))
bang_diem = Table('bang_diem', meta, Column('id', Integer, primary_key=True),
                  Column('nam_hoc', Integer), Column('mon_hoc', String),
                  Column('student_id', Integer), Column('kh1', Integer),
                  Column('kh1_15p', Integer), Column('kh1_45p', Integer),
                  Column('kh2', Integer), Column('kh2_15p', Integer),
                  Column('kh2_45p', Integer))

mon_hoc = Table('mon_hoc', meta, Column('id', Integer, primary_key=True),
                Column('name', Integer))

lop_hoc = Table('lop_hoc', meta, Column('id', Integer, primary_key=True),
                Column('name', String), Column('khoi_lop', Integer),
                Column('nam_hoc', Integer))

hoc_sinh = Table('hoc_sinh', meta, Column('id', Integer, primary_key=True),
                 Column('name', String), Column('lop_hoc_id', Integer),
                 Column('gioi_tinh', String), Column('ngay_sinh', DateTime),
                 Column('dia_chi', String), Column('email', String),
                 Column('sdt', String))
