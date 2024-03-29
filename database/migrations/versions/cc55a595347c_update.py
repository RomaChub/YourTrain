"""Update

Revision ID: cc55a595347c
Revises: f95ba987512c
Create Date: 2024-03-12 00:10:59.533335

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc55a595347c'
down_revision: Union[str, None] = 'f95ba987512c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('exercises', sa.Column('training_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'exercises', 'training', ['training_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_constraint('training_exercise_id_fkey', 'training', type_='foreignkey')
    op.drop_column('training', 'exercise_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('training', sa.Column('exercise_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('training_exercise_id_fkey', 'training', 'exercises', ['exercise_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_constraint(None, 'exercises', type_='foreignkey')
    op.drop_column('exercises', 'training_id')
    # ### end Alembic commands ###
