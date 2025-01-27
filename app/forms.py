from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class VehicleForm(FlaskForm):
    vehicle_name = StringField('Vehicle Name', validators=[DataRequired()])
    submit = SubmitField('Add Vehicle')

class EntryForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    entry_type = SelectField('Entry Type', choices=[('Income', 'Income'), ('Expense', 'Expense')], validators=[DataRequired()])
    amount = IntegerField('Amount', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
