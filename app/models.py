from app import db
from datetime import datetime

class Parent(db.Model):
    __tablename__ = 'parents'

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

    # Establish relationship
    leaves_as_main = db.relationship('Leave', foreign_keys='Leave.main_parent_id', back_populates='main_parent')

    @property
    def total_days_as_main_parent(self):
        current_year = datetime.now().year
        return sum(
            Leave.total_days
            for leave in self.leaves_as_main
            if leave.date_from.year == current_year
        )

class Child(db.Model):
    __tablename__ = 'children'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    pesel = db.Column(db.String(11), unique=True, nullable=False)

class Leave(db.Model):
    __tablename__ = 'leaves'

    id = db.Column(db.Integer, primary_key=True)
    date_from = db.Column(db.Date, nullable=False)
    date_to = db.Column(db.Date, nullable=False)
    l4_num = db.Column(db.String(50))
    main_parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'), nullable=False)
    spouse_id = db.Column(db.Integer, db.ForeignKey('parents.id'))
    spouse_days_taken = db.Column(db.Integer, nullable=True)
    spouse_received_benefits = db.Column(db.String(3), nullable=True)
    sign_date = db.Column(db.Date, nullable=False)
    total_days = db.Column(db.Integer, nullable=False)

    # Establish relationship
    main_parent = db.relationship('Parent', foreign_keys=[main_parent_id], back_populates='leaves_as_main')