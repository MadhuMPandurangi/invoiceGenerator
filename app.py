from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def hello_world():
    today = datetime.today().strftime("%B %-d, %Y")
    invoice_number = 123
    from_addr = {
        'seller_name': 'MY DOCTOR GURU',
        'addr': '#219 ANTILIA B3 BACHUPALLY HYDERABAD 500090',
        'ph': '+91-9032660596',
        'email': 'mydoctorguru@gmail.com',
        'GSTIN': '36AZNPK5171C1ZC',
        'state': 'TELANGANA'
    }
    to_addr = {
        'buyer_name': 'Sripad V Kulkarni',
        'addr': '#85/2A, Pimple Gurav, Pune',
        'ph': '+91-8884244459',
        'email': 'sripadvk97@gmail.com'
    }
    items ={
            'sno': '1',
            'description': 'DNB PEDIATRICS SOLVED Q PAPER FULL ACCESS COURSE',
            'duration': '12',
            'code': 'FA12',
            'price': 12499,
            'discount' : 4600,
            'gst':5,
        }
    duedate = "August 1, 2018"
    tax_amt = items['price'] - items['discount']
    gst_amt = round(tax_amt*((items['gst'])/100),2)
    cgst = gst_amt/2
    total = tax_amt + gst_amt
    round_tot = round(total)
    return render_template('invoice.html',
                            date = today,
                            from_addr = from_addr,
                            to_addr = to_addr,
                            items = items,
                            total = total,
                            tax_amt = tax_amt,
                            gst_amt = gst_amt,
                            cgst = round(cgst,2),
                            round_tot = round_tot,
                            invoice_number = invoice_number,
                            duedate = duedate)

if __name__ == '__main__':
    app.run(debug=True)