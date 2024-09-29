from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired

class ParentForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    pesel = StringField('PESEL', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    address_street = StringField('Street', validators=[DataRequired()])
    address_bldg_nbr = StringField('Building Number', validators=[DataRequired()])
    address_apt_nbr = StringField('Apartment Number')
    address_postal_code = StringField('Postal Code', validators=[DataRequired()])
    address_city = StringField('City', validators=[DataRequired()])
    phone_nbr = StringField('Phone Number', validators=[DataRequired()])
    employer_tax_id = StringField('Employer Tax ID', validators=[DataRequired()])
    employer_name = StringField('Employer Name', validators=[DataRequired()])
    bank_account = StringField('Bank Account Number', validators=[DataRequired()])
    submit = SubmitField('Add Parent')

class ChildForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    pesel = StringField('PESEL', validators=[DataRequired()])
    submit = SubmitField('Add Child')

class LeaveForm(FlaskForm):
    date_from = DateField('Date From', format='%Y-%m-%d', validators=[DataRequired()])
    date_to = DateField('Date To', format='%Y-%m-%d', validators=[DataRequired()])
    l4_num = StringField('L4 Number')
    main_parent_id = SelectField('Main Parent', coerce=int, validators=[DataRequired()])
    spouse_id = SelectField('Spouse', coerce=int)
    child_id = SelectField('Child', coerce=int, validators=[DataRequired()])
    sign_date = DateField('Sign Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Create Leave')