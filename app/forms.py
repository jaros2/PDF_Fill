from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired
import datetime
 

class ParentForm(FlaskForm):
    first_name = StringField('Imię', validators=[DataRequired()])
    last_name = StringField('Nazwisko', validators=[DataRequired()])
    pesel = StringField('PESEL', validators=[DataRequired()])
    date_of_birth = DateField('Data urodzin', format='%Y-%m-%d', validators=[DataRequired()])
    address_street = StringField('Ulica', validators=[DataRequired()])
    address_bldg_nbr = StringField('Nr bud', validators=[DataRequired()])
    address_apt_nbr = StringField('Nr mieszk')
    address_postal_code = StringField('Kod pocztowy', validators=[DataRequired()])
    address_city = StringField('Miasto', validators=[DataRequired()])
    phone_nbr = StringField('Nr tel', validators=[DataRequired()])
    employer_tax_id = StringField('NIP zakładu pracy', validators=[DataRequired()])
    employer_name = StringField('Zakład pracy', validators=[DataRequired()])
    bank_account = StringField('Nr Konta', validators=[DataRequired()])
    

class ChildForm(FlaskForm):
    first_name = StringField('Imię', validators=[DataRequired()])
    last_name = StringField('Nazwisko', validators=[DataRequired()])
    date_of_birth = DateField('Data urodzin', format='%Y-%m-%d', validators=[DataRequired()])
    pesel = StringField('PESEL', validators=[DataRequired()])
    

class LeaveForm(FlaskForm):
    date_from = DateField('Od', format='%Y-%m-%d', validators=[DataRequired()])
    date_to = DateField('Do', format='%Y-%m-%d', validators=[DataRequired()])
    total_days = IntegerField('Suma dni roboczych', validators=[DataRequired()])
    l4_num = StringField('L4')
    main_parent_id = SelectField('Rodzic główny', coerce=int, validators=[DataRequired()])
    spouse_id = SelectField('Rodzic drugi', coerce=int)
    child_id = SelectField('Dziecko', coerce=int, validators=[DataRequired()])
    sign_date = DateField('Data podpisania', default=datetime.date.today, format='%Y-%m-%d', validators=[DataRequired()])
    