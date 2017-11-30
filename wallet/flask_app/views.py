from flask_app import app
from flask import render_template, request, redirect
import os
import sys
sys.path.append(os.path.dirname(os.getcwd()))
from wallet import Wallet
from .forms import LoginForm

SAVE_DIR = os.path.join((os.getcwd()), 'addresses')

def get_all_saved_addresses():
    return [file for file in os.listdir(SAVE_DIR) if os.path.isfile(os.path.join(SAVE_DIR, file))]

addresses = get_all_saved_addresses()
wallet = Wallet()

def refresh():
    addresses = get_all_saved_addresses()

@app.route('/')
@app.route('/index')
def index():
    current_address = wallet.current_address
    label = current_address.label if current_address else None
    return render_template('index.html', addresses=addresses, current_address=current_address, label=label)

@app.route('/login/<label>', methods=['GET', 'POST'])
def login(label):
    if wallet.current_address and wallet.current_address.label == label:
        return redirect('/')
    form = LoginForm()
    error = None
    if request.method == 'POST':
        if form.validate_on_submit():
            if wallet.log_in(str(form.password.data), str(label)):
                return redirect('/')
            error = "Wrong password"
    return render_template('login.html', addresses=addresses, label=label, error=error, form=form)

@app.route('/logout')
def logout():
    wallet.log_out()
    return redirect('/')

@app.route('/test')
def ok():
    wallet.log_in('aaaaaaaaaaaaaaaa', 'address1')
    return index()
