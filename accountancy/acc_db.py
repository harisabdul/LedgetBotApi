from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

# # Database engine and session setup
# engine = create_engine('sqlite:///acc.db')
# Base.metadata.create_all(engine)

# Replace with your actual details
DB_USER = "haris"
DB_PASSWORD = "goldcoin"
DB_NAME = "db_clarence_one"
INSTANCE_CONNECTION_NAME = "clarencefashion:us-central1:clarence-db"

# Use Public or Private IP (if applicable)
DB_HOST = "35.222.80.37"  # Replace with actual IP
DB_PORT = "5432"

# Create connection string
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine
engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)


# Define the AccountGroup, Account, and JournalEntry models
class AccountGroup(Base):
    __tablename__ = 'account_group'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    account_title = Column(String(15))
    
    def __init__(self, name, account_title):
        self.name = name
        self.account_title = account_title

class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    account_group_id = Column(Integer, ForeignKey('account_group.id'))
    date = Column(DateTime)
    account_group = relationship('AccountGroup')

    def __init__(self, name, account_group_id, date):
        self.name = name
        self.account_group_id = account_group_id
        self.date = date

class JournalEntry(Base):
    __tablename__ = 'journal_entry'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    description = Column(String(50))
    amount = Column(Float)
    account_id = Column(Integer, ForeignKey('account.id'))
    side = Column(String(10))
    
    account = relationship('Account')

    def __init__(self, date, description, amount, account_id, side):
        self.date = date
        self.description = description
        self.amount = amount
        self.account_id = account_id
        self.side = side



class TrialBalance(Base):
    __tablename__ = 'trial_balance'
    id = Column(Integer, primary_key=True, autoincrement=True)
    account_title = Column(String(50))
    account_group = Column(String(50))
    account_name = Column(String(50))
    debit = Column(Float, default=0.0)
    credit = Column(Float, default=0.0)
    date_generated = Column(DateTime, default=datetime.utcnow)

    def __init__(self, account_title, account_group, account_name, debit, credit):
        self.account_title = account_title
        self.account_group = account_group
        self.account_name = account_name
        self.debit = debit
        self.credit = credit







def create_account_group(account_group_name, account_title):
    Session = sessionmaker(bind=engine)
    session = Session()

    # Check if account group already exists
    existing_account_group = session.query(AccountGroup).filter_by(name=account_group_name).first()
    
    if existing_account_group is None:
        account_group = AccountGroup(account_group_name, account_title)
        session.add(account_group)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            # Handle exception if necessary
    else:
        print(f"Account group '{account_group_name}' already exists.")
    
def create_account(account_name, account_group_id, date_str):
    date = datetime.strptime(date_str, '%Y-%m-%d')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Check if account already exists
    existing_account = session.query(Account).filter_by(name=account_name, account_group_id=account_group_id).first()
    
    if existing_account is None:
        account = Account(account_name, account_group_id, date)
        session.add(account)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            # Handle exception if necessary
    else:
        print(f"Account '{account_name}' already exists in this group.")


def create_journal_entry(date_str, description, amount, account_id, side):
    date = datetime.strptime(date_str, '%Y-%m-%d')
    Session = sessionmaker(bind=engine)
    session = Session()

    journal_entry = JournalEntry(date, description, amount, account_id, side)
    session.add(journal_entry)
    session.commit()




def fetch_journal_entries_between_dates(start_date_str, end_date_str, account_id=None, account_group_id=None):
    # Convert string to datetime objects
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    
    Session = sessionmaker(bind=engine)
    session = Session()

    # Start with the base query
    query = session.query(JournalEntry).filter(JournalEntry.date.between(start_date, end_date))
    
    # Apply account filter if provided
    if account_id:
        query = query.filter_by(account_id=account_id)
    
    # Apply account group filter if provided
    if account_group_id:
        # Fetch accounts in the given group
        accounts_in_group = session.query(Account).filter_by(account_group_id=account_group_id).all()
        query = query.filter(JournalEntry.account_id.in_([account.id for account in accounts_in_group]))

    # Execute the query and fetch the results
    journal_entries = query.all()
    return journal_entries







def fetch_account_group_by_name(account_group_name):
    Session = sessionmaker(bind=engine)
    session = Session()

    # Fetch account group by name using keyword arguments
    account_group = session.query(AccountGroup).filter_by(name=account_group_name).first()
    return account_group



def fetch_all_account_groups():
    Session = sessionmaker(bind=engine)
    session = Session()

    # Fetch all account groups
    account_groups = session.query(AccountGroup).all()
    return account_groups


def fetch_account_by_name(account_name, account_group_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    # Fetch account by name and group ID
    account = session.query(Account).filter_by(name=account_name, account_group_id=account_group_id).first()
    return account



def fetch_all_accounts_by_group(account_group_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    # Fetch all accounts in a given group
    accounts = session.query(Account).filter_by(account_group_id=account_group_id).all()
    return accounts


def update_account_group(account_group_id, **kwargs):
    Session = sessionmaker(bind=engine)
    session = Session()

    # Update account group based on the given keyword arguments
    account_group = session.query(AccountGroup).filter_by(id=account_group_id).first()
    
    if account_group:
        for key, value in kwargs.items():
            setattr(account_group, key, value)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            # Handle exception if necessary
    else:
        print(f"Account group with ID {account_group_id} not found.")




def update_account(account_id, **kwargs):
    Session = sessionmaker(bind=engine)
    session = Session()

    # Update account based on the given keyword arguments
    account = session.query(Account).filter_by(id=account_id).first()

    if account:
        for key, value in kwargs.items():
            setattr(account, key, value)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            # Handle exception if necessary
    else:
        print(f"Account with ID {account_id} not found.")


def delete_account_group(account_group_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    # Delete account group by ID
    account_group = session.query(AccountGroup).filter_by(id=account_group_id).first()

    if account_group:
        session.delete(account_group)
        session.commit()
    else:
        print(f"Account group with ID {account_group_id} not found.")




def delete_account(account_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    # Delete account by ID
    account = session.query(Account).filter_by(id=account_id).first()

    if account:
        session.delete(account)
        session.commit()
    else:
        print(f"Account with ID {account_id} not found.")










ASSET = 'asset'
LIABILITY = 'liability'
EQUITY = 'equity'
INCOME = 'income'
EXPENSE = 'expense'

account_titles = [ASSET, LIABILITY, EQUITY, INCOME, EXPENSE]

def get_account_groups_with_accounts(start_date, end_date):
    # Fetch all account groups
    account_groups = fetch_all_account_groups()
    
    # Initialize an empty dictionary to store the account groups by their titles
    account_groups_dict = {}

    # Loop through each account group
    for account_group in account_groups:
        # Fetch all accounts under this account group
        accounts = fetch_all_accounts_by_group(account_group.id)
        
        # Ensure account title exists in dictionary
        if account_group.account_title not in account_groups_dict:
            account_groups_dict[account_group.account_title] = {}

        # Initialize account details for this group
        group_accounts = {}

        for account in accounts:
            # Fetch journal entries for this account
            journal_entries = fetch_journal_entries_between_dates(start_date, end_date, account_id=account.id)

            # Calculate debit and credit totals
            debit_total = sum(entry.amount for entry in journal_entries if entry.side.lower() == 'debit')
            credit_total = sum(entry.amount for entry in journal_entries if entry.side.lower() == 'credit')

            # Determine the final balance (debit - credit)
            balance = debit_total - credit_total  # Debit-positive, Credit-negative

            # Store account name and its financial details
            group_accounts[account.name] = {
                "debit": debit_total,
                "credit": credit_total,
                "balance": balance
            }

        # Store the calculated accounts under their respective group name
        account_groups_dict[account_group.account_title][account_group.name] = group_accounts

    return account_groups_dict




def generate_trial_balance(start_date='2009-01-01', end_date='2025-12-31'):
    Session = sessionmaker(bind=engine)
    session = Session()

    # Fetch account groups with balances (You need to implement get_account_groups_with_accounts)
    account_groups_dict = get_account_groups_with_accounts(start_date, end_date)

    trial_balance = []
    
    # Iterate through account titles and their respective groups
    for account_title, groups in account_groups_dict.items():
        for group_name, accounts in groups.items():
            for account_name, details in accounts.items():
                existing_entry = session.query(TrialBalance).filter_by(account_name=account_name).first()

                if existing_entry:
                    # Update the existing record
                    existing_entry.debit = details["debit"]
                    existing_entry.credit = details["credit"]

                elif details["debit"] != details["credit"]:
                    # Create a new record
                    trial_entry = TrialBalance(
                        account_title=account_title,
                        account_group=group_name,
                        account_name=account_name,
                        debit=details["debit"],
                        credit=details["credit"]
                    )
                    session.add(trial_entry)  # Add to the database session
                
            
                    
                    # trial_balance.append({
                    #     "Account Title": account_title,
                    #     "Account Group": group_name,
                    #     "Account Name": account_name,
                    #     "Debit": details["debit"],
                    #     "Credit": details["credit"]
                    # })

    # Commit the transaction
    session.commit()

    # Convert to DataFrame for better handling
    # df = pd.DataFrame(trial_balance)
    
    # # Calculate total debits and credits
    # total_debit = df["Debit"].sum()
    # total_credit = df["Credit"].sum()
    
    # # Ensure trial balance matches
    # print(f"Total Debit: {total_debit}, Total Credit: {total_credit}")
    
    return True








def fetch_trial_balance():
    """Fetches all trial balance records from the database."""
    Session = sessionmaker(bind=engine)
    session = Session()

    # Query all records from the trial_balance table
    records = session.query(TrialBalance).all()

    # Convert to a list of dictionaries
    trial_balance_data = [
        {
            "ID": record.id,
            "Account Title": record.account_title,
            "Account Group": record.account_group,
            "Account Name": record.account_name,
            "Debit": record.debit,
            "Credit": record.credit,
            "Date Generated": record.date_generated
        }
        for record in records
    ]

    # Convert to a DataFrame
    # df = pd.DataFrame(trial_balance_data)

    # # Calculate total debits and credits
    # total_debit = df["Debit"].sum()
    # total_credit = df["Credit"].sum()

    # print(f"Total Debit: {total_debit}, Total Credit: {total_credit}")

    return trial_balance_data
