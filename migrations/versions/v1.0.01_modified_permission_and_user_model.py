"""Modified Permission and User model

Revision ID: v1.0.01
Revises: ad0b22ebfb4f
Create Date: 2025-01-01 18:24:22.660565

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'v1.0.01'
down_revision = 'ad0b22ebfb4f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('permission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('permissions', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('permission', sa.Integer(), nullable=True))
        batch_op.drop_constraint('user_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'permission', ['permission'], ['id'])
        batch_op.drop_column('app_right')

    with op.batch_alter_table('user_right', schema=None) as batch_op:
        batch_op.drop_index('id')

    op.drop_table('user_right')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('app_right', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('user_ibfk_1', 'user_right', ['app_right'], ['id'])
        batch_op.drop_column('permission')

    op.create_table('user_right',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=200), nullable=True),
    sa.Column('app_right', mysql.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_swedish_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('user_right', schema=None) as batch_op:
        batch_op.create_index('id', ['id'], unique=True)

    op.drop_table('permission')
    # ### end Alembic commands ###
