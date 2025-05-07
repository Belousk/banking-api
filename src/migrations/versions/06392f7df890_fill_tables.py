"""fill tables with initial data"""

from alembic import op
import sqlalchemy as sa
from hashlib import sha256

# revision identifiers, used by Alembic.
revision = '06392f7df890'
down_revision = '919b7bf773b3'
branch_labels = None
depends_on = None


def upgrade():
    # Добавим клиентов
    op.execute("""
        INSERT INTO clients (id, full_name, email, phone_number, created_at)
        VALUES 
        (1, 'Иван Иванов', 'ivan@example.com', '+79991112233', now()),
        (2, 'Мария Смирнова', 'maria@example.com', '+79995556677', now())
    """)

    # Добавим пользователей
    password1 = sha256('password123'.encode()).hexdigest()
    password2 = sha256('securepass'.encode()).hexdigest()

    op.execute(f"""
        INSERT INTO users (id, email, hashed_password, client_id)
        VALUES
        (1, 'ivan@example.com', '{password1}', 1),
        (2, 'maria@example.com', '{password2}', 2)
    """)

    # Добавим счета
    op.execute("""
        INSERT INTO accounts (id, client_id, account_number, balance, created_at)
        VALUES
        (1, 1, 'ACC1234567890', 15000.00, now()),
        (2, 2, 'ACC9876543210', 27000.50, now())
    """)

    # Добавим карты
    op.execute("""
        INSERT INTO cards (id, account_id, card_number, expiration_date, cvv, card_type)
        VALUES
        (1, 1, '4111111111111111', '2026-12-31', '123', 'debit'),
        (2, 2, '4222222222222222', '2025-06-30', '456', 'credit')
    """)

    # Добавим займы
    op.execute("""
        INSERT INTO loans (id, client_id, loan_amount, interest_rate, start_date, end_date)
        VALUES
        (1, 1, 50000.00, 12.5, '2023-01-01', '2024-01-01'),
        (2, 2, 100000.00, 10.0, '2022-06-01', '2025-06-01')
    """)

    # Добавим платежи по займам
    op.execute("""
        INSERT INTO payments (id, loan_id, payment_amount, payment_date)
        VALUES
        (1, 1, 10000.00, now()),
        (2, 2, 25000.00, now())
    """)

    # Добавим транзакции
    op.execute("""
        INSERT INTO transactions (id, sender_account_id, receiver_account_id, amount, transaction_type, description, transaction_date)
        VALUES
        (1, 1, 2, 5000.00, 'transfer', 'Перевод между клиентами', now())
    """)


def downgrade():
    op.execute("DELETE FROM transactions")
    op.execute("DELETE FROM payments")
    op.execute("DELETE FROM loans")
    op.execute("DELETE FROM cards")
    op.execute("DELETE FROM accounts")
    op.execute("DELETE FROM users")
    op.execute("DELETE FROM clients")
