from models.database import db


class Project(db.Model):

    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)

    project_name = db.Column(db.String(150), nullable=False)

    project_type = db.Column(db.String(100), nullable=False)

    client_id = db.Column(
        db.Integer,
        db.ForeignKey("clients.id"),
        nullable=False
    )

    budget = db.Column(db.Float, default=0)

    status = db.Column(db.String(50), default="Pending")

    start_date = db.Column(db.Date)

    end_date = db.Column(db.Date)

    description = db.Column(db.Text)

    created_at = db.Column(db.DateTime, server_default=db.func.now())   