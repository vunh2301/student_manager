from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from app import db, app
from flask_login import UserMixin
from sqlalchemy.orm import relationship


# Define Model
class User(db.Model, UserMixin):
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(100), nullable=False)
  username = Column(String(50), nullable=False, unique=True)
  password = Column(String(100), nullable=False)
  user_role = Column(String(20), default='USER')

  def __str__(self):
    return self.name


class Mon_hoc(db.Model):
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(50))

  def __str__(self):
    return self.name


class Lop_hoc(db.Model):
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(50))
  khoi_lop = Column(Integer)
  nam_hoc = Column(Integer)
  sl_toi_da = Column(Integer, default=40)

  def __str__(self):
    return self.name


class Hoc_sinh(db.Model):
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(50))
  lop_hoc_id = Column(Integer, ForeignKey(Lop_hoc.id))
  gioi_tinh = Column(String(50))
  ngay_sinh = Column(DateTime)
  dia_chi = Column(String(50))
  email = Column(String(50))
  sdt = Column(String(50))
  lop_hoc_detail = relationship('Lop_hoc', backref='hoc_sinh', lazy=True)

  def __str__(self):
    return self.name


class Bang_diem(db.Model):
  id = Column(Integer, primary_key=True, autoincrement=True)
  nam_hoc = Column(Integer)
  mon_hoc = Column(String(50))
  student_id = Column(Integer)
  kh1 = Column(Integer)
  kh1_15p = Column(Integer)
  kh1_45p = Column(Integer)
  kh2 = Column(Integer)
  kh2_15p = Column(Integer)
  kh2_45p = Column(Integer)

  def __str__(self):
    return self.name


if __name__ == '__main__':
  with app.app_context():
    db.create_all()
    # import hashlib
    # u1 = User(username='admin',
    #           password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
    #           name='Administrator')
    # db.session.add_all([u1])
    # db.session.commit()
