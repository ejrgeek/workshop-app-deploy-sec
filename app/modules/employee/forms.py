from flask_wtf import FlaskForm
from wtforms import StringField, DateField, DecimalField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional

class EmployeeForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Optional(), Length(min=6)])
    
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[Optional()])
    position = StringField('Position', validators=[DataRequired()])
    department = StringField('Department')
    salary = DecimalField('Salary', places=2, validators=[DataRequired()])
    hire_date = DateField('Hire Date', format='%Y-%m-%d', validators=[Optional()])
    phone = StringField('Phone', validators=[Optional()])
    address = StringField('Address', validators=[Optional()])
    
    submit = SubmitField('Save')
