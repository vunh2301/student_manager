from models import Mon_hoc, Lop_hoc, Hoc_sinh, Bang_diem, User
from app import db
from sqlalchemy import func
import hashlib

# Người dùng


def get_user_by_id(user_id):
  print(user_id)
  return User.query.get(user_id)


def auth_user(username, password):
  password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

  return User.query.filter(User.username.__eq__(username),
                           User.password.__eq__(password)).first()


def add_user(name, username, password):
  password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
  u = User(name=name, username=username, password=password)
  db.session.add(u)
  db.session.commit()


# Môn học
def list_mon_hoc():
  return Mon_hoc.query.all()


def get_mon_hoc(id):
  return Mon_hoc.query.get(id)


def add_mon_hoc(name):
  mon = Mon_hoc(name=name)
  db.session.add(mon)
  db.session.commit()
  return None


def update_mon_hoc(id, name):
  mon = get_mon_hoc(id)
  mon.name = name
  db.session.commit()
  return None


def delete_mon_hoc(id):
  mon = get_mon_hoc(id)
  db.session.delete(mon)
  db.session.commit()
  return None


# Lớp học
def list_lop_hoc():
  return db.session\
    .query(Lop_hoc.id, Lop_hoc.name, Lop_hoc.khoi_lop, Lop_hoc.nam_hoc, Lop_hoc.sl_toi_da, func.count(Hoc_sinh.lop_hoc_id))\
    .join(Hoc_sinh, Hoc_sinh.lop_hoc_id.__eq__(Lop_hoc.id), isouter=True)\
    .group_by(Lop_hoc.id).all()


def get_lop_hoc(id):
  return Lop_hoc.query.get(id)


def add_lop_hoc(name, khoi_lop, nam_hoc, sl_toi_da=40):
  lop = Lop_hoc(name=name,
                khoi_lop=khoi_lop,
                nam_hoc=nam_hoc,
                sl_toi_da=sl_toi_da)
  db.session.add(lop)
  db.session.commit()
  return None


def update_lop_hoc(id, name, khoi_lop, nam_hoc, sl_toi_da):
  lop = get_lop_hoc(id)
  lop.name = name
  lop.khoi_lop = khoi_lop
  lop.nam_hoc = nam_hoc
  lop.sl_toi_da = sl_toi_da
  db.session.commit()
  return None


def delete_lop_hoc(id):
  lop = get_lop_hoc(id)
  db.session.delete(lop)
  db.session.commit()
  return None


# Lớp học
def list_hoc_sinh(lop_hoc_id):
  return Hoc_sinh.query.filter_by(lop_hoc_id=lop_hoc_id).all()


def get_hoc_sinh(id):
  return Hoc_sinh.query.get(id)


def add_hoc_sinh(name, lop_hoc_id, gioi_tinh, ngay_sinh, dia_chi, email, sdt):
  hoc_sinh = Hoc_sinh(name=name,
                      lop_hoc_id=lop_hoc_id,
                      gioi_tinh=gioi_tinh,
                      ngay_sinh=ngay_sinh,
                      dia_chi=dia_chi,
                      email=email,
                      sdt=sdt)
  db.session.add(hoc_sinh)
  db.session.commit()
  return None


def update_hoc_sinh(id, name, lop_hoc_id, gioi_tinh, ngay_sinh, dia_chi, email,
                    sdt):
  hoc_sinh = get_hoc_sinh(id)
  hoc_sinh.name = name
  hoc_sinh.lop_hoc_id = lop_hoc_id
  hoc_sinh.gioi_tinh = gioi_tinh
  hoc_sinh.ngay_sinh = ngay_sinh
  hoc_sinh.dia_chi = dia_chi
  hoc_sinh.email = email
  hoc_sinh.sdt = sdt
  db.session.commit()
  return None


def delete_hoc_sinh(id):
  hoc_sinh = get_hoc_sinh(id)
  db.session.delete(hoc_sinh)
  db.session.commit()
  return None
