from ledger.ledger import * 

ledger=Ledger()
account1=ledger.create_account("akshat")
account2=ledger.create_account("soham")
id=ledger.transaction(account1, account2, 110)
ledger.debt_transaction(account1 ,account2, id)