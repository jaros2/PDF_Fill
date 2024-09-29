from app import db

class Parent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    pesel = db.Column(db.String(11), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    address_street = db.Column(db.String(100), nullable=False)
    address_bldg_nbr = db.Column(db.String(10), nullable=False)
    address_apt_nbr = db.Column(db.String(10))
    address_postal_code = db.Column(db.String(10), nullable=False)
    address_city = db.Column(db.String(50), nullable=False)
    phone_nbr = db.Column(db.String(25))
    employer_tax_id = db.Column(db.String(50), nullable=False)
    employer_name = db.Column(db.String(100), nullable=False)
    bank_account = db.Column(db.String(26), nullable=False)

class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    pesel = db.Column(db.String(11), unique=True, nullable=False)

class Leave(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_from = db.Column(db.Date, nullable=False)
    date_to = db.Column(db.Date, nullable=False)
    l4_num = db.Column(db.String(50))
    main_parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'), nullable=False)
    spouse_id = db.Column(db.Integer, db.ForeignKey('parent.id'))
    spouse_days_taken = db.Column(db.Integer, nullable=True)
    spouse_received_benefits = db.Column(db.String(3), nullable=False)
    sign_date = db.Column(db.Date, nullable=False)
    total_days = db.Column(db.Integer, nullable=False)