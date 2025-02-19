from fastapi import FastAPI
from accountancy import create_account_group, create_account, create_journal_entry, fetch_account_by_name, fetch_all_accounts_by_group, fetch_account_group_by_name, fetch_all_account_groups, update_account_group, fetch_journal_entries_between_dates, generate_trial_balance, fetch_trial_balance




app = FastAPI()

@app.post("/account_group")
def account_group(account_group_name, account_title):
    create_account_group(account_group_name, account_title)
    account_group_data = fetch_all_account_groups()
    return account_group_data

@app.post("/account")
def account(account_name, account_group_id, date_str):
    create_account(account_name, account_group_id, date_str)
    account_data = fetch_all_accounts_by_group(account_group_id)
    return account_data

@app.post("/journal_entry")
def journal_entry(date_str, description, amount, account_id, side):
    create_journal_entry(date_str, description, amount, account_id, side)
    return True

@app.post("/trial_balance")
def trial_balance(start_date, end_date):
    generate_trial_balance(start_date, end_date)
    tb_response = fetch_trial_balance()
    return tb_response

@app.get("/ledger")
def get_ledger():
    ledger = {}
    return ledger

# Endpoint to get Profit & Loss Report
@app.get("/income_statement")
def get_income_statement():
    pnl_report = {
    }
    return pnl_report

# Endpoint to get Balance Sheet Report
@app.get("/position_statement")
def get_position_statement():
    balance_sheet = {}
    return balance_sheet

# Main entry point to run the FastAPI app with Uvicorn (in the terminal)
# uvicorn app:app --reload
