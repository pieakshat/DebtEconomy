import sqlite3
from random import randint

class Ledger:
    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            balance REAL,
                            debt REAL)''')
        
      
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                            id INTEGER PRIMARY KEY,
                            sender TEXT,
                            receiver TEXT,
                            amount REAL)''')
        

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS debts (
                            id INTEGER PRIMARY KEY,
                            account TEXT,
                            amount REAL)''')
        self.connection.commit()

    def create_account(self, name):
        balance = 100
        debt = 0
        self.cursor.execute("INSERT INTO accounts (name, balance, debt) VALUES (?, ?, ?)", (name, balance, debt))
        self.connection.commit()
        return self.cursor.lastrowid

    def transaction(self, sender, receiver, amount):
        sender_balance = self.get_balance(sender)
        if sender_balance < amount:
            return "Insufficient balance"

        self.cursor.execute("UPDATE accounts SET balance = balance - ? WHERE name = ?", (amount, sender))
        self.cursor.execute("UPDATE accounts SET balance = balance + ? WHERE name = ?", (amount, receiver))

        self.cursor.execute("INSERT INTO transactions (sender, receiver, amount) VALUES (?, ?, ?)",
                            (sender, receiver, amount))
        self.connection.commit()

        return "Transaction successful"

    def create_debt(self, account, amount):
        self.cursor.execute("INSERT INTO debts (account, amount) VALUES (?, ?)", (account, amount))
        self.connection.commit()
        return self.cursor.lastrowid

    def debt_transaction(self, sender, receiver, debt_id):
        self.cursor.execute("SELECT * FROM debts WHERE id = ?", (debt_id,))
        debt = self.cursor.fetchone()
        if not debt:
            return "Debt does not exist"

        self.cursor.execute("UPDATE debts SET account = ? WHERE id = ?", (receiver, debt_id))
        self.connection.commit()

        self.cursor.execute("INSERT INTO transactions (sender, receiver, amount) VALUES (?, ?, ?)",
                            (sender, receiver, debt[2]))
        self.connection.commit()

        return "Debt transaction successful"

    def add_debts(self, account, debt_id1, debt_id2):
        self.cursor.execute("SELECT * FROM debts WHERE id IN (?, ?)", (debt_id1, debt_id2))
        debts = self.cursor.fetchall()

        if len(debts) != 2:
            return "Invalid debt IDs"

        new_debt_amount = debts[0][2] + debts[1][2]

        self.create_debt(account, new_debt_amount)

        self.cursor.execute("DELETE FROM debts WHERE id IN (?, ?)", (debt_id1, debt_id2))
        self.connection.commit()

        return "Debts added successfully"

    def get_balance(self, account_name):
        self.cursor.execute("SELECT balance FROM accounts WHERE name = ?", (account_name,))
        balance = self.cursor.fetchone()
        return balance[0] if balance else None

    def close(self):
        self.connection.close()

ledger = Ledger("ledger.db")

