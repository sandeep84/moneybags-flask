import piecash
import json 
import babel.numbers

recid = 1

def populateAccountChildrenRecords(account, record, rootCurrency):
    global recid
    for child in account.children:
        # print(f'Populating record for {child.name}')
        accountRecord = {
            'recid': recid,
            'w2ui': {
                'children': []
            }
        }

        recid += 1
        accountRecord['accName'] = child.name
        try:
            accountRecord['accBalance'] = babel.numbers.format_currency(child.get_balance(recurse=True), child.commodity.mnemonic)
            accountRecord['accBalanceGBP'] = babel.numbers.format_currency(child.get_balance(recurse=True, commodity=rootCurrency), rootCurrency.mnemonic)
        except Exception as e:
            accountRecord['accBalance'] = 0
            accountRecord['accBalanceGBP'] = 0
            print(e)
        populateAccountChildrenRecords(child, accountRecord['w2ui']['children'], rootCurrency)

        record.append(accountRecord)

# { recid: 1, fname: 'John', lname: 'doe', email: 'jdoe@gmail.com', sdate: '4/3/2012', w2ui: { children: [] }},
def getAccounts():
    records = list()
    book = piecash.open_book("HomeAccounts.gnucash", readonly=True)
    root = book.root_account
    rootCurrency = book.currencies[0]
    populateAccountChildrenRecords(root, records, rootCurrency)
    book.close()
    # print(json.dumps(records))
    return json.dumps(records, indent=4)

if __name__ == "__main__":
    getAccounts()

