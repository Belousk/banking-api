"""fill tabeles

Revision ID: d71e288c956d
Revises: e1dc63dfb6c2
Create Date: 2025-04-27 12:13:48.423970

"""
from typing import Sequence, Union
from datetime import datetime, date
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd71e288c956d'
down_revision: Union[str, None] = 'e1dc63dfb6c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Fill tables with sample data."""
    # Insert clients
    op.bulk_insert(
        sa.table(
            'clients',
            sa.column('id', sa.Integer),
            sa.column('full_name', sa.String),
            sa.column('email', sa.String),
            sa.column('phone_number', sa.String),
            sa.column('created_at', sa.TIMESTAMP),
        ),
        [
            {"id": 1, "full_name": "Alice Smith", "email": "alice@example.com", "phone_number": "+1234567890", "created_at": datetime.utcnow()},
            {"id": 2, "full_name": "Bob Johnson", "email": "bob@example.com", "phone_number": "+1987654321", "created_at": datetime.utcnow()},
            {"id": 3, "full_name": "Charlie Brown", "email": "charlie@example.com", "phone_number": "+1122334455", "created_at": datetime.utcnow()},
            {"id": 4, "full_name": "Diana Prince", "email": "diana@example.com", "phone_number": "+1223344556", "created_at": datetime.utcnow()},
            {"id": 5, "full_name": "Ethan Hunt", "email": "ethan@example.com", "phone_number": "+1334455667", "created_at": datetime.utcnow()},
        ]
    )

    # Insert accounts
    op.bulk_insert(
        sa.table(
            'accounts',
            sa.column('id', sa.Integer),
            sa.column('client_id', sa.Integer),
            sa.column('account_number', sa.String),
            sa.column('balance', sa.Numeric),
            sa.column('created_at', sa.TIMESTAMP),
        ),
        [
            {"id": 1, "client_id": 1, "account_number": "ACC1234567890", "balance": 10000.00, "created_at": datetime.utcnow()},
            {"id": 2, "client_id": 2, "account_number": "ACC2234567890", "balance": 15000.00, "created_at": datetime.utcnow()},
            {"id": 3, "client_id": 3, "account_number": "ACC3234567890", "balance": 8000.00, "created_at": datetime.utcnow()},
            {"id": 4, "client_id": 4, "account_number": "ACC4234567890", "balance": 12000.00, "created_at": datetime.utcnow()},
            {"id": 5, "client_id": 5, "account_number": "ACC5234567890", "balance": 5000.00, "created_at": datetime.utcnow()},
        ]
    )

    # Insert loans
    op.bulk_insert(
        sa.table(
            'loans',
            sa.column('id', sa.Integer),
            sa.column('client_id', sa.Integer),
            sa.column('loan_amount', sa.Numeric),
            sa.column('interest_rate', sa.Numeric),
            sa.column('start_date', sa.Date),
            sa.column('end_date', sa.Date),
        ),
        [
            {"id": 1, "client_id": 1, "loan_amount": 5000.00, "interest_rate": 5.5, "start_date": date(2025, 1, 1), "end_date": date(2026, 1, 1)},
            {"id": 2, "client_id": 2, "loan_amount": 7000.00, "interest_rate": 6.0, "start_date": date(2025, 2, 1), "end_date": date(2026, 2, 1)},
            {"id": 3, "client_id": 3, "loan_amount": 3000.00, "interest_rate": 4.8, "start_date": date(2025, 3, 1), "end_date": date(2026, 3, 1)},
        ]
    )

    # Insert cards
    op.bulk_insert(
        sa.table(
            'cards',
            sa.column('id', sa.Integer),
            sa.column('account_id', sa.Integer),
            sa.column('card_number', sa.String),
            sa.column('expiration_date', sa.Date),
            sa.column('cvv', sa.String),
            sa.column('card_type', sa.String),
        ),
        [
            {"id": 1, "account_id": 1, "card_number": "4111111111111111", "expiration_date": date(2028, 5, 31), "cvv": "123", "card_type": "debit"},
            {"id": 2, "account_id": 2, "card_number": "4222222222222222", "expiration_date": date(2027, 11, 30), "cvv": "456", "card_type": "credit"},
            {"id": 3, "account_id": 3, "card_number": "4333333333333333", "expiration_date": date(2029, 6, 30), "cvv": "789", "card_type": "debit"},
        ]
    )

    # Insert payments
    op.bulk_insert(
        sa.table(
            'payments',
            sa.column('id', sa.Integer),
            sa.column('loan_id', sa.Integer),
            sa.column('payment_amount', sa.Numeric),
            sa.column('payment_date', sa.TIMESTAMP),
        ),
        [
            {"id": 1, "loan_id": 1, "payment_amount": 500.00, "payment_date": datetime.utcnow()},
            {"id": 2, "loan_id": 2, "payment_amount": 700.00, "payment_date": datetime.utcnow()},
            {"id": 3, "loan_id": 3, "payment_amount": 300.00, "payment_date": datetime.utcnow()},
        ]
    )

    # Insert transactions
    op.bulk_insert(
        sa.table(
            'transactions',
            sa.column('id', sa.Integer),
            sa.column('sender_account_id', sa.Integer),
            sa.column('receiver_account_id', sa.Integer),
            sa.column('amount', sa.Numeric),
            sa.column('transaction_type', sa.Enum('debit', 'credit', 'transfer', name='transaction_type_enum')),
            sa.column('description', sa.Text),
            sa.column('transaction_date', sa.TIMESTAMP),
        ),
        [
            {"id": 1, "sender_account_id": 1, "receiver_account_id": 2, "amount": 1000.00, "transaction_type": "transfer", "description": "Payment for invoice #123", "transaction_date": datetime.utcnow()},
            {"id": 2, "sender_account_id": 2, "receiver_account_id": 3, "amount": 500.00, "transaction_type": "transfer", "description": "Gift", "transaction_date": datetime.utcnow()},
            {"id": 3, "sender_account_id": None, "receiver_account_id": 1, "amount": 2000.00, "transaction_type": "credit", "description": "Salary deposit", "transaction_date": datetime.utcnow()},
            {"id": 4, "sender_account_id": 3, "receiver_account_id": None, "amount": 300.00, "transaction_type": "debit", "description": "ATM withdrawal", "transaction_date": datetime.utcnow()},
        ]
    )
