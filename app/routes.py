from flask import render_template, redirect, url_for, request
from app import app, db
from app.models import Parent, Child, Leave
from app.forms import ParentForm, ChildForm, LeaveForm
from app.pdf_fill import fill_pdf

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_parent', methods=['GET', 'POST'])
def add_parent():
    form = ParentForm()
    if form.validate_on_submit():
        parent = Parent(**form.data)
        db.session.add(parent)
        db.session.commit()
        return redirect(url_for('add_child'))
    return render_template('add_parent.html', form=form)

@app.route('/add_child', methods=['GET', 'POST'])
def add_child():
    form = ChildForm()
    if form.validate_on_submit():
        child = Child(**form.data)
        db.session.add(child)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_child.html', form=form)

@app.route('/create_leave', methods=['GET', 'POST'])
def create_leave():
    form = LeaveForm()
    if request.method == 'POST' and form.validate():
        leave = Leave(**form.data)
        db.session.add(leave)
        db.session.commit()
        
        parent = Parent.query.get(form.main_parent_id.data)
        child = Child.query.get(form.child_id.data)
        spouse = Parent.query.get(form.spouse_id.data)
        
        pdf_dict = {
            'first_name': parent.first_name,
            'last_name': parent.last_name,
            'pesel': parent.pesel,
            'dob': parent.date_of_birth.strftime('%d.%m.%Y'),
            'street': parent.address_street,
            'bldg_num': parent.address_bldg_nbr,
            'apt_num': parent.address_apt_nbr,
            'postal_code': parent.address_postal_code,
            'city': parent.address_city,
            'phone_num': parent.phone_nbr,
            'employer_tax_id': parent.employer_tax_id,
            'employer_name': parent.employer_name,
            'bank_acct': parent.bank_account,
            'date_from': form.date_from.data.strftime('%d.%m.%Y'),
            'date_to': form.date_to.data.strftime('%d.%m.%Y'),
            'l4_num': form.l4_num.data,
            'child_pesel': child.pesel,
            'child_name': child.first_name,
            'child_last_name': child.last_name,
            'child_dob': child.date_of_birth.strftime('%d.%m.%Y'),
            'spouse_pesel': spouse.pesel,
            'spouse_dob': spouse.date_of_birth.strftime('%d.%m.%Y'),
            'spouse_first_name': spouse.first_name,
            'spouse_last_name': spouse.last_name,
            'spouse_received_benefit': 'Yes' if form.spouse_days_taken.data > 0 else 'No',
            'benefit_days_total': form.spouse_days_taken.data,
            'sign_date': form.sign_date.data.strftime('%d.%m.%Y')
        }

        pdf_path = fill_pdf(pdf_dict)  # Assuming this function returns the path to the filled PDF
        return redirect(pdf_path)
    return render_template('create_leave.html', form=form)