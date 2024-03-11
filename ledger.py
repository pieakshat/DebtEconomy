from random import randint
import sqlite3
class Ledger: 
    def __init__(self): 
        self.transactions=[]
        self.accounts=[]
        self.debts=[]
        self.debt_transactions=[]

    #making accounts 
    def create_account(self, name):        
        balance=100 
        debt=0
        account = { 
            'name': name, 
            'balance': balance,
            'debt': debt
        }
        self.accounts.append(account)
        return account

    def transaction(self, sender, reciever, amount): 
        transaction = { 
            'sender': sender, 
            'reciever': reciever, 
            'amount': amount
        }
        if sender not in self.accounts or reciever not in self.accounts: 
            exit(f'invalid account/accounts')
        if amount > sender['balance']: 
            sender['debt'] = amount
            reciever['balance'] += amount 
            debtid=self.create_debt(sender, amount)
            return debtid
        else: 
            sender['balance'] -= amount
            reciever['balance'] += amount
            print("transaction successful: ", transaction)               

            # using debts as a means of transferring money 
    
    def create_debt(self, account, amount): 
        debt={ 
            'account': account, 
            'id': randint(1, 1000),       
            'amount': amount
        }
        self.debts.append(debt) 
        print(debt)
        return debt['id']

    
    def debt_transaction(self, sender, reciever, debtid): 
        if sender not in self.accounts or reciever not in self.accounts: 
            exit("invalid account/accounts")

        debt_to_transfer=None
        for debt in self.debts: 
            if debt['id'] == debtid: 
                break
            if debt_to_transfer is None: 
                exit('debt does not exist')

        debt_transaction = { 
            'sender': sender, 
            'reciever': reciever, 
            'debt_id': debtid
        }
        debt['account']=reciever
        print("debt transaction successful: ", debt_transaction)
        self.debt_transactions.append(debt_transaction)
        return debt_transaction
    
    # two debts can be added the id of the new debt will be some function 
    #only the debts linked with the same account can be added 
    def add_debts(self, account, debtid1, debtid2): 
        if debtid1 not in self.debts or debtid2 not in self.debts: 
            exit("wrong debt id")
        if account not in self.accounts: 
            exit("invalid account")
        if debtid1['account'] == debtid2['account']: 
            new_account_balance=debtid1['amount'] + debtid2['amount'] 
            newdebt=self.create_debt(account, new_account_balance)
            newdebt['id'] = debtid1['id'] + debtid2['id']
            # I want to keep record of every debt which was derived. I will go forward with merkle trees to do this 
            newdebt['amount'] = debtid1['amount'] + debtid2['amount'] 
            self.debts.pop(debtid1)
            self.debts.pop(debtid2)
            self.debts.append(newdebt)
            print("debts added sucessfully")
    











        








    
