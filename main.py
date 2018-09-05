import os
import base64
from flask import Flask, render_template, request, redirect, url_for, session
from peewee import fn
from model import Bill, User

app = Flask(__name__)
# app.secret_key = b'\xf1A\x88f\x1a@6\x1d\xa2\xc8J\xfc\x9e\x9c1\x86p\x04\xc1\xc7\xc7\x03\xfd\xbd'
# app.secret_key = os.environ.get('SECRET_KEY').encode()


@app.route('/')
def home():
    return redirect(url_for('all'))


@app.route('/bills/')
def all():
    bills = Bill.select()
    return render_template('bills.jinja2', bills=bills)


@app.route('/users/')
def users():
    all_users = User.select()
    return render_template('users.jinja2', all_users=all_users)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        bill_name = request.form['name']
        bill_amt = int(request.form['amount'])
        new_bill = Bill(name=bill_name, amount=bill_amt)
        new_bill.save()
        return redirect(url_for('all'))

    return render_template('create.jinja2')


@app.route('/report')
def report():
    bills = Bill.select(Bill.amount)
    total = 0
    for bill in bills:
        total += bill.amount
    bills_total = total
    return render_template('report.jinja2', bills_total=bills_total)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port, debug=True)
