from sqlalchemy import Column, String, Integer, DateTime, func
from app import db, app
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import case


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
  tuoi_toi_thieu = Column(Integer, default=15)
  tuoi_toi_da = Column(Integer, default=20)

  def __str__(self):
    return self.name


class Hoc_sinh(db.Model):
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(50))
  lop_hoc_id = Column(Integer)
  gioi_tinh = Column(String(50))
  ngay_sinh = Column(DateTime)
  dia_chi = Column(String(50))
  email = Column(String(50))
  sdt = Column(String(50))

  def __str__(self):
    return self.name


class Bang_diem(db.Model):
  __tablename__ = 'bang_diem'
  id = Column(Integer, primary_key=True, autoincrement=True)
  nam_hoc = Column(Integer)
  mon_hoc_id = Column(Integer)
  hoc_sinh_id = Column(Integer)
  diem_thi_hk1 = Column(Integer)
  diem_15p_hk1_1 = Column(Integer)
  diem_15p_hk1_2 = Column(Integer)
  diem_15p_hk1_3 = Column(Integer)
  diem_15p_hk1_4 = Column(Integer)
  diem_15p_hk1_5 = Column(Integer)
  diem_45p_hk1_1 = Column(Integer)
  diem_45p_hk1_2 = Column(Integer)
  diem_45p_hk1_3 = Column(Integer)
  dien_trung_binh_hk1 = Column(Integer)
  diem_thi_hk2 = Column(Integer)
  diem_15p_hk2_1 = Column(Integer)
  diem_15p_hk2_2 = Column(Integer)
  diem_15p_hk2_3 = Column(Integer)
  diem_15p_hk2_4 = Column(Integer)
  diem_15p_hk2_5 = Column(Integer)
  diem_45p_hk2_1 = Column(Integer)
  diem_45p_hk2_2 = Column(Integer)
  diem_45p_hk2_3 = Column(Integer)
  dien_trung_binh_hk2 = Column(Integer)

  def __str__(self):
    return self.name


if __name__ == '__main__':
  with app.app_context():
    # db.drop_all()
    db.create_all()
    # import hashlib
    # u1 = User(username='admin',
    #           password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
    #           name='Administrator')
    # db.session.add_all([u1])
    # db.session.commit()
