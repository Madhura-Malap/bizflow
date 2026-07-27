from models.database import db
from datetime import datetime


class Invoice(db.Model):

    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True)

    invoice_number = db.Column(db.String(30), unique=True, nullable=False)

    client_id = db.Column(
        db.Integer,
        db.ForeignKey("clients.id"),
        nullable=False
    )

    project_id = db.Column(
        db.Integer,
        db.ForeignKey("projects.id"),
        nullable=False
    )

    subtotal = db.Column(db.Float, nullable=False)

    gst = db.Column(db.Float, nullable=False)

    total = db.Column(db.Float, nullable=False)

    payment_status = db.Column(
        db.String(30),
        default="Pending"
    )

    invoice_date = db.Column(db.Date, nullable=False)

    due_date = db.Column(db.Date, nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    client = db.relationship("Client", backref="invoices")

    project = db.relationship("Project", backref="invoices")