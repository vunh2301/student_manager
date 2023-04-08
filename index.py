from flask import render_template, request
from app import app
from controllers import get_students, add_student, delete_student, update_student


@app.route("/")
def index():
  # student = add_student()
  # delete = delete_student(6)
  # update = update_student(5)
  students = get_students()
  return render_template('index.html', students=students)


@app.route("/students", methods=['POST', 'DELETE', 'GET'])
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
  return render_template('index.html', students=students, student=student)


@app.route("/classes")
def classes():
  return render_template('index.html', path='/classes')


@app.route("/courses")
def courses():
  return render_template('index.html', path='/courses')


@app.route("/settings")
def settings():
  return render_template('index.html', path='/settings')


@app.route("/login")
def login():
  return render_template('index.html', path='/login')


@app.context_processor
def commont_attr():
  # if not current_user.is_authenticated:
  #   return redirect('/login')

  return {'categories': '/index'}


app.run(host='0.0.0.0', debug=True)
