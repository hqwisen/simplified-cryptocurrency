from flask_app import app
from flask import flash, render_template, request, redirect
import os
import sys
import requests
sys.path.append(os.path.dirname(os.getcwd()))
sys.path.append(os.pardir)
from wallet import Wallet, Transaction
from .forms import LoginForm, MakeTransactionForm, CreateAddressForm
from relay_channel import send_transaction

WRONG_PASSWORD_ERROR = 'Wrong password'
TRANSACTION_TO_SELF_ERROR = 'Receiver and sender addresses must be different'
TRANSACTION_ALREADY_ADDED = 'Transaction already added to next block'
UNKNOWN_ERROR = 'Unknown error'
SIGN_TRANSACTION_SUCCESS = 'Transaction succesfully signed and sent'
LABEL_ALREADY_EXISTS_ERROR = 'This label already exists, please choose another one'
GREEN_ALERT = 'success'
RED_ALERT = 'danger'
POST = 'POST'
GET = 'GET'
SAVE_DIR = os.path.join((os.getcwd()), 'addresses')
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def get_all_saved_addresses():
    return [file for file in os.listdir(SAVE_DIR) if os.path.isfile(os.path.join(SAVE_DIR, file))]

wallet = Wallet()
wallet.update_blockchain()

@app.route('/refresh_blockchain')
def refresh_blockchain() :
    wallet.update_blockchain()
    return index()

@app.route('/', methods=[GET, POST])
@app.route('/index', methods=[GET, POST])
def index():
    current_address = wallet.current_address
    label = current_address.label if current_address else None
    form = MakeTransactionForm()
    if current_address is not None :
        current_balance = wallet.blockchain.get_balance(wallet.current_address.raw)
    else :
        current_balance = None
    if form.validate_on_submit():
        if form.receiver.data == wallet.current_address.raw :
            return render_template('index.html', addresses=get_all_saved_addresses(), current_address=current_address, current_balance=current_balance, label=label, error=TRANSACTION_TO_SELF_ERROR, form=form)
        transaction = wallet.create_transaction(form.receiver.data, form.amount.data)
        response_status = send_transaction(transaction)
        if response_status == 201 :
            flash(SIGN_TRANSACTION_SUCCESS, GREEN_ALERT)
        elif response_status == 406 :
            flash(TRANSACTION_ALREADY_ADDED, RED_ALERT)
        else :
            flash(UNKNOWN_ERROR, RED_ALERT)
        return redirect('/')
    return render_template('index.html', addresses=get_all_saved_addresses(), current_address=current_address, current_balance=current_balance, label=label, form=form)

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
    return render_template('login.html', addresses=get_all_saved_addresses(), label=label, error=error, form=form)

@app.route('/create_address', methods=[GET, POST])
def create_address():
    form = CreateAddressForm()
    label = wallet.current_address.label if wallet.current_address else None
    error = None
    if form.validate_on_submit():
        if form.label.data not in get_all_saved_addresses():
            new_address = wallet.sign_up(form.password.data, form.label.data)
            return redirect('/')
        else:
            error = LABEL_ALREADY_EXISTS_ERROR
    return render_template('create_address.html', addresses=get_all_saved_addresses(), current_address=wallet.current_address, label=label, form=form, error=error)

@app.route('/logout')
def logout():
    wallet.log_out()
    return redirect('/')