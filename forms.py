from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import phonenumbers
from datetime import date


class RegistrationForm(FlaskForm):
    name = StringField('Name', 
            validators = [DataRequired(), Length(min = 2, max = 20)])
    email = StringField('Email', 
            validators = [DataRequired(), Email()])
    phone_num = StringField('Phone Number', 
        validators = [DataRequired(), Length(min = 10, max = 14)])
    birth_date = DateField('Birth Date',default = date.today )         
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
            validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    #cur = mysql.connection.cursor()
    #cur.execute('INSERT INTO user (name,email,phone_num, birth_date, password) VALUES(%s,%s,%s,%s,%s)', (user[0],user[1],user[2],user[3],user[4]))
    #mysql.connection.commit()


class LoginForm(FlaskForm):
    email = StringField('Email', 
            validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')