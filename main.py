import datetime

from data.categories import CategoryJob
from data.departments import Department
from data.jobs import Jobs
from data.users import User
from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms import RegisterForm, LoginForm, JobForm, DepForm

from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return render_template("jobs.html", title="Mars Colonization", jobs=jobs)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Sign in', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('registration.html', title='Sign up', form=form)


@app.route("/new_job", methods=['GET', 'POST'])
@login_required
def new_job():
    form = JobForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        job = Jobs()
        job.job = form.title.data
        job.team_leader = form.leader_id.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        job.creator = current_user.id

        category_id = form.category.data
        category = session.query(CategoryJob).filter(CategoryJob.id == category_id).first()
        job.categories.append(category)
        session.commit()

        try:
            current_user.jobs.append(job)
        except:
            pass
        session.merge(current_user)
        session.commit()
        return redirect('/')
    return render_template('new_job.html', title='New job', form=form)


@app.route('/new_job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = JobForm()
    if request.method == "GET":
        session = db_session.create_session()
        if current_user.id == 1:
            job = session.query(Jobs).filter(Jobs.id == id).first()
        else:
            job = session.query(Jobs).filter(Jobs.id == id,
                                             Jobs.creator == current_user.id).first()
        if job:
            form.title.data = job.job
            form.leader_id.data = job.team_leader
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.is_finished.data = job.is_finished
            form.category.data = job.categories[0].id
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        if current_user.id == 1:
            job = session.query(Jobs).filter(Jobs.id == id).first()
        else:
            job = session.query(Jobs).filter(Jobs.id == id,
                                             Jobs.creator == current_user.id).first()
        if job:
            job.job = form.title.data
            job.team_leader = form.leader_id.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.is_finished = form.is_finished.data

            category_id = form.category.data
            category = session.query(CategoryJob).filter(CategoryJob.id == category_id).first()
            job.categories[0] = category

            try:
                current_user.jobs.append(job)
            except:
                pass

            session.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('new_job.html', title='Job edit', form=form)


@app.route('/delete_job/<int:id>', methods=['GET', 'POST'])
@login_required
def job_delete(id):
    session = db_session.create_session()
    if current_user.id == 1:
        job = session.query(Jobs).filter(Jobs.id == id).first()
    else:
        job = session.query(Jobs).filter(Jobs.id == id,
                                         Jobs.creator == current_user.id).first()
    if job:
        session.delete(job)
        session.commit()
    else:
        abort(404)
    return redirect('/')


@app.route("/departments")
def departments():
    session = db_session.create_session()
    deps = session.query(Department).all()
    return render_template("departments.html", title="List of Departments", deps=deps)


@app.route('/new_dep', methods=['GET', 'POST'])
@login_required
def new_dep():
    form = DepForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        dep = Department()
        dep.title = form.title.data
        dep.chief = form.chief_id.data
        dep.members = form.members.data
        dep.email = form.email.data
        dep.creator = current_user.id
        chief = session.query(User).filter(User.id == form.chief_id.data).first()
        chief.deps.append(dep)
        session.merge(current_user)
        session.commit()
        return redirect('/departments')
    return render_template('new_dep.html', title='New Department',
                           form=form)


@app.route('/new_dep/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_dep(id):
    form = DepForm()
    if request.method == "GET":
        session = db_session.create_session()
        if current_user.id == 1:
            dep = session.query(Department).filter(Department.id == id).first()
        else:
            dep = session.query(Department).filter(Department.id == id,
                                                   Department.creator == current_user.id).first()
        if dep:
            form.title.data = dep.title
            form.chief_id.data = dep.chief
            form.members.data = dep.members
            form.email.data = dep.email
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        if current_user.id == 1:
            dep = session.query(Department).filter(Department.id == id).first()
        else:
            dep = session.query(Department).filter(Department.id == id,
                                                   Department.creator == current_user.id).first()
        if dep:
            dep.title = form.title.data
            dep.chief = form.chief_id.data
            dep.members = form.members.data
            dep.email = form.email.data
            session.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('new_dep.html', title='Department edit', form=form)


@app.route('/delete_dep/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_dep(id):
    session = db_session.create_session()
    if current_user.id == 1:
        dep = session.query(Department).filter(Department.id == id).first()
    else:
        dep = session.query(Department).filter(Department.id == id,
                                               Department.creator == current_user.id).first()
    if dep:
        session.delete(dep)
        session.commit()
    else:
        abort(404)
    return redirect('/departments')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


if __name__ == '__main__':
    db_session.global_init("db/mars_one.sqlite")
    app.run(port=8080, host='127.0.0.1')
    app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
