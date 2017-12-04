from wallet import Wallet
from relay_channel import send_transaction

NTX = 5

if __name__ == "__main__":
    w = Wallet()
    logged = w.log_in("DatabasePassword", "DatabaseAddress")
    print("Logged %s" % logged)

    for i in range(NTX):
        print("Creating TX %d" % i)
        tx = w.create_transaction("237479f422db84ca4908bbf1ad0f47680604537c", 11)
        send_transaction(tx)
        print(tx.sender_public_key)
        print()
        print(tx.b64signature)
        print()
        print(tx.hash)
        print()
        print(tx.timestamp)
        print()
        print(tx.receiver)
        print()
