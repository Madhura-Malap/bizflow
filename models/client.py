from models.database import db


class Client(db.Model):

    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)

    company_name = db.Column(db.String(150), nullable=False)

    contact_person = db.Column(db.String(100), nullable=False)

    phone = db.Column(db.String(15), nullable=False)

    email = db.Column(db.String(120), unique=True)

    address = db.Column(db.Text)

    gst_number = db.Column(db.String(50))

    notes = db.Column(db.Text)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    projects = db.relationship(
    "Project",
    backref="client",
    lazy=True,
    cascade="all, delete"
)