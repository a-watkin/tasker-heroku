from flask_wtf import Form
from wtforms import StringField, DateField, IntegerField, \
    SelectField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class AddTaskForm(Form):
    task_id = IntegerField()
    # this thing right here was DataRequired instead of DataRequired()
    # so having fixed that, it now doesn't show the error
    # 
    # but also doesn't actually add anything
    
    # name = StringField('Task Name', validators=[DataRequired()])

    name = StringField('Task Name', validators=[DataRequired()])

    # ok so the problem is here
    due_date = DateField(

        'Date Due (mm/dd/yyyy)',

        # you had:
        # validators=[DataRequired()], format='%m%d%Y'
        # I guess sqlalchemy is more picky? because it worked before when
        # sending actual SQL to the database

        # should be:
        validators=[DataRequired()], format='%m/%d/%Y'
        
    )

    # problem not here
    priority = SelectField(
        'Priority',
        validators=[DataRequired()],
        choices=[
            ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
            ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')
        ]
    )
    # typo here, satus instead of status
    status = IntegerField('Status')


class RegisterForm(Form):

    name = StringField(
        'Username',
        validators=[DataRequired(), Length( min=6, max=25 ) ]
    )

    email = StringField(
        'Email',
        validators=[DataRequired(), Email(), Length( min=6, max=40 ) ]
    )

    password = StringField(
        'Password',
        validators=[DataRequired(), Length( min=6, max=40 ) ] 
    )

    confirm = PasswordField(
        'Repeat Password',
        validators=[DataRequired(), EqualTo('password', message='Password must match')]
    )
    

class LoginForm(Form):
    name = StringField(
        'Username',
        validators=[DataRequired()]
        )

    password = PasswordField(
        'Password',
        validators=[DataRequired()]
        )