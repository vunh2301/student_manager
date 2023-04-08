from models import students
from app import conn


def get_students():
  s = students.select()
  result = conn.execute(s).fetchall()
  return result


def add_student(name, gender, brithday, address):
  ins = students.insert().values(name=name,
                                 gender=gender,
                                 brithday=brithday,
                                 address=address)
  result = conn.execute(ins)
  return result.inserted_primary_key


def delete_student(id):
  stmt = students.delete().where(students.c.id == id)
  conn.execute(stmt)
  s = students.select()
  result = conn.execute(s).fetchall()
  print(result)
  return result


def update_student(id, name, gender, brithday, address):
  stmt = students.update().where(students.c.id == id).values(name=name,
                                                             gender=gender,
                                                             brithday=brithday,
                                                             address=address)
  result = conn.execute(stmt)
  print(result)
  return result
