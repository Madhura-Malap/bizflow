from utils.pdf_generator import generate_invoice_pdf
from sqlalchemy import extract

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    send_file
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.security import check_password_hash, generate_password_hash
from config import Config
from models.database import db
from models.user import User
from models.client import Client
from models.project import Project
from models.employee import Employee
from models.invoice import Invoice
from models.complaint import Complaint
from datetime import datetime

app = Flask(__name__)

app.config.from_object(Config)
app.secret_key = "madhura_secret"

db.init_app(app)

# Create database tables and default admin
with app.app_context():

    db.create_all()

    admin = User.query.filter_by(email="admin@madhura.com").first()

    if not admin:

        admin = User(
            name="Administrator",
            email="admin@madhura.com",
            password=generate_password_hash("admin123"),
            role="Admin"
        )

        db.session.add(admin)
        db.session.commit()


# ---------------------- LOGIN PAGE ----------------------

@app.route("/")
def login():
    return render_template("login.html")


# ---------------------- LOGIN AUTH ----------------------

@app.route("/login", methods=["POST"])
def login_user():

    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):

        session["user"] = user.name
        session["email"] = user.email
        session["role"] = user.role

        return redirect(url_for("dashboard"))

    flash("Invalid Email or Password")
    return redirect(url_for("login"))

@app.route("/demo-login")
def demo_login():

    session["user"] = "Demo Admin"
    session["email"] = "demo@pratyushadvertising.com"
    session["role"] = "Administrator"

    return redirect(url_for("dashboard"))


# ---------------------- DASHBOARD ----------------------

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    total_clients = Client.query.count()

    total_projects = Project.query.count()

    total_employees = Employee.query.count()

    total_revenue = db.session.query(
        db.func.sum(Invoice.total)
    ).scalar() or 0

    complaint_count = Complaint.query.count()

    # ==========================
    # Monthly Revenue Data
    # ==========================

    current_year = datetime.now().year
    current_month = datetime.now().month

    month_labels = []
    monthly_revenue = []

    for month in range(1, current_month + 1):

        month_labels.append(
            datetime(2000, month, 1).strftime("%b")
        )

        revenue = db.session.query(
            db.func.sum(Invoice.total)
        ).filter(
            extract("year", Invoice.invoice_date) == current_year,
            extract("month", Invoice.invoice_date) == month
        ).scalar() or 0

        monthly_revenue.append(float(revenue))

    # Recent Activities

    recent_activities = []

    # Recent Clients
    recent_clients = Client.query.order_by(Client.id.desc()).limit(2).all()

    for client in recent_clients:
        recent_activities.append({
            "message": f"✔ New client '{client.company_name}' added",
            "time": "Recently"
        })

    # Recent Projects
    recent_projects = Project.query.order_by(Project.id.desc()).limit(2).all()

    for project in recent_projects:
        recent_activities.append({
            "message": f"📁 Project '{project.project_name}' created",
            "time": "Recently"
        })

    # Recent Complaints
    recent_complaints = Complaint.query.order_by(Complaint.id.desc()).limit(2).all()

    for complaint in recent_complaints:
        recent_activities.append({
            "message": f"⚠ Complaint '{complaint.title}' received",
            "time": "Recently"
        })

    # Recent Invoices
    recent_invoices = Invoice.query.order_by(Invoice.id.desc()).limit(2).all()

    for invoice in recent_invoices:
        recent_activities.append({
            "message": f"💰 Invoice #{invoice.id} generated",
            "time": "Recently"
        })

    recent_activities = recent_activities[:3]

    return render_template(

        "dashboard.html",

        username=session["user"],

        total_clients=total_clients,

        total_projects=total_projects,

        total_employees=total_employees,

        total_revenue=total_revenue,

        complaint_count=complaint_count,

        recent_activities=recent_activities,

        month_labels=month_labels,

        monthly_revenue=monthly_revenue

    )

# ---------------------- LOGOUT ----------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))

# ---------------------- CLIENTS ----------------------

@app.route("/clients")
def clients():

    if "user" not in session:
        return redirect(url_for("login"))

    clients = Client.query.order_by(Client.id.desc()).all()

    return render_template(
        "clients.html",
        clients=clients,
        username=session["user"]
    )


@app.route("/clients/add", methods=["POST"])
def add_client():

    if "user" not in session:
        return redirect(url_for("login"))

    client = Client(

        company_name=request.form["company_name"],

        contact_person=request.form["contact_person"],

        phone=request.form["phone"],

        email=request.form["email"],

        address=request.form["address"],

        gst_number=request.form["gst_number"],

        notes=request.form["notes"]

    )

    db.session.add(client)

    db.session.commit()

    flash("Client Added Successfully!")

    return redirect(url_for("clients"))

@app.route("/clients/delete/<int:id>")
def delete_client(id):

    if "user" not in session:
        return redirect(url_for("login"))

    client = Client.query.get_or_404(id)

    db.session.delete(client)
    db.session.commit()

    flash("Client Deleted Successfully!")

    return redirect(url_for("clients"))

@app.route("/clients/edit/<int:id>", methods=["GET", "POST"])
def edit_client(id):

    if "user" not in session:
        return redirect(url_for("login"))

    client = Client.query.get_or_404(id)

    if request.method == "POST":

        client.company_name = request.form["company_name"]
        client.contact_person = request.form["contact_person"]
        client.phone = request.form["phone"]
        client.email = request.form["email"]
        client.address = request.form["address"]
        client.gst_number = request.form["gst_number"]
        client.notes = request.form["notes"]

        db.session.commit()

        flash("Client Updated Successfully!")

        return redirect(url_for("clients"))

    return render_template(
        "edit_client.html",
        client=client,
        username=session["user"]
    )

@app.route("/projects")
def projects():

    if "user" not in session:
        return redirect(url_for("login"))

    projects = Project.query.order_by(Project.id.desc()).all()
    clients = Client.query.all()

    return render_template(
        "projects.html",
        projects=projects,
        clients=clients,
        username=session["user"]
    )


@app.route("/projects/add", methods=["POST"])
def add_project():

    if "user" not in session:
        return redirect(url_for("login"))

    from datetime import datetime

    project = Project(
        project_name=request.form["project_name"],
        project_type=request.form["project_type"],
        client_id=request.form["client_id"],
        budget=float(request.form["budget"]),
        status=request.form["status"],
        start_date=datetime.strptime(request.form["start_date"], "%Y-%m-%d").date(),
        end_date=datetime.strptime(request.form["end_date"], "%Y-%m-%d").date(),
        description=request.form["description"]
    )

    db.session.add(project)
    db.session.commit()

    flash("Project Added Successfully!")

    return redirect(url_for("projects"))

@app.route("/projects/delete/<int:id>")
def delete_project(id):

    if "user" not in session:
        return redirect(url_for("login"))

    project = Project.query.get_or_404(id)

    db.session.delete(project)
    db.session.commit()

    flash("Project Deleted Successfully!")

    return redirect(url_for("projects"))

@app.route("/projects/edit/<int:id>", methods=["GET", "POST"])
def edit_project(id):

    if "user" not in session:
        return redirect(url_for("login"))

    project = Project.query.get_or_404(id)

    clients = Client.query.all()

    if request.method == "POST":

        from datetime import datetime

        project.project_name = request.form["project_name"]
        project.project_type = request.form["project_type"]
        project.client_id = request.form["client_id"]
        project.budget = request.form["budget"]
        project.status = request.form["status"]
        project.start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%d").date()
        project.end_date = datetime.strptime(request.form["end_date"], "%Y-%m-%d").date()
        project.description = request.form["description"]

        db.session.commit()

        flash("Project Updated Successfully!")

        return redirect(url_for("projects"))

    return render_template(
        "edit_project.html",
        project=project,
        clients=clients,
        username=session["user"]
    )

@app.route("/employees")
def employees():

    if "user" not in session:
        return redirect(url_for("login"))

    employees = Employee.query.order_by(Employee.id.desc()).all()

    return render_template(
        "employees.html",
        employees=employees,
        username=session["user"]
    )

@app.route("/employees/add", methods=["POST"])
def add_employee():

    if "user" not in session:
        return redirect(url_for("login"))

    from datetime import datetime

    employee = Employee(

        employee_name=request.form["employee_name"],
        email=request.form["email"],
        phone=request.form["phone"],
        department=request.form["department"],
        designation=request.form["designation"],
        salary=float(request.form["salary"]),
        joining_date=datetime.strptime(
            request.form["joining_date"],
            "%Y-%m-%d"
        ).date(),
        status=request.form["status"]

    )

    db.session.add(employee)
    db.session.commit()

    flash("Employee Added Successfully!")

    return redirect(url_for("employees"))

@app.route("/employees/delete/<int:id>")
def delete_employee(id):

    if "user" not in session:
        return redirect(url_for("login"))

    employee = Employee.query.get_or_404(id)

    db.session.delete(employee)
    db.session.commit()

    flash("Employee Deleted Successfully!")

    return redirect(url_for("employees"))

@app.route("/employees/edit/<int:id>", methods=["GET", "POST"])
def edit_employee(id):

    if "user" not in session:
        return redirect(url_for("login"))

    employee = Employee.query.get_or_404(id)

    if request.method == "POST":

        from datetime import datetime

        employee.employee_name = request.form["employee_name"]
        employee.email = request.form["email"]
        employee.phone = request.form["phone"]
        employee.department = request.form["department"]
        employee.designation = request.form["designation"]
        employee.salary = float(request.form["salary"])
        employee.joining_date = datetime.strptime(
            request.form["joining_date"],
            "%Y-%m-%d"
        ).date()
        employee.status = request.form["status"]

        db.session.commit()

        flash("Employee Updated Successfully!")

        return redirect(url_for("employees"))

    return render_template(
        "edit_employee.html",
        employee=employee,
        username=session["user"]
    )

@app.route("/invoices")
def invoices():

    if "user" not in session:
        return redirect("/login")

    invoices = Invoice.query.all()
    clients = Client.query.all()
    projects = Project.query.all()

    return render_template(
        "invoices.html",
        invoices=invoices,
        clients=clients,
        projects=projects,
        username=session["user"]
    )

@app.route("/invoices/add", methods=["POST"])
def add_invoice():

    if "user" not in session:
        return redirect("/login")

    # Generate Invoice Number
    last_invoice = Invoice.query.order_by(Invoice.id.desc()).first()

    if last_invoice:
        next_id = last_invoice.id + 1
    else:
        next_id = 1

    invoice_number = f"INV-{next_id:04d}"

    # Create Invoice
    invoice = Invoice(
        invoice_number=invoice_number,
        client_id=request.form["client_id"],
        project_id=request.form["project_id"],
        subtotal=float(request.form["subtotal"]),
        gst=float(request.form["gst"]),
        total=round(float(request.form["total"]), 2),
        payment_status=request.form["payment_status"],
        invoice_date=datetime.strptime(
            request.form["invoice_date"], "%Y-%m-%d"
        ).date(),
        due_date=datetime.strptime(
            request.form["due_date"], "%Y-%m-%d"
        ).date()
    )

    db.session.add(invoice)
    db.session.commit()

    flash("Invoice created successfully!")

    return redirect("/invoices")

@app.route("/invoices/edit/<int:id>", methods=["GET", "POST"])
def edit_invoice(id):

    if "user" not in session:
        return redirect("/login")

    invoice = Invoice.query.get_or_404(id)

    if request.method == "POST":

        invoice.client_id = request.form["client_id"]
        invoice.project_id = request.form["project_id"]
        invoice.subtotal = float(request.form["subtotal"])
        invoice.gst = float(request.form["gst"])
        invoice.total = round(float(request.form["total"]), 2)
        invoice.payment_status = request.form["payment_status"]

        invoice.invoice_date = datetime.strptime(
            request.form["invoice_date"],
            "%Y-%m-%d"
        ).date()

        invoice.due_date = datetime.strptime(
            request.form["due_date"],
            "%Y-%m-%d"
        ).date()

        db.session.commit()

        flash("Invoice updated successfully!")

        return redirect("/invoices")

    clients = Client.query.all()
    projects = Project.query.all()

    return render_template(
        "edit_invoice.html",
        invoice=invoice,
        clients=clients,
        projects=projects
    )

@app.route("/invoices/delete/<int:id>")
def delete_invoice(id):

    if "user" not in session:
        return redirect("/login")

    invoice = Invoice.query.get_or_404(id)

    db.session.delete(invoice)
    db.session.commit()

    flash("Invoice deleted successfully!")

    return redirect("/invoices")

@app.route("/invoice/pdf/<int:id>")
def download_invoice_pdf(id):

    if "user" not in session:
        return redirect("/login")

    invoice = Invoice.query.get_or_404(id)

    pdf_file = generate_invoice_pdf(invoice)

    return send_file(
        pdf_file,
        as_attachment=True
    )

@app.route("/complaints")
def complaints():

    if "user" not in session:
        return redirect("/login")

    search = request.args.get("search", "").strip()
    status = request.args.get("status", "")
    priority = request.args.get("priority", "")
    client = request.args.get("client", "")
    employee = request.args.get("employee", "")

    query = Complaint.query

    if search:
        query = query.filter(
            Complaint.title.ilike(f"%{search}%")
        )

    if status:
        query = query.filter(
            Complaint.status == status
        )

    if priority:
        query = query.filter(
            Complaint.priority == priority
        )

    if client:
        query = query.filter(
            Complaint.client_id == int(client)
        )

    if employee:
        query = query.filter(
            Complaint.employee_id == int(employee)
        )

    complaints = query.order_by(
        Complaint.id.desc()
    ).all()

    clients = Client.query.order_by(
        Client.company_name
    ).all()

    projects = Project.query.order_by(
        Project.project_name
    ).all()

    employees = Employee.query.order_by(
        Employee.employee_name
    ).all()

    return render_template(
        "complaints.html",
        complaints=complaints,
        clients=clients,
        projects=projects,
        employees=employees,
        search=search,
        status=status,
        priority=priority,
        selected_client=client,
        selected_employee=employee,
        username=session["user"]
    )

@app.route("/complaints/add", methods=["GET", "POST"])
def add_complaint():

    if "user" not in session:
        return redirect("/login")

    clients = Client.query.order_by(Client.company_name).all()
    projects = Project.query.order_by(Project.project_name).all()
    employees = Employee.query.order_by(Employee.employee_name).all()

    if request.method == "POST":

        complaint = Complaint(
            client_id=request.form["client_id"],
            project_id=request.form["project_id"],
            employee_id=request.form["employee_id"],
            title=request.form["title"],
            description=request.form["description"],
            priority=request.form["priority"],
            status=request.form["status"]
        )

        db.session.add(complaint)
        db.session.commit()

        flash("Complaint added successfully!")

        return redirect("/complaints")

    return render_template(
        "add_complaint.html",
        clients=clients,
        projects=projects,
        employees=employees
    )

@app.route("/complaints/edit/<int:id>", methods=["GET", "POST"])
def edit_complaint(id):

    if "user" not in session:
        return redirect("/login")

    complaint = Complaint.query.get_or_404(id)

    clients = Client.query.all()
    projects = Project.query.all()
    employees = Employee.query.all()

    if request.method == "POST":

        complaint.client_id = request.form["client_id"]
        complaint.project_id = request.form["project_id"]
        complaint.employee_id = request.form["employee_id"]
        complaint.title = request.form["title"]
        complaint.description = request.form["description"]
        complaint.priority = request.form["priority"]
        complaint.status = request.form["status"]

        db.session.commit()

        flash("Complaint updated successfully!")

        return redirect("/complaints")

    return render_template(
        "edit_complaint.html",
        complaint=complaint,
        clients=clients,
        projects=projects,
        employees=employees
    )

@app.route("/complaints/delete/<int:id>")
def delete_complaint(id):

    if "user" not in session:
        return redirect("/login")

    complaint = Complaint.query.get_or_404(id)

    db.session.delete(complaint)
    db.session.commit()

    flash("Complaint deleted successfully!")

    return redirect("/complaints")


@app.route("/settings", methods=["GET", "POST"])
def settings():

    if "user" not in session:
        return redirect("/login")

    user = User.query.filter_by(email=session["email"]).first()

    if request.method == "POST":

        current_password = request.form["current_password"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        # Check current password
        if not check_password_hash(user.password, current_password):
            flash("Current password is incorrect.")
            return redirect("/settings")

        # Check new passwords match
        if new_password != confirm_password:
            flash("New passwords do not match.")
            return redirect("/settings")

        # Update password
        user.password = generate_password_hash(new_password)
        db.session.commit()

        flash("Password updated successfully.")
        return redirect("/settings")

    return render_template(
        "settings.html",
        username=session["user"]
    )

# ---------------------- RUN APP ----------------------

if __name__ == "__main__":
    app.run(debug=True)