from flask import Flask, render_template, send_file, url_for
import csv, os
from flask_apscheduler import APScheduler
from num2words import num2words
from weasyprint import HTML, CSS
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)

def send_email(to_email, subject, body, attachment_path):
    from_email = "madhumpandurangi@gmail.com"
    from_password = "MaDhU8150937838"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the body of the email to the MIME message
    msg.attach(MIMEText(body, 'plain'))

    # Attach the PDF file
    with open(attachment_path, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(attachment_path)}")
        msg.attach(part)

    # Connect to the server and send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, from_password)
        server.send_message(msg)
        server.quit()
        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def generate_invoice():
    with app.app_context():
        with open('static/CSV/payment_info.csv', newline='') as payment_file:
            payment_reader = csv.DictReader(payment_file)
            for payment_row in payment_reader:
                invoice_date = payment_row['invoice_date']
                invoice_number = payment_row['invoice_no']
                gst = 5
                from_addr = {
                    'seller_name': 'MY DOCTOR GURU',
                    'addr': '#219 ANTILIA B3 BACHUPALLY HYDERABAD 500090',
                    'ph': '+91-9032660596',
                    'email': 'mydoctorguru@gmail.com',
                    'GSTIN': '36AZNPK5171C1ZC',
                    'state': 'TELANGANA'
                }
                to_addr = {
                    'buyer_name': payment_row['name'],
                    'addr': payment_row['addr'],
                    'ph': payment_row['ph'],
                    'email': payment_row['email']
                }

                with open('static/CSV/prod_info.csv', newline='') as prod_file:
                    prod_reader = csv.DictReader(prod_file)
                    for prod_row in prod_reader:
                        if prod_row['final_amt'] == payment_row['amount']:
                            desc = prod_row['desc']
                            duration = payment_row['duration']
                            price = float(prod_row['price'])
                            discount = float(prod_row['dis'])
                            code = prod_row['code']

                tax_amt = price - discount
                gst_amt = round(tax_amt * (gst / 100), 2)
                cgst = gst_amt / 2
                total = tax_amt + gst_amt
                round_tot = round(total)

                # Generate the HTML content
                html_content =  render_template('invoice.html',
                                               date=invoice_date,
                                               from_addr=from_addr,
                                               to_addr=to_addr,
                                               total=total,
                                               price=price,
                                               discount=discount,
                                               code = code,
                                               tax_amt=tax_amt,
                                               gst_amt=gst_amt,
                                               desc=desc,
                                               duration=duration,
                                               cgst=round(cgst, 2),
                                               round_tot=round_tot,
                                               invoice_number=invoice_number,
                                               price_in_words=num2words(round_tot).capitalize())

                # Convert HTML to PDF with base_url for static files
                pdf = HTML(string=html_content, base_url=os.path.abspath('.')).write_pdf()

                # Save PDF to a file
                pdf_filename = f"static/invoices/{payment_row['name']}_{invoice_number}_invoice.pdf"
                with open(pdf_filename, 'wb') as pdf_file:
                    pdf_file.write(pdf)

                # # Send the PDF via email
                # subject = f"Your Invoice {invoice_number} from MY DOCTOR GURU"
                # body = f"Dear {to_addr['buyer_name']},\n\nPlease find attached your invoice {invoice_number}.\n\nThank you!\n\nBest regards,\nMY DOCTOR GURU"
                # send_email(to_addr['email'], subject, body, pdf_filename)

            
@app.route('/')
def home():
    generate_invoice()  # Run the invoice generation once when this route is accessed
    return "Invoices generated in the path 'static/invoices', if u want to regenerate the invoices then refresh this page."

if __name__ == '__main__':
    app.run(debug=True)