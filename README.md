# simplified-cryptocurrency

Project for the Introduction to cryptography's course: A simplified cryptocurrency.




# Virtualenv and requirements

To run the different components first setup a virtualenv and install the requirements.

To install virtualenv (on Ubuntu):

```bash
sudo apt install virtualenv
```


Create a new virtualenv crypto.


```bash
virtualenv .venv/crypto
```

Activate the virtualenv

```bash
source .venv/crypto/bin/activate
```

Install the packages requirements

```
pip install -r requirements.txt
```

# Setup the network

**Make sure you run those commands in the virtualenv with the requirements**

**The master node must be ran before the relay nodes**

Run the master node on `http://127.0.0.1:8000/master`

```
bash simplcrypto.sh master
```

Run (multiple) relay node on `http://127.0.0.1:800X/relay`

```
bash simplcrypto.sh relay X
```

Where X is the relay number. For example to run 2 relay nodes on 8001 and 8002:

```bash
bash simplcrypto.sh relay 1
```

```bash
bash simplcrypto.sh relay 2
```

# Start a wallet

The wallet is a web-app, available on `http://127.0.0.1:5000`

```bash
cd wallet
python wallet-webapp.py
```

The created/used addresses are store in the directory `addresses/`

# Start a miner

The miner is a command line application using a config file.

Setup the address (to be rewarded) and the relay url in **miner/config.json**
then start the miner

```bash
cd miner
python miner.py
```


