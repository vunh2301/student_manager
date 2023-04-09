from models import students, entities, mon_hoc, bang_diem, lop_hoc, hoc_sinh
from app import conn, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()


def get_students():
  select = students.select()
  result = conn.execute(select).fetchall()
  return result


def add_student(name, gender, brithday, address):
  insert = students.insert().values(name=name,
                                    gender=gender,
                                    brithday=brithday,
                                    address=address)
  result = conn.execute(insert)
  insert_bang_diem = bang_diem.insert().values(
    nam_hoc=2023, mon_hoc='Môn A', student_id=result.inserted_primary_key)
  result_bang_diem = conn.execute(insert_bang_diem)
  print(result_bang_diem)
  return result.inserted_primary_key


def delete_student(id):
  delete = students.delete().where(students.c.id == id)
  result = conn.execute(delete)
  return result


def update_student(id, name, gender, brithday, address):
  update = students.update().where(students.c.id == id).values(
    name=name, gender=gender, brithday=brithday, address=address)
  result = conn.execute(update)
  print(result)
  return result


def get_entities(type):
  select = entities.select().where(entities.c.type == type)
  result = conn.execute(select).fetchall()
  return result


def add_entities(type, title, value):
  insert = entities.insert().values(type=type, title=title, value=value)
  result = conn.execute(insert)
  return result


def update_entities(id, type, title, value):
  update = entities.update().where(entities.c.id == id).values(type=type,
                                                               title=title,
                                                               value=value)
  result = conn.execute(update)
  return result


def delete_entities(id):
  delete = entities.delete().where(students.c.id == id)
  result = conn.execute(delete)
  return result


def list_mon_hoc():
  select = mon_hoc.select()
  result = conn.execute(select).fetchall()
  return result


def add_mon_hoc(name):
  insert = mon_hoc.insert().values(name=name)
  result = conn.execute(insert)
  return result


def update_mon_hoc(id, name):
  update = mon_hoc.update().where(mon_hoc.c.id == id).values(name=name)
  result = conn.execute(update)
  return result


def delete_mon_hoc(id):
  delete = mon_hoc.delete().where(mon_hoc.c.id == id)
  result = conn.execute(delete)
  return result


# lop hoc
def list_lop_hoc():
  select = lop_hoc.select()
  result = conn.execute(select).fetchall()
  return result


def get_lop_hoc(id):
  select = lop_hoc.select().where(lop_hoc.c.id == id)
  result = conn.execute(select).fetchone()
  return result


def add_lop_hoc(name, khoi_lop, nam_hoc):
  insert = lop_hoc.insert().values(name=name,
                                   khoi_lop=khoi_lop,
                                   nam_hoc=nam_hoc)
  result = conn.execute(insert)
  return result


def update_lop_hoc(id, name, khoi_lop, nam_hoc):
  update = lop_hoc.update().where(lop_hoc.c.id == id).values(name=name,
                                                             khoi_lop=khoi_lop,
                                                             nam_hoc=nam_hoc)
  result = conn.execute(update)
  return result


def delete_lop_hoc(id):
  delete = lop_hoc.delete().where(lop_hoc.c.id == id)
  result = conn.execute(delete)
  return result

# hoc sinh
def list_hoc_sinh(lop_hoc_id):
  select = hoc_sinh.select().where(hoc_sinh.c.lop_hoc_id == lop_hoc_id)
  result = conn.execute(select)
  return result