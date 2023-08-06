import time
import data
import crypto
import finance_db


def record(t_interval=None, t_unit=None):
    t_interval = 5*60
    db = finance_db.FinanceDB()
    accounts = db.conn.cursor().execute("SELECT num FROM accounts "
                                        "WHERE institution = 'QT' OR institution = 'crypto'").fetchall()
    while True:
        for account in accounts:
            print(account)
            data.update_account(db=db, account=account[0])
            crypto_data = db.conn.cursor().execute("SELECT * FROM crypto").fetchall()
            qtrade_data = db.conn.cursor().execute("SELECT * FROM qtrade").fetchall()

            print(crypto_data)
            print(qtrade_data)


        time.sleep(t_interval)


# TODO dashboards to combine all functions - db table(s) to store dashboards - new driver

# TODO budgets - monthly & yearly representations? loading bar with basic prediction
# TODO set desired budgets & store
# TODO assign to dashboard
# TODO display

# TODO flux - monthly & daily per category
# TODO bills - predictions & free cash calcs given goals

