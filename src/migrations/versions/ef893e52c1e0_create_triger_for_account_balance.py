"""create triger for account balance

Revision ID: ef893e52c1e0
Revises: a8cf8def4377
Create Date: 2025-05-09 16:55:19.050514

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef893e52c1e0'
down_revision: Union[str, None] = 'a8cf8def4377'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
    CREATE OR REPLACE FUNCTION update_account_balance() RETURNS TRIGGER AS $$
    BEGIN
      UPDATE accounts
      SET balance = (
        SELECT COALESCE(SUM(balance), 0)
        FROM cards
        WHERE cards.account_id = NEW.account_id
      )
      WHERE id = NEW.account_id;
      RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE TRIGGER trigger_update_balance
    AFTER INSERT OR UPDATE OR DELETE ON cards
    FOR EACH ROW
    EXECUTE FUNCTION update_account_balance();
    """)

def downgrade():
    op.execute("DROP TRIGGER IF EXISTS trigger_update_balance ON cards;")
    op.execute("DROP FUNCTION IF EXISTS update_account_balance();")