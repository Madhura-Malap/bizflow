from app import app
from models.database import db

from models.client import Client
from models.employee import Employee
from models.project import Project
from models.invoice import Invoice
from models.complaint import Complaint

from datetime import datetime, timedelta
import random


if __name__ == "__main__":

    with app.app_context():

        print("=" * 50)
        print("Starting Seed Data...")
        print("=" * 50)

        # =====================================================
        # CLIENTS
        # =====================================================

        clients_data = [

            {
                "company_name": "Bright Bakery",
                "contact_person": "Aarav Patil",
                "phone": "9876543201",
                "email": "brightbakery@gmail.com",
                "address": "Pune",
                "gst_number": "GST1001",
                "notes": "Bakery & Cakes"
            },

            {
                "company_name": "Sunrise Cafe",
                "contact_person": "Neha Joshi",
                "phone": "9876543202",
                "email": "sunrisecafe@gmail.com",
                "address": "Mumbai",
                "gst_number": "GST1002",
                "notes": "Cafe Promotions"
            },

            {
                "company_name": "Green Leaf Restaurant",
                "contact_person": "Rohan Deshmukh",
                "phone": "9876543203",
                "email": "greenleaf@gmail.com",
                "address": "Nashik",
                "gst_number": "GST1003",
                "notes": "Restaurant Branding"
            },

            {
                "company_name": "Royal Furniture",
                "contact_person": "Sneha Kulkarni",
                "phone": "9876543204",
                "email": "royalfurniture@gmail.com",
                "address": "Pune",
                "gst_number": "GST1004",
                "notes": "Furniture Advertising"
            },

            {
                "company_name": "Elite Fashion",
                "contact_person": "Priya Shah",
                "phone": "9876543205",
                "email": "elitefashion@gmail.com",
                "address": "Mumbai",
                "gst_number": "GST1005",
                "notes": "Fashion Campaign"
            },

            {
                "company_name": "City Electronics",
                "contact_person": "Rahul Jain",
                "phone": "9876543206",
                "email": "cityelectronics@gmail.com",
                "address": "Nagpur",
                "gst_number": "GST1006",
                "notes": "Electronics Marketing"
            },

            {
                "company_name": "Happy Kids School",
                "contact_person": "Meera Patil",
                "phone": "9876543207",
                "email": "happykids@gmail.com",
                "address": "Kolhapur",
                "gst_number": "GST1007",
                "notes": "School Promotions"
            },

            {
                "company_name": "Fresh Mart",
                "contact_person": "Aniket More",
                "phone": "9876543208",
                "email": "freshmart@gmail.com",
                "address": "Satara",
                "gst_number": "GST1008",
                "notes": "Retail Marketing"
            },

            {
                "company_name": "Urban Salon",
                "contact_person": "Kajal Singh",
                "phone": "9876543209",
                "email": "urbansalon@gmail.com",
                "address": "Pune",
                "gst_number": "GST1009",
                "notes": "Beauty Campaign"
            },

            {
                "company_name": "Dream Homes",
                "contact_person": "Vivek Sharma",
                "phone": "9876543210",
                "email": "dreamhomes@gmail.com",
                "address": "Thane",
                "gst_number": "GST1010",
                "notes": "Real Estate Ads"
            },

            {
                "company_name": "Pixel Prints",
                "contact_person": "Aditya Naik",
                "phone": "9876543211",
                "email": "pixelprints@gmail.com",
                "address": "Goa",
                "gst_number": "GST1011",
                "notes": "Printing Services"
            },

            {
                "company_name": "Spark Technologies",
                "contact_person": "Tanvi Kulkarni",
                "phone": "9876543212",
                "email": "sparktech@gmail.com",
                "address": "Pune",
                "gst_number": "GST1012",
                "notes": "IT Company"
            },

            {
                "company_name": "BlueWave Solutions",
                "contact_person": "Karan Mehta",
                "phone": "9876543213",
                "email": "bluewave@gmail.com",
                "address": "Mumbai",
                "gst_number": "GST1013",
                "notes": "Software Services"
            },

            {
                "company_name": "Creative Media",
                "contact_person": "Pooja Patil",
                "phone": "9876543214",
                "email": "creativemedia@gmail.com",
                "address": "Pune",
                "gst_number": "GST1014",
                "notes": "Media Agency"
            },

            {
                "company_name": "Prime Builders",
                "contact_person": "Amit Chavan",
                "phone": "9876543215",
                "email": "primebuilders@gmail.com",
                "address": "Nashik",
                "gst_number": "GST1015",
                "notes": "Construction"
            },

            {
                "company_name": "Vision Healthcare",
                "contact_person": "Dr. Neha Joshi",
                "phone": "9876543216",
                "email": "visionhealth@gmail.com",
                "address": "Pune",
                "gst_number": "GST1016",
                "notes": "Healthcare Marketing"
            },

            {
                "company_name": "Nova Foods",
                "contact_person": "Sagar Pawar",
                "phone": "9876543217",
                "email": "novafoods@gmail.com",
                "address": "Aurangabad",
                "gst_number": "GST1017",
                "notes": "Food Products"
            },

            {
                "company_name": "Skyline Travels",
                "contact_person": "Komal Patil",
                "phone": "9876543218",
                "email": "skyline@gmail.com",
                "address": "Mumbai",
                "gst_number": "GST1018",
                "notes": "Travel Agency"
            },

            {
                "company_name": "Zenith Fitness",
                "contact_person": "Ritesh More",
                "phone": "9876543219",
                "email": "zenithfitness@gmail.com",
                "address": "Pune",
                "gst_number": "GST1019",
                "notes": "Gym Promotions"
            },

            {
                "company_name": "Blossom Boutique",
                "contact_person": "Anjali Kulkarni",
                "phone": "9876543220",
                "email": "blossomboutique@gmail.com",
                "address": "Kolhapur",
                "gst_number": "GST1020",
                "notes": "Boutique Branding"
            }

        ]

        print("Adding Clients...")

        if Client.query.count() == 0:

            for data in clients_data:

                client = Client(
                    company_name=data["company_name"],
                    contact_person=data["contact_person"],
                    phone=data["phone"],
                    email=data["email"],
                    address=data["address"],
                    gst_number=data["gst_number"],
                    notes=data["notes"]
                )

                db.session.add(client)

            db.session.commit()
            print("Clients Added Successfully")

        else:
            print("Clients Already Exist")

        # =====================================================
        # EMPLOYEES
        # =====================================================

        employees_data = [
                        {
                "name": "Aarav Sharma",
                "designation": "Graphic Designer",
                "department": "Creative",
                "email": "aarav@gmail.com",
                "phone": "9123456701",
                "salary": 40000
            },

            {
                "name": "Priya Patil",
                "designation": "Content Writer",
                "department": "Content",
                "email": "priya@gmail.com",
                "phone": "9123456702",
                "salary": 38000
            },

            {
                "name": "Rahul Deshmukh",
                "designation": "Social Media Manager",
                "department": "Marketing",
                "email": "rahul@gmail.com",
                "phone": "9123456703",
                "salary": 45000
            },

            {
                "name": "Sneha Kulkarni",
                "designation": "SEO Executive",
                "department": "Marketing",
                "email": "sneha@gmail.com",
                "phone": "9123456704",
                "salary": 42000
            },

            {
                "name": "Rohan Joshi",
                "designation": "UI/UX Designer",
                "department": "Creative",
                "email": "rohan@gmail.com",
                "phone": "9123456705",
                "salary": 47000
            },

            {
                "name": "Meera Shah",
                "designation": "Video Editor",
                "department": "Creative",
                "email": "meera@gmail.com",
                "phone": "9123456706",
                "salary": 43000
            },

            {
                "name": "Karan Mehta",
                "designation": "Marketing Executive",
                "department": "Marketing",
                "email": "karan@gmail.com",
                "phone": "9123456707",
                "salary": 39000
            },

            {
                "name": "Anjali More",
                "designation": "HR Executive",
                "department": "Human Resources",
                "email": "anjali@gmail.com",
                "phone": "9123456708",
                "salary": 36000
            },

            {
                "name": "Sagar Pawar",
                "designation": "Sales Executive",
                "department": "Sales",
                "email": "sagar@gmail.com",
                "phone": "9123456709",
                "salary": 41000
            },

            {
                "name": "Neha Chavan",
                "designation": "Account Manager",
                "department": "Accounts",
                "email": "neha@gmail.com",
                "phone": "9123456710",
                "salary": 50000
            }

        ]

        print("Adding Employees...")

        if Employee.query.count() == 0:

            for data in employees_data:

                employee = Employee(

                    employee_name=data["name"],

                    designation=data["designation"],

                    department=data["department"],

                    email=data["email"],

                    phone=data["phone"],

                    salary=data["salary"],

                    joining_date=datetime.now().date(),

                    status="Active"

                )

                db.session.add(employee)

            db.session.commit()

            print("Employees Added Successfully")

        else:

            print("Employees Already Exist")

        # =====================================================
        # PROJECTS
        # =====================================================

        project_names = [

            ("Summer Sale Campaign", "Social Media Marketing"),
            ("Website Redesign", "Web Development"),
            ("Brand Awareness Drive", "Digital Marketing"),
            ("Festival Poster Design", "Graphic Design"),
            ("Product Launch Campaign", "Advertising"),
            ("SEO Optimization", "SEO"),
            ("Instagram Promotion", "Social Media Marketing"),
            ("Corporate Branding", "Branding"),
            ("Logo Design", "Graphic Design"),
            ("Facebook Ads Campaign", "Advertising"),
            ("YouTube Video Promotion", "Video Marketing"),
            ("Email Marketing Campaign", "Email Marketing"),
            ("Influencer Collaboration", "Influencer Marketing"),
            ("Brochure Design", "Print Media"),
            ("Google Ads Campaign", "PPC Marketing"),
            ("Packaging Design", "Graphic Design"),
            ("Business Card Design", "Print Media"),
            ("Restaurant Promotion", "Digital Marketing"),
            ("Mobile App Promotion", "Advertising"),
            ("Product Photography", "Photography"),
            ("Content Marketing", "Content Creation"),
            ("Rebranding Campaign", "Branding"),
            ("LinkedIn Marketing", "Social Media Marketing"),
            ("Outdoor Hoarding Design", "Outdoor Advertising"),
            ("Annual Marketing Campaign", "Marketing")

        ]

        print("Adding Projects...")

        if Project.query.count() == 0:

            clients = Client.query.all()

            statuses = [
                "Pending",
                "Ongoing",
                "Completed"
            ]

            for name, ptype in project_names:

                start_date = datetime.now().date() - timedelta(
                    days=random.randint(20, 180)
                )

                end_date = start_date + timedelta(
                    days=random.randint(15, 90)
                )

                project = Project(

                    project_name=name,
                    project_type=ptype,

                    client_id=random.choice(clients).id,

                    budget=random.randint(
                        25000,
                        300000
                    ),

                    status=random.choice(statuses),

                    start_date=start_date,

                    end_date=end_date,

                    description=f"{name} project for advertising and promotional activities."

                )

                db.session.add(project)

            db.session.commit()

            print("Projects Added Successfully")

        else:

            print("Projects Already Exist")

        # =====================================================
        # INVOICES
        # =====================================================

        print("Adding Invoices...")

        if Invoice.query.count() == 0:

            projects = Project.query.all()

            payment_statuses = [

                "Paid",
                "Pending",
                "Overdue"

            ]

            for i, project in enumerate(projects, start=1):

                invoice_date = datetime.now().date() - timedelta(

                    days=random.randint(10, 180)

                )

                due_date = invoice_date + timedelta(days=30)

                subtotal = project.budget

                gst = round(subtotal * 0.18, 2)

                total = subtotal + gst

                if project.status == "Completed":
                    payment_status = "Paid"
                
                elif project.status == "In Progress":
                    payment_status = "Pending"
                
                else:
                    payment_status = "Overdue"

                invoice = Invoice(

                    invoice_number=f"INV-{1000+i}",

                    client_id=project.client_id,

                    project_id=project.id,

                    subtotal=subtotal,

                    gst=gst,

                    total=total,

                    payment_status=payment_status,

                    invoice_date=invoice_date,

                    due_date=due_date

                )

                db.session.add(invoice)

            db.session.commit()

            print("Invoices Added Successfully")

        else:

            print("Invoices Already Exist")

        # =====================================================
        # COMPLAINTS
        # =====================================================

        print("Adding Complaints...")

        if Complaint.query.count() == 0:

            projects = Project.query.all()

            employees = Employee.query.all()

            complaint_titles = [
                                (
                    "Campaign Delay",
                    "Advertising campaign was delivered later than the agreed timeline."
                ),

                (
                    "Design Revision",
                    "The client requested multiple revisions to the final creative design."
                ),

                (
                    "Budget Concern",
                    "Campaign expenses exceeded the approved marketing budget."
                ),

                (
                    "Low Engagement",
                    "The social media campaign received lower engagement than expected."
                )

            ]

            priorities = [
                "Low",
                "Medium",
                "High"
            ]

            complaint_statuses = [
                "In Progress",
                "Resolved"
            ]

            for title, description in complaint_titles:

                project = random.choice(projects)

                employee = random.choice(employees)

                status = random.choice(complaint_statuses)

                complaint = Complaint(

                    client_id=project.client_id,

                    project_id=project.id,

                    employee_id=employee.id,

                    title=title,

                    description=description,

                    priority=random.choice(priorities),

                    status=status,

                    resolved_at=(
                        datetime.now()
                        if status == "Resolved"
                        else None
                    )

                )

                db.session.add(complaint)

            db.session.commit()

            print("Complaints Added Successfully")

        else:

            print("Complaints Already Exist")

        print("=" * 50)
        print("Seed Data Completed Successfully!")
        print("=" * 50)

        print(f"Clients     : {Client.query.count()}")
        print(f"Employees   : {Employee.query.count()}")
        print(f"Projects    : {Project.query.count()}")
        print(f"Invoices    : {Invoice.query.count()}")
        print(f"Complaints  : {Complaint.query.count()}")

        print("=" * 50)