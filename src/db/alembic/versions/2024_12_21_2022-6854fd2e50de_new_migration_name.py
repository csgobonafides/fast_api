"""new_migration_name

Revision ID: 6854fd2e50de
Revises: c2f97387f912
Create Date: 2024-12-21 20:22:08.911590

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6854fd2e50de'
down_revision: Union[str, None] = 'c2f97387f912'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'manufacturer', ['manufacturer'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'manufacturer', type_='unique')
    # ### end Alembic commands ###