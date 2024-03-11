import sqlite3
from random import randint

class Ledger: 
    def __init__(self, db_file): 
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            balance REAL,
                            debt REAL)''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS debts (
                            id INTEGER PRIMARY KEY,
                            account_id INTEGER,
                            amount REAL)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                            id INTEGER PRIMARY KEY,
                            sender_id INTEGER,
                            receiver_id INTEGER,
                            amount REAL)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS debt_transactions (
                            id INTEGER PRIMARY KEY,
                            sender_id INTEGER,
                            receiver_id INTEGER,
                            debt_id INTEGER)''')

        self.connection.commit()

    def create_account(self, name):        
        balance = 100 
        debt = 0
        id = randint(1000, 10000)
        self.cursor.execute("INSERT INTO accounts (name, balance, debt) VALUES (?, ?, ?)", (name, balance, debt))
        self.connection.commit()
        return self.cursor.lastrowid

    def transaction(self, sender_id, receiver_id, amount): 
        self.cursor.execute("SELECT * FROM accounts WHERE id=?", (sender_id,))
        sender = self.cursor.fetchone()
        self.cursor.execute("SELECT * FROM accounts WHERE id=?", (receiver_id,))
        receiver = self.cursor.fetchone()

        if not sender or not receiver: 
            exit(f'invalid account/accounts')

        if amount > sender[2]: 
            sender_balance = sender[2]
            debt_amount = amount - sender_balance
            sender_balance = 0
            receiver_balance = receiver[2] + sender_balance
            self.cursor.execute("UPDATE accounts SET balance = ?, debt = ? WHERE id = ?", (sender_balance, debt_amount, sender_id))
            self.cursor.execute("UPDATE accounts SET balance = ? WHERE id = ?", (receiver_balance, receiver_id))
            debt_id = self.create_debt(sender_id, debt_amount)
            self.create_debt_transaction(sender_id, receiver_id, debt_id)
            return debt_id
        else: 
            sender_balance = sender[2] - amount
            receiver_balance = receiver[2] + amount
            self.cursor.execute("UPDATE accounts SET balance = ? WHERE id = ?", (sender_balance, sender_id))
            self.cursor.execute("UPDATE accounts SET balance = ? WHERE id = ?", (receiver_balance, receiver_id))
            transaction = self.create_transaction(sender_id, receiver_id, amount)
            print("transaction successful")
            return transaction

    def create_debt(self, account_id, amount): 
        self.cursor.execute("INSERT INTO debts (account_id, amount) VALUES (?, ?)", (account_id, amount))
        self.connection.commit()
        return self.cursor.lastrowid

    def create_transaction(self, sender_id, receiver_id, amount):
        self.cursor.execute("INSERT INTO transactions (sender_id, receiver_id, amount) VALUES (?, ?, ?)", (sender_id, receiver_id, amount))
        self.connection.commit()
        return [sender_id, receiver_id, amount]

    def create_debt_transaction(self, sender_id, receiver_id, debt_id):
        self.cursor.execute("INSERT INTO debt_transactions (sender_id, receiver_id, debt_id) VALUES (?, ?, ?)", (sender_id, receiver_id, debt_id))
        self.connection.commit()

    def close(self):
        self.connection.close()

# Example usage:
ledger = Ledger("ledger.db")
sender_id = ledger.create_account("Akshat")
receiver_id = ledger.create_account("Bob")
transaction_status = ledger.transaction(sender_id, receiver_id, 50)
print(transaction_status)
ledger.close

