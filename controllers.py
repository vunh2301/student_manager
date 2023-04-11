from models import Mon_hoc, Lop_hoc, Hoc_sinh, Bang_diem, User
from app import db
from sqlalchemy import func
from flask import jsonify
import hashlib
import datetime


# Người dùng
def get_current_year():
  today = datetime.date.today()
  return today.year


def get_user_by_id(user_id):
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
def list_mon_hoc(kw=None):
  if kw:
    return Mon_hoc.query.filter(Mon_hoc.name.contains(kw)).all()
  else:
    return Mon_hoc.query.all()


def get_mon_hoc(id):
  return Mon_hoc.query.get(id)


def add_mon_hoc(name):
  mon = Mon_hoc(name=name)
  db.session.add(mon)
  db.session.commit()
  general_bang_diem_for_mon_hoc(mon.id)
  return None


def update_mon_hoc(id, name):
  mon = get_mon_hoc(id)
  mon.name = name
  db.session.commit()
  return None


def delete_mon_hoc(id):
  mon = get_mon_hoc(id)
  db.session.delete(mon)
  db.session.query(Bang_diem).filter(Bang_diem.mon_hoc_id == id).delete()
  db.session.commit()
  return None


# Lớp học


def json_list_lop_hoc():
  return [{
    "id": lop.id,
    "sl_toi_da": lop.sl_toi_da,
    "tuoi_toi_thieu": lop.tuoi_toi_thieu,
    "tuoi_toi_da": lop.tuoi_toi_da,
    "si_so": lop.si_so
  } for lop in db.session\
    .query(Lop_hoc.id, Lop_hoc.sl_toi_da, Lop_hoc.tuoi_toi_thieu, Lop_hoc.tuoi_toi_da, func.count(Hoc_sinh.lop_hoc_id).label('si_so'))\
    .join(Hoc_sinh, Hoc_sinh.lop_hoc_id.__eq__(Lop_hoc.id), isouter=True)\
    .group_by(Lop_hoc.id).all()]


def list_lop_hoc():
  return db.session\
    .query(Lop_hoc.id, Lop_hoc.name, Lop_hoc.khoi_lop, Lop_hoc.nam_hoc, Lop_hoc.sl_toi_da, Lop_hoc.tuoi_toi_thieu, Lop_hoc.tuoi_toi_da, func.count(Hoc_sinh.lop_hoc_id).label('si_so'))\
    .join(Hoc_sinh, Hoc_sinh.lop_hoc_id.__eq__(Lop_hoc.id), isouter=True)\
    .group_by(Lop_hoc.id).all()


def get_lop_hoc(id):
  return db.session\
    .query(Lop_hoc.id, Lop_hoc.name, Lop_hoc.khoi_lop, Lop_hoc.nam_hoc, Lop_hoc.sl_toi_da, Lop_hoc.tuoi_toi_thieu, Lop_hoc.tuoi_toi_da, func.count(Hoc_sinh.lop_hoc_id).label('si_so'))\
    .join(Hoc_sinh, Hoc_sinh.lop_hoc_id.__eq__(Lop_hoc.id), isouter=True)\
    .filter(Lop_hoc.id == id)\
    .group_by(Lop_hoc.id).first()


def add_lop_hoc(name,
                khoi_lop,
                nam_hoc,
                sl_toi_da=40,
                tuoi_toi_thieu=15,
                tuoi_toi_da=20,
                apply_all=False):
  lop = Lop_hoc(name=name,
                khoi_lop=khoi_lop,
                nam_hoc=nam_hoc,
                sl_toi_da=sl_toi_da,
                tuoi_toi_thieu=tuoi_toi_thieu,
                tuoi_toi_da=tuoi_toi_da)
  db.session.add(lop)
  if apply_all:
    db.session.query(Lop_hoc).update({
      Lop_hoc.sl_toi_da: sl_toi_da,
      Lop_hoc.tuoi_toi_thieu: tuoi_toi_thieu,
      Lop_hoc.tuoi_toi_da: tuoi_toi_da
    })
  db.session.commit()
  return None


def update_lop_hoc(id,
                   name,
                   khoi_lop,
                   nam_hoc,
                   sl_toi_da,
                   tuoi_toi_thieu=15,
                   tuoi_toi_da=20,
                   apply_all=False):
  lop = Lop_hoc.query.get(id)
  lop.name = name
  lop.khoi_lop = khoi_lop
  lop.nam_hoc = nam_hoc
  lop.sl_toi_da = sl_toi_da
  lop.tuoi_toi_thieu = tuoi_toi_thieu
  lop.tuoi_toi_da = tuoi_toi_da
  if apply_all:
    db.session.query(Lop_hoc).update({
      Lop_hoc.sl_toi_da: sl_toi_da,
      Lop_hoc.tuoi_toi_thieu: tuoi_toi_thieu,
      Lop_hoc.tuoi_toi_da: tuoi_toi_da
    })

  db.session.commit()
  return None


def delete_lop_hoc(id):
  ds_hoc_sinh = list_hoc_sinh(id)
  for hoc_sinh in ds_hoc_sinh:
    delete_hoc_sinh(hoc_sinh.id)

  db.session.query(Lop_hoc).filter(Lop_hoc.id == id).delete()
  db.session.commit()
  return None


# Hoc sinh
def list_hoc_sinh(lop_hoc_id):
  return Hoc_sinh.query.filter_by(lop_hoc_id=lop_hoc_id).all()


def get_hoc_sinh(id):
  return Hoc_sinh.query.get(id)


def add_hoc_sinh(name, lop_hoc_id, gioi_tinh, ngay_sinh, dia_chi, email, sdt):
  lop_hoc = get_lop_hoc(lop_hoc_id)
  hoc_sinh = Hoc_sinh(name=name,
                      lop_hoc_id=lop_hoc_id,
                      gioi_tinh=gioi_tinh,
                      ngay_sinh=ngay_sinh,
                      dia_chi=dia_chi,
                      email=email,
                      sdt=sdt)
  db.session.add(hoc_sinh)
  db.session.commit()
  general_bang_diem_for_hoc_sinh(lop_hoc.nam_hoc, hoc_sinh.id)
  return None


def update_hoc_sinh(id, name, lop_hoc_id, gioi_tinh, ngay_sinh, dia_chi, email,
                    sdt):
  hoc_sinh = Hoc_sinh.query.get(id)
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
  db.session.query(Hoc_sinh).filter(Hoc_sinh.id == id).delete()
  db.session.query(Bang_diem).filter(Bang_diem.hoc_sinh_id == id).delete()
  db.session.commit()
  return None


def tinh_diem_tb_hk1(self):
  count = 0
  total = 0
  if self.diem_15p_hk1_1:
    count += 1
    total += self.diem_15p_hk1_1
  if self.diem_15p_hk1_2:
    count += 1
    total += self.diem_15p_hk1_2
  if self.diem_15p_hk1_3:
    count += 1
    total += self.diem_15p_hk1_3
  if self.diem_15p_hk1_4:
    count += 1
    total += self.diem_15p_hk1_4
  if self.diem_15p_hk1_5:
    count += 1
    total += self.diem_15p_hk1_5
  if self.diem_45p_hk1_1:
    count += 2
    total += self.diem_45p_hk1_1
  if self.diem_45p_hk1_2:
    count += 2
    total += self.diem_45p_hk1_2
  if self.diem_45p_hk1_3:
    count += 2
    total += self.diem_45p_hk1_3
  if self.diem_thi_hk1:
    count += 3
    total += self.diem_thi_hk1
  if count == 0: return 0
  return round(total / count, 2)


def tinh_diem_tb_hk2(self):
  count = 0
  total = 0
  if self.diem_15p_hk2_1:
    count += 1
    total += self.diem_15p_hk2_1
  if self.diem_15p_hk2_2:
    count += 1
    total += self.diem_15p_hk2_2
  if self.diem_15p_hk2_3:
    count += 1
    total += self.diem_15p_hk2_3
  if self.diem_15p_hk2_4:
    count += 1
    total += self.diem_15p_hk2_4
  if self.diem_15p_hk2_5:
    count += 1
    total += self.diem_15p_hk2_5
  if self.diem_45p_hk2_1:
    count += 2
    total += self.diem_45p_hk2_1
  if self.diem_45p_hk2_2:
    count += 2
    total += self.diem_45p_hk2_2
  if self.diem_45p_hk2_3:
    count += 2
    total += self.diem_45p_hk2_3
  if self.diem_thi_hk2:
    count += 3
    total += self.diem_thi_hk2
  if count == 0: return 0
  return round(total / count, 2)


# Bang dien
def list_bang_diem_lop_hoc(mon_hoc_id):
  ds_bang_diem = []
  for diem in db.session.query(
      Bang_diem.id,
      Bang_diem.hoc_sinh_id,
      Hoc_sinh.name,
      Bang_diem.diem_15p_hk1_1,
      Bang_diem.diem_15p_hk1_2,
      Bang_diem.diem_15p_hk1_3,
      Bang_diem.diem_15p_hk1_4,
      Bang_diem.diem_15p_hk1_5,
      Bang_diem.diem_45p_hk1_1,
      Bang_diem.diem_45p_hk1_2,
      Bang_diem.diem_45p_hk1_3,
      Bang_diem.diem_thi_hk1,
      Bang_diem.diem_15p_hk2_1,
      Bang_diem.diem_15p_hk2_2,
      Bang_diem.diem_15p_hk2_3,
      Bang_diem.diem_15p_hk2_4,
      Bang_diem.diem_15p_hk2_5,
      Bang_diem.diem_45p_hk2_1,
      Bang_diem.diem_45p_hk2_2,
      Bang_diem.diem_45p_hk2_3,
      Bang_diem.diem_thi_hk2,
  ).filter(Bang_diem.mon_hoc_id == mon_hoc_id).join(
      Hoc_sinh, Hoc_sinh.id.__eq__(Bang_diem.hoc_sinh_id)).all():

    ds_bang_diem.append({
      "id": diem.id,
      "hoc_sinh_id": diem.hoc_sinh_id,
      "name": diem.name,
      "diem_15p_hk1_1": diem.diem_15p_hk1_1,
      "diem_15p_hk1_2": diem.diem_15p_hk1_2,
      "diem_15p_hk1_3": diem.diem_15p_hk1_3,
      "diem_15p_hk1_4": diem.diem_15p_hk1_4,
      "diem_15p_hk1_5": diem.diem_15p_hk1_5,
      "diem_45p_hk1_1": diem.diem_45p_hk1_1,
      "diem_45p_hk1_2": diem.diem_45p_hk1_2,
      "diem_45p_hk1_3": diem.diem_45p_hk1_3,
      "diem_thi_hk1": diem.diem_thi_hk1,
      "diem_15p_hk2_1": diem.diem_15p_hk2_1,
      "diem_15p_hk2_2": diem.diem_15p_hk2_2,
      "diem_15p_hk2_3": diem.diem_15p_hk2_3,
      "diem_15p_hk2_4": diem.diem_15p_hk2_4,
      "diem_15p_hk2_5": diem.diem_15p_hk2_5,
      "diem_45p_hk2_1": diem.diem_45p_hk2_1,
      "diem_45p_hk2_2": diem.diem_45p_hk2_2,
      "diem_45p_hk2_3": diem.diem_45p_hk2_3,
      "diem_thi_hk2": diem.diem_thi_hk2,
      "tb_hk1": tinh_diem_tb_hk1(diem),
      "tb_hk2": tinh_diem_tb_hk2(diem)
    })
  return ds_bang_diem


def parseInt(num):
  variable = int(num) if num else None
  return variable


def update_dang_diem(bang_diem):
  print(bang_diem["id"])

  db.session.query(Bang_diem).filter(Bang_diem.id == bang_diem["id"]).update({
    Bang_diem.diem_15p_hk1_1:
    parseInt(bang_diem["diem_15p_hk1_1"]),
    Bang_diem.diem_15p_hk1_2:
    parseInt(bang_diem["diem_15p_hk1_2"]),
    Bang_diem.diem_15p_hk1_3:
    parseInt(bang_diem["diem_15p_hk1_3"]),
    Bang_diem.diem_15p_hk1_4:
    parseInt(bang_diem["diem_15p_hk1_4"]),
    Bang_diem.diem_15p_hk1_5:
    parseInt(bang_diem["diem_15p_hk1_5"]),
    Bang_diem.diem_45p_hk1_1:
    parseInt(bang_diem["diem_45p_hk1_1"]),
    Bang_diem.diem_45p_hk1_2:
    parseInt(bang_diem["diem_45p_hk1_2"]),
    Bang_diem.diem_45p_hk1_3:
    parseInt(bang_diem["diem_45p_hk1_3"]),
    Bang_diem.diem_thi_hk1:
    parseInt(bang_diem["diem_thi_hk1"]),
    Bang_diem.diem_15p_hk2_1:
    parseInt(bang_diem["diem_15p_hk2_1"]),
    Bang_diem.diem_15p_hk2_2:
    parseInt(bang_diem["diem_15p_hk2_2"]),
    Bang_diem.diem_15p_hk2_3:
    parseInt(bang_diem["diem_15p_hk2_3"]),
    Bang_diem.diem_15p_hk2_4:
    parseInt(bang_diem["diem_15p_hk2_4"]),
    Bang_diem.diem_15p_hk2_5:
    parseInt(bang_diem["diem_15p_hk2_5"]),
    Bang_diem.diem_45p_hk2_1:
    parseInt(bang_diem["diem_45p_hk2_1"]),
    Bang_diem.diem_45p_hk2_2:
    parseInt(bang_diem["diem_45p_hk2_2"]),
    Bang_diem.diem_45p_hk2_3:
    parseInt(bang_diem["diem_45p_hk2_3"]),
    Bang_diem.diem_thi_hk2:
    parseInt(bang_diem["diem_thi_hk2"]),
  })
  db.session.commit()
  return None


def list_diem_trung_binh(lop_hoc_id):
  return db.session\
    .query(Hoc_sinh.id, Hoc_sinh.name, Hoc_sinh.lop_hoc_id, func.count(Hoc_sinh.lop_hoc_id).label('si_so'))\
    .join(Hoc_sinh, Hoc_sinh.lop_hoc_id.__eq__(Lop_hoc.id), isouter=True)\
    .group_by(Lop_hoc.id).all()


# from add mon hoc
def general_bang_diem_for_mon_hoc(mon_hoc_id):
  ds_hoc_sinh = Hoc_sinh.query.all()
  for hoc_sinh in ds_hoc_sinh:
    bang_diem = Bang_diem(nam_hoc=get_current_year(),
                          mon_hoc_id=mon_hoc_id,
                          hoc_sinh_id=hoc_sinh.id)
    db.session.add(bang_diem)
  db.session.commit()
  return None


# from add hoc sinh
def general_bang_diem_for_hoc_sinh(nam_hoc, hoc_sinh_id):
  ds_mon_hoc = list_mon_hoc()
  for mon in ds_mon_hoc:
    bang_diem = Bang_diem(nam_hoc=get_current_year(),
                          mon_hoc_id=mon.id,
                          hoc_sinh_id=hoc_sinh_id)
    db.session.add(bang_diem)
  db.session.commit()
  return None

  #   nam_hoc = Column(Integer)
  # mon_hoc_id = Column(Integer)
  # hoc_sinh_id = Column(Integer)
