from flask import render_template, redirect, url_for, request, flash
from app import app, db
from app.models import Parent, Child, Leave
from app.forms import ParentForm, ChildForm, LeaveForm
from app.fill_pdf import fill_pdf

@app.route('/')
def index():
    parent_exists = Parent.query.first() is not None
    if not parent_exists:
        # Redirect to the add_parent route if no parents exist
        flash('W bazie danych nie ma rodzica.')
        return redirect(url_for('add_parent'))

    child_exists = Child.query.first() is not None
    if not child_exists:
        # Redirect to the add_parent route if no parents exist
        flash('W bazie danych nie ma dziecka.')
        return redirect(url_for('add_child'))
    
    # Continue rendering index if parents exist
    return render_template('index.html')

@app.route('/add_parent', methods=['GET', 'POST'])
def add_parent():
    form = ParentForm()
    if form.validate_on_submit():
        parent_data = {key: value for key, value in form.data.items() if key in ['first_name', 
                                                                                 'last_name', 
                                                                                 'pesel', 
                                                                                 'date_of_birth', 
                                                                                 'address_street', 
                                                                                 'address_bldg_nbr', 
                                                                                 'address_apt_nbr', 
                                                                                 'address_postal_code', 
                                                                                 'address_city', 
                                                                                 'phone_nbr', 
                                                                                 'employer_tax_id',
                                                                                 'employer_name',
                                                                                 'bank_account']}
        parent = Parent(**parent_data)
        try:
            db.session.add(parent)
            db.session.commit()
            flash('Dodano rodzica.')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Wystąpił błąd {e}', 'danger')
    else:
        flash(form.errors)
        print(form.errors)  # Print out validation errors

    return render_template('add_parent.html', form=form)

@app.route('/add_child', methods=['GET', 'POST'])
def add_child():
    form = ChildForm()
    if form.validate_on_submit():
        child_data = {key: value for key, value in form.data.items() if key not in ['csrf_token']}
        child = Child(**child_data)
        try:
            db.session.add(child)
            db.session.commit()
            flash('Dodano dziecko.')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Wystąpił błąd {e}', 'danger')
    else:
        flash(form.errors)
        print(form.errors)  # Print out validation errors
    return render_template('add_child.html', form=form)

@app.route('/create_leave', methods=['GET', 'POST'])
def create_leave():
    form = LeaveForm()

    form.main_parent_id.choices = [(parent.id, f"{parent.first_name} {parent.last_name}") for parent in Parent.query.all()]
    form.child_id.choices = [(child.id, f"{child.first_name} {child.last_name}") for child in Child.query.all()]
    form.spouse_id.choices = [(parent.id, f"{parent.first_name} {parent.last_name}") for parent in Parent.query.all()]  # If using

    if request.method == 'POST' and form.validate():
        leave_data = {key: value for key, value in form.data.items() if key not in ['csrf_token']}
        leave = Leave(**leave_data)
        db.session.add(leave)
        db.session.commit()
        
        parent = Parent.query.get(form.main_parent_id.data)
        child = Child.query.get(form.child_id.data)
        spouse = Parent.query.get(form.spouse_id.data)
        
        pdf_dict = {
            'first_name': parent.first_name,
            'last_name': parent.last_name,
            'pesel': parent.pesel,
            'dob': parent.date_of_birth.strftime('%d%m%Y'),
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
            'spouse_dob': spouse.date_of_birth.strftime('%d%m%Y'),
            'spouse_first_name': spouse.first_name,
            'spouse_last_name': spouse.last_name,
            'spouse_received_benefit': 'Yes' if spouse.total_days_as_main_parent > 0 else 'No',
            'benefit_days_total': spouse.total_days_as_main_parent,
            'sign_date': form.sign_date.data.strftime('%d.%m.%Y')
        }

        pdf_path = fill_pdf(pdf_dict)  # Assuming this function returns the path to the filled PDF
        pdf_path = '/static/' + pdf_path
        return redirect(pdf_path)
    return render_template('create_leave.html', form=form)