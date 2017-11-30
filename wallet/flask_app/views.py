from flask_app import app
from flask import flash, render_template, request, redirect
import os
import sys
sys.path.append(os.path.dirname(os.getcwd()))
from wallet import Wallet, Transaction
from .forms import LoginForm, MakeTransaction

WRONG_PASSWORD_ERROR = 'Wrong password'
SIGN_TRANSACTION_SUCCESS = 'Transaction succesfully signed and sent'
GREEN_ALERT = 'success'
POST = 'POST'
GET = 'GET'
SAVE_DIR = os.path.join((os.getcwd()), 'addresses')
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def get_all_saved_addresses():
    return [file for file in os.listdir(SAVE_DIR) if os.path.isfile(os.path.join(SAVE_DIR, file))]

addresses = get_all_saved_addresses()
wallet = Wallet()

def refresh():
    addresses = get_all_saved_addresses()

@app.route('/', methods=[GET, POST])
@app.route('/index', methods=[GET, POST])
def index():
    current_address = wallet.current_address
    label = current_address.label if current_address else None
    form = MakeTransaction()
    if form.validate_on_submit():
        transaction = wallet.create_transaction(form.receiver.data, form.amount.data)
        print(Transaction.serialize(transaction))
        flash(SIGN_TRANSACTION_SUCCESS, GREEN_ALERT)
        return redirect('/')
    return render_template('index.html', addresses=addresses, current_address=current_address, label=label, form=form)

@app.route('/login/<label>', methods=[GET, POST])
def login(label):
    if wallet.current_address and wallet.current_address.label == label:
        return redirect('/')
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        if wallet.log_in(str(form.password.data), str(label)):
            return redirect('/')
        error = WRONG_PASSWORD_ERROR
    return render_template('login.html', addresses=addresses, label=label, error=error, form=form)

@app.route('/logout')
def logout():
    wallet.log_out()
    return redirect('/')

@app.route('/test')
def ok():
    wallet.log_in('aaaaaaaaaaaaaaaa', 'address1')
    return index()
