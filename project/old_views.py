from forms import AddTaskForm, RegisterForm, LoginForm 

from functools import wraps
from flask import Flask, flash, redirect, render_template, \
                    request, session, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

from sqlalchemy.exc import IntegrityError

# config
app = Flask(__name__)
app.config.from_object('_config')

db = SQLAlchemy(app)

from models import Task, User

# helper function, (removed because of switching to SQLAlchemy)
# def connect_db():
#     return sqlite3.connect(app.config['DATABASE_PATH'])


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to log in first.')
            return redirect(url_for('login'))
    return wrap

# helper function to display errors?
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text, error), 'error')

# helper function to populate the task area when there is an error
def open_tasks():
    return db.session.query(Task).filter_by(
        status='1').order_by(Task.due_date.asc())

# helper function to populate the task area when there is an error
def closed_tasks():
    return db.session.query(Task).filter_by(
        status='0').order_by(Task.due_date.asc())


# route handlers
@app.route('/logout/')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('role', None)
    flash('Goodbye!')
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name=request.form['name']).first()

            if user is not None and user.password == request.form['password']:
                session['logged_in'] = True

                session['user_id'] = user.id

                session['role'] = user.role

                flash('Welcome!')
                return redirect(url_for('tasks'))

            else:
                error = 'Invalid username or password.'

        # else:
        #     error = 'Both fields are required.'

    # if method is get then this is returned
    return render_template('login.html', form=form, error=error)

@app.route('/tasks/')
@login_required
def tasks():
    return render_template(
        'tasks.html',
        form=AddTaskForm(request.form),
        # helper functions above, referenced here
        open_tasks=open_tasks(),
        closed_tasks=closed_tasks()
    )

# Add new task
@app.route('/add/', methods=['GET', 'POST'])
@login_required
def new_task():
    error = None
    form = AddTaskForm(request.form)
    if request.method == 'POST':

        
        if form.validate_on_submit():
            print('\n', 'fuck flask', '\n', '\n', '\n', '\n')
            new_task = Task(
                form.name.data,
                form.due_date.data,
                form.priority.data,
                datetime.datetime.utcnow(),
                '1',
                session['user_id'])

            db.session.add(new_task)
            db.session.commit()
            flash('New entry was successfully posted. Thanks.')
            return redirect(url_for('tasks'))
    return render_template(
        'tasks.html',
        form=form,
        error=error,
        open_tasks=open_tasks(),
        closed_tasks=closed_tasks()
    )

# Mark task as complete
@app.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
    # passes the task_id from above to a new variable name
    new_id = task_id
    # looks for that task_id
    task = db.session.query(Task).filter_by(task_id=new_id)
    # checks if the current user_id is equal to the user_id of that task
    # 
    # first here is a little confusing? they seem to be saying that a task
    # can have many user_ids, presumable an admin also has control at the very
    # least
    if session['user_id'] == task.first().user_id or session['role'] == "admin":
        # if the user_id matches then update the status of the task
        task.update({"status": "0"})
        # commit changes
        db.session.commit()
        # tell user changes have been made
        flash('The task is complete. Nice.')
        # return tasks page
        return redirect(url_for('tasks'))
    else:
        # if the user_id does not match the task_id then don't allow changes
        # warn the user
        flash('You can only update tasks that belong to you.')
        # redirect to tasks page
        return redirect(url_for('tasks'))

# Delete tasks
@app.route('/delete/<int:task_id>/')
@login_required
def delete_entry(task_id):
    new_id = task_id
    task = db.session.query(Task).filter_by(task_id=new_id)

    if session['user_id'] == task.first().user_id or session['role'] == "admin":
        # you can do it like this because of the reference above
        task.delete()
        db.session.commit()
        flash('The task was deleted. Why not add a new one?')
        # gotta remember those return statements...
        return redirect(url_for('tasks'))
    else:
        flash('You can only delete tasks that belong to you.')
        return redirect(url_for('tasks'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    error = None
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            print('\n\n\n\n\n fuck flask')
            new_user = User(
                form.name.data,
                form.email.data,
                form.password.data,
            )
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Thanks for registering. Please login.')
            except IntegrityError:
                error = 'That username and/or email already exists.'
                return render_template('register.html', form=form, error=error)

    return render_template('register.html', form=form, error=error)