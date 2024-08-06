from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def hello_world():
    today = datetime.today().strftime("%B %-d, %Y")
    return render_template('invoice.html',
                            date = today)

if __name__ == '__main__':
    app.run(debug=True)