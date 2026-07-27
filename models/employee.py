from models.database import db
from datetime import datetime


class Employee(db.Model):

    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)

    employee_name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)

    phone = db.Column(db.String(20), nullable=False)

    department = db.Column(db.String(50), nullable=False)

    designation = db.Column(db.String(50), nullable=False)

    salary = db.Column(db.Float, nullable=False)

    joining_date = db.Column(db.Date, nullable=False)

    status = db.Column(db.String(20), default="Active")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)