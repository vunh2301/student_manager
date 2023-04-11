from flask import render_template, request, redirect, url_for
from app import app, login
from controllers import get_current_year, get_user_by_id, auth_user, list_mon_hoc, add_mon_hoc, update_mon_hoc, delete_mon_hoc, list_lop_hoc, add_lop_hoc, update_lop_hoc, delete_lop_hoc, list_hoc_sinh, add_hoc_sinh, update_hoc_sinh, delete_hoc_sinh, get_lop_hoc, json_list_lop_hoc, list_bang_diem_lop_hoc, update_dang_diem
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
    next_page = request.args.get('next')
    return redirect(next_page if next_page else "/")
  return render_template('index.html')


@app.route("/logout")
def logout():
  logout_user()
  return redirect("/")


@app.route("/mon-hoc")
def mon_hoc():
  if "search" in request.args:
    kw = request.args['search']
    mon_hoc = list_mon_hoc(kw)
  else:
    kw = ""
    mon_hoc = list_mon_hoc(None)
  if "messages" in request.args:
    messages = request.args['messages']
  else:
    messages = ""
  return render_template('mon-hoc.html',
                         mon_hoc=mon_hoc,
                         kw=kw,
                         messages=messages)


@app.route("/mon-hoc", methods=['POST'])
def process_mon_hoc():
  if "id" in request.form:  #Cập Nhật
    messages = "Updated"
    update_mon_hoc(request.form['id'], request.form['name'])
  elif "delete" in request.form:  #Xoá
    messages = "Deleted"
    delete_mon_hoc(request.form['delete'])
  else:  #Thêm mới
    messages = "Created"
    add_mon_hoc(request.form['name'])

  return redirect(url_for("mon_hoc", messages=messages))


@app.route("/lop-hoc")
def lop_hoc():
  lop_hoc = list_lop_hoc()
  return render_template('lop-hoc.html', lop_hoc=lop_hoc)


@app.route("/lop-hoc/<int:lop_hoc_id>")
def lop_hoc_detail(lop_hoc_id):
  lop_hoc = get_lop_hoc(lop_hoc_id)
  ds_lop_hoc = list_lop_hoc()
  ds_hoc_sinh = list_hoc_sinh(lop_hoc_id)
  return render_template('dshs.html',
                         lop_hoc=lop_hoc,
                         ds_hoc_sinh=ds_hoc_sinh,
                         ds_lop_hoc=ds_lop_hoc)


@app.route("/lop-hoc/<int:lop_hoc_id>/trung-binh")
def trung_binh(lop_hoc_id):
  lop_hoc = get_lop_hoc(lop_hoc_id)
  ds_mon_hoc = list_mon_hoc()
  mon_hoc = None
  if len(ds_mon_hoc) > 0:
    mon_hoc = ds_mon_hoc[0].id
  if "mon_hoc" in request.args:
    mon_hoc = int(request.args['mon_hoc'])

  ds_bang_diem = list_bang_diem_lop_hoc(mon_hoc, lop_hoc_id)
  print(ds_bang_diem)
  return render_template('trung-binh.html',
                         ds_bang_diem=ds_bang_diem,
                         lop_hoc=lop_hoc,mon_hoc=mon_hoc)


@app.route("/lop-hoc/<int:lop_hoc_id>/bang-diem")
def bang_diem(lop_hoc_id):
  ds_mon_hoc = list_mon_hoc()
  lop_hoc = get_lop_hoc(lop_hoc_id)
  mon_hoc = None
  if len(ds_mon_hoc) > 0:
    mon_hoc = ds_mon_hoc[0].id
  if "mon_hoc" in request.args:
    mon_hoc = int(request.args['mon_hoc'])

  ds_bang_diem_lop_hoc = list_bang_diem_lop_hoc(mon_hoc, lop_hoc_id)

  return render_template('bang-diem.html',
                         ds_mon_hoc=ds_mon_hoc,
                         lop_hoc=lop_hoc,
                         mon_hoc=mon_hoc,
                         ds_bang_diem_lop_hoc=ds_bang_diem_lop_hoc)


@app.route("/lop-hoc/<int:lop_hoc_id>/bang-diem", methods=['POST'])
def process_bang_diem(lop_hoc_id):
  ds_mon_hoc = list_mon_hoc()
  mon_hoc = None
  if len(ds_mon_hoc) > 0:
    mon_hoc = ds_mon_hoc[0].id
  if "mon_hoc" in request.args:
    mon_hoc = int(request.args['mon_hoc'])
  print("list_diem_hoc_sinh: ", request.form.getlist("id[]"))
  for idx, id in enumerate(request.form.getlist("id[]")):
    bang_diem = {
      "id": id,
      "hoc_sinh_id": request.form.getlist("hoc_sinh_id[]")[idx],
      "diem_15p_hk1_1": request.form.getlist("diem_15p_hk1_1[]")[idx],
      "diem_15p_hk1_2": request.form.getlist("diem_15p_hk1_2[]")[idx],
      "diem_15p_hk1_3": request.form.getlist("diem_15p_hk1_3[]")[idx],
      "diem_15p_hk1_4": request.form.getlist("diem_15p_hk1_4[]")[idx],
      "diem_15p_hk1_5": request.form.getlist("diem_15p_hk1_5[]")[idx],
      "diem_45p_hk1_1": request.form.getlist("diem_45p_hk1_1[]")[idx],
      "diem_45p_hk1_2": request.form.getlist("diem_45p_hk1_2[]")[idx],
      "diem_45p_hk1_3": request.form.getlist("diem_45p_hk1_3[]")[idx],
      "diem_thi_hk1": request.form.getlist("diem_thi_hk1[]")[idx],
      "diem_15p_hk2_1": request.form.getlist("diem_15p_hk2_1[]")[idx],
      "diem_15p_hk2_2": request.form.getlist("diem_15p_hk2_2[]")[idx],
      "diem_15p_hk2_3": request.form.getlist("diem_15p_hk2_3[]")[idx],
      "diem_15p_hk2_4": request.form.getlist("diem_15p_hk2_4[]")[idx],
      "diem_15p_hk2_5": request.form.getlist("diem_15p_hk2_5[]")[idx],
      "diem_45p_hk2_1": request.form.getlist("diem_45p_hk2_1[]")[idx],
      "diem_45p_hk2_2": request.form.getlist("diem_45p_hk2_2[]")[idx],
      "diem_45p_hk2_3": request.form.getlist("diem_45p_hk2_3[]")[idx],
      "diem_thi_hk2": request.form.getlist("diem_thi_hk2[]")[idx]
    }
    update_dang_diem(bang_diem)

  return redirect("/lop-hoc/" + str(lop_hoc_id) + "/bang-diem?mon_hoc=" +
                  str(mon_hoc))


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
  if 'apply_all' in request.form:
    apply_all = request.form['apply_all']
  else:
    apply_all = None
  if "id" in request.form:  #Cập Nhật
    update_lop_hoc(request.form['id'], request.form['name'],
                   request.form['khoi_lop'], request.form['nam_hoc'],
                   request.form['sl_toi_da'], request.form['tuoi_toi_thieu'],
                   request.form['tuoi_toi_da'], apply_all)
  elif "delete" in request.form:  #Xoá
    delete_lop_hoc(request.form['delete'])
  else:  #Thêm mới
    add_lop_hoc(request.form['name'], request.form['khoi_lop'],
                request.form['nam_hoc'], request.form['sl_toi_da'],
                request.form['tuoi_toi_thieu'], request.form['tuoi_toi_da'],
                apply_all)

  return redirect("/lop-hoc")


@login.user_loader
def user_loader(user_id):
  return get_user_by_id(user_id)


@app.context_processor
def common_attr():
  return {
    'current_year': get_current_year(),
    'json_ds_lop_hoc': json_list_lop_hoc(),
    'common_ds_mon_hoc': list_mon_hoc(),
    'common_ds_lop_hoc': list_lop_hoc()
  }


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
