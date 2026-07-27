from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib.units import inch
from flask import send_file
import os


def generate_invoice_pdf(invoice):

    os.makedirs("pdfs", exist_ok=True)

    filename = f"pdfs/Invoice_{invoice.invoice_number}_{invoice.client.company_name}.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        """
        <font size="22"><b>PRATYUSH ADVERTISING</b></font><br/>
        <font size="11" color="grey">
        Advertising & Branding Solutions
        </font><br/><br/>
        <font size="18"><b>INVOICE</b></font>
        """,
        styles["Title"]
    )

    elements.append(title)

    elements.append(
        Paragraph(
            f"<b>Invoice No:</b> {invoice.invoice_number}<br/><br/>",
            styles["Normal"]
        )
    )
    
    status_color = colors.black
    status_bg = colors.white

    if invoice.payment_status == "Paid":
        status_color = colors.green

    elif invoice.payment_status == "Pending":
        status_color = colors.orange

    elif invoice.payment_status == "Overdue":
        status_color = colors.red

    data = [
        ["Invoice Number", invoice.invoice_number],
        ["Client", invoice.client.company_name],
        ["Project", invoice.project.project_name],
        ["Invoice Date", invoice.invoice_date.strftime("%d %b %Y")],
        ["Due Date", invoice.due_date.strftime("%d %b %Y")],
        ["Subtotal", f"Rs. {invoice.subtotal:,.2f}"],
        ["GST Amount", f"Rs. {invoice.gst:,.2f}"],
        ["Total Amount", f"Rs. {invoice.total:,.2f}"],
        ["Payment Status", invoice.payment_status.upper()]
    ]

    table = Table(data, colWidths=[180, 250])

    table.setStyle(TableStyle([

        # Left column styling
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F5F5F5")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#333333")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),

        # Right column
        ("BACKGROUND", (1, 0), (1, -1), colors.white),

        # Grid
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CFCFCF")),

        # Alignment
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),

        # Padding
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),

        # Total Amount row
        ("BACKGROUND", (0, 7), (-1, 7), colors.HexColor("#FFF8E1")),
        ("FONTNAME", (0, 7), (-1, 7), "Helvetica-Bold"),

        # Payment Status
        ("TEXTCOLOR", (1, 8), (1, 8), status_color),
        ("FONTNAME", (1, 8), (1, 8), "Helvetica-Bold"),
        ("FONTSIZE", (1, 8), (1, 8), 12),

    ]))

    elements.append(table)

    elements.append(
        Paragraph("<br/><br/>", styles["Normal"])
    )

    elements.append(
        Paragraph(
            """
            <font size="10" color="grey">
            <b>Thank you for choosing Pratyush Advertising.</b><br/><br/>
            This is a computer-generated invoice and does not require a signature.
            </font>
            """,
            styles["Normal"]
        )
    )

    doc.build(elements)

    return filename