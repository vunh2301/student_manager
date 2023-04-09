from flask import render_template, request, redirect
from app import app
from controllers import get_students, add_student, delete_student, update_student, get_entities, update_entities, list_mon_hoc, add_mon_hoc, update_mon_hoc, delete_mon_hoc, list_lop_hoc, get_lop_hoc, add_lop_hoc, update_lop_hoc, delete_lop_hoc, list_hoc_sinh
import json


@app.route("/")
def index():
  students = get_students()
  return render_template('index.html', students=students)


@app.route("/lop-hoc/<int:lop_hoc_id>", methods=['POST', 'GET'])
def dshs(lop_hoc_id):
  lop_hoc = get_lop_hoc(lop_hoc_id)
  danh_sach = list_hoc_sinh(lop_hoc_id)
  so_luong = 40
  return render_template('dshs.html', lop_hoc=lop_hoc, so_luong=so_luong, danh_sach=danh_sach)


@app.route("/lop-hoc", methods=['POST', 'GET'])
def lop_hoc():
  if request.method == 'POST':
    if "id" in request.form:  #Cập Nhật
      update_lop_hoc(request.form['id'], request.form['name'],
                     request.form['khoi_lop'], request.form['nam_hoc'])
    elif "delete" in request.form:  #Xoá
      delete_lop_hoc(request.form['delete'])
    else:  #Thêm mới
      add_lop_hoc(request.form['name'], request.form['khoi_lop'],
                  request.form['nam_hoc'])

    redirect('/lop-hoc')

  lop_hoc = list_lop_hoc()
  return render_template('lop-hoc.html', lop_hoc=lop_hoc)


@app.route("/mon-hoc", methods=['POST', 'GET'])
def mon_hoc():
  if request.method == 'POST':
    if "id" in request.form:  #Cập Nhật
      update_mon_hoc(request.form['id'], request.form['name'])
    elif "delete" in request.form:  #Xoá
      delete_mon_hoc(request.form['delete'])
    else:  #Thêm mới
      add_mon_hoc(request.form['name'])
  
    redirect('/mon-hoc')

  mon_hoc = list_mon_hoc()
  return render_template('mon-hoc.html', mon_hoc=mon_hoc)


@app.route("/students", methods=['POST', 'GET'])
def students():
  if request.method == 'POST':
    if "id" in request.form:
      student = update_student(request.form['id'], request.form['name'],
                               request.form['gender'],
                               request.form['brithday'],
                               request.form['address'])
    elif "delete" in request.form:
      student = delete_student(request.form['delete'])
    else:
      student = add_student(request.form['name'], request.form['gender'],
                            request.form['brithday'], request.form['address'])
  else:
    student = ''
  students = get_students()
  return render_template('students.html', students=students, student=student)


@app.route("/classes")
def classes():
  return render_template('index.html')


@app.route("/courses")
def courses():
  lop = json.dumps([{
    "id": 1,
    "lop": 10
  }, {
    "id": 2,
    "lop": 11
  }, {
    "id": 3,
    "lop": 12
  }])
  bang_diem = json.dumps([{
    "nam": 2022,
    "mon": "Python",
    "hk1_15p": None,
    "hk1_1h": None,
    "hk1": None,
    "hk2_15p": None,
    "hk2_1h": None,
    "hk2": None,
    "join_student_id": 1
  }])
  print(bang_diem)
  return render_template('index.html', lop=lop)


@app.route("/settings", methods=['POST', 'GET'])
def settings():
  if request.method == 'POST':
    if "quy_dinh" in request.form:
      print(request.form)
      update_entities(1, 'quy_dinh', '')

  quy_dinh = get_entities('quy-dinh')
  return render_template('settings.html', quy_dinh=quy_dinh)


@app.route("/login")
def login():
  return render_template('index.html')


@app.context_processor
def commont_attr():
  # if not current_user.is_authenticated:
  #   return redirect('/login')

  return {'categories': '/index'}


app.run(host='0.0.0.0', debug=True)
