from flask import render_template, request, redirect
from app import app, login
from controllers import get_user_by_id, auth_user, list_mon_hoc, add_mon_hoc, update_mon_hoc, delete_mon_hoc, list_lop_hoc, add_lop_hoc, update_lop_hoc, delete_lop_hoc, list_hoc_sinh, get_hoc_sinh, add_hoc_sinh, update_hoc_sinh, delete_hoc_sinh, get_lop_hoc
from flask_login import login_user, logout_user


@app.route("/")
def index():
  return render_template('index.html')


@app.route("/login", methods=['POST'])
def my_login():
  username = request.form['username']
  password = request.form['password']
  current_user = auth_user(username, password)
  if current_user:
    login_user(current_user)
    print(current_user)
    next_page = request.args.get('next')
    return redirect(next_page if next_page else "/")
  return render_template('index.html')


@app.route("/logout")
def logout():
  logout_user()
  return redirect("/")


@app.route("/mon-hoc")
def mon_hoc():
  mon_hoc = list_mon_hoc()
  return render_template('mon-hoc.html', mon_hoc=mon_hoc)


@app.route("/mon-hoc", methods=['POST'])
def process_mon_hoc():
  if "id" in request.form:  #Cập Nhật
    update_mon_hoc(request.form['id'], request.form['name'])
  elif "delete" in request.form:  #Xoá
    delete_mon_hoc(request.form['delete'])
  else:  #Thêm mới
    add_mon_hoc(request.form['name'])

  return redirect("/mon-hoc")


@app.route("/lop-hoc")
def lop_hoc():
  lop_hoc = list_lop_hoc()
  return render_template('lop-hoc.html', lop_hoc=lop_hoc)


@app.route("/lop-hoc/<int:lop_hoc_id>")
def lop_hoc_detail(lop_hoc_id):
  lop_hoc = get_lop_hoc(lop_hoc_id)
  ds_lop_hoc = list_lop_hoc()
  ds_hoc_sinh = list_hoc_sinh(lop_hoc_id)
  so_luong = len(ds_hoc_sinh)
  return render_template('dshs.html',
                         lop_hoc=lop_hoc,
                         so_luong=so_luong,
                         ds_hoc_sinh=ds_hoc_sinh,
                         ds_lop_hoc=ds_lop_hoc)


@app.route("/lop-hoc/<int:lop_hoc_id>", methods=['POST'])
def process_lop_hoc_detail(lop_hoc_id):

  if "id" in request.form:  #Cập Nhật
    update_hoc_sinh(request.form['id'], request.form['name'],
                    request.form['lop_hoc_id'], request.form['gioi_tinh'],
                    request.form['ngay_sinh'], request.form['dia_chi'],
                    request.form['email'], request.form['sdt'])
  elif "delete" in request.form:  #Xoá
    delete_hoc_sinh(request.form['delete'])
  else:  #Thêm mới
    add_hoc_sinh(request.form['name'], request.form['lop_hoc_id'],
                 request.form['gioi_tinh'], request.form['ngay_sinh'],
                 request.form['dia_chi'], request.form['email'],
                 request.form['sdt'])

  return redirect("/lop-hoc/" + str(lop_hoc_id))


@app.route("/lop-hoc", methods=['POST'])
def process_lop_hoc():
  if "id" in request.form:  #Cập Nhật
    update_lop_hoc(request.form['id'], request.form['name'],
                   request.form['khoi_lop'], request.form['nam_hoc'],
                   request.form['sl_toi_da'])
  elif "delete" in request.form:  #Xoá
    delete_lop_hoc(request.form['delete'])
  else:  #Thêm mới
    add_lop_hoc(request.form['name'], request.form['khoi_lop'],
                request.form['nam_hoc'], request.form['sl_toi_da'])

  return redirect("/lop-hoc")


@login.user_loader
def user_loader(user_id):
  return get_user_by_id(user_id)


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)

# @app.route("/settings", methods=['POST', 'GET'])
# def settings():
#   if request.method == 'POST':
#     if "quy_dinh" in request.form:
#       print(request.form)
#       update_entities(1, 'quy_dinh', '')

#   quy_dinh = get_entities('quy-dinh')
#   return render_template('settings.html', quy_dinh=quy_dinh)

# @app.route("/lop-hoc/<int:lop_hoc_id>", methods=['POST', 'GET'])
# def dshs(lop_hoc_id):
#   lop_hoc = get_lop_hoc(lop_hoc_id)
#   danh_sach = list_hoc_sinh(lop_hoc_id)
#   so_luong = 40
#   return render_template('dshs.html',
#                          lop_hoc=lop_hoc,
#                          so_luong=so_luong,
#                          danh_sach=danh_sach)

# @app.route("/lop-hoc", methods=['POST', 'GET'])
# def lop_hoc():
#   if request.method == 'POST':
#     if "id" in request.form:  #Cập Nhật
#       update_lop_hoc(request.form['id'], request.form['name'],
#                      request.form['khoi_lop'], request.form['nam_hoc'])
#     elif "delete" in request.form:  #Xoá
#       delete_lop_hoc(request.form['delete'])
#     else:  #Thêm mới
#       add_lop_hoc(request.form['name'], request.form['khoi_lop'],
#                   request.form['nam_hoc'])

#   lop_hoc = list_lop_hoc()
#   return render_template('lop-hoc.html', lop_hoc=lop_hoc)

# @app.route("/mon-hoc", methods=['POST', 'GET'])
# def mon_hoc():
#   if request.method == 'POST':
#     if "id" in request.form:  #Cập Nhật
#       update_mon_hoc(request.form['id'], request.form['name'])
#     elif "delete" in request.form:  #Xoá
#       delete_mon_hoc(request.form['delete'])
#     else:  #Thêm mới
#       add_mon_hoc(request.form['name'])

#   mon_hoc = list_mon_hoc()
#   return render_template('mon-hoc.html', mon_hoc=mon_hoc)

# @app.route("/students", methods=['POST', 'GET'])
# def students():
#   if request.method == 'POST':
#     if "id" in request.form:
#       student = update_student(request.form['id'], request.form['name'],
#                                request.form['gender'],
#                                request.form['brithday'],
#                                request.form['address'])
#     elif "delete" in request.form:
#       student = delete_student(request.form['delete'])
#     else:
#       student = add_student(request.form['name'], request.form['gender'],
#                             request.form['brithday'], request.form['address'])
#   else:
#     student = ''
#   students = get_students()
#   return render_template('students.html', students=students, student=student)

# @app.route("/classes")
# def classes():
#   return render_template('index.html')
