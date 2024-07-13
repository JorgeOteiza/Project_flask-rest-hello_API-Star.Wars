"""update alembic_version table

Revision ID: some_revision_id
Revises: previous_revision_id
Create Date: 2024-07-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'some_revision_id'
down_revision = 'previous_revision_id'
branch_labels = None
depends_on = None


def upgrade():
    # Change column type
    op.alter_column('alembic_version', 'version_num',
                    existing_type=sa.String(length=32),
                    type_=sa.String(length=32),
                    existing_nullable=False)

    # Rename column
    op.alter_column('alembic_version', 'version_num',
                    new_column_name='version_num')

    # Change column comment
    op.execute('COMMENT ON COLUMN alembic_version.version_num IS \'comment\'')

    # Drop existing index
    op.drop_index('alembic_version_pkc', table_name='alembic_version')

    # Create new index
    op.create_index('alembic_version_pkc_1720839554322_index', 'alembic_version', ['version_num'], unique=True)


def downgrade():
    # Drop new index
    op.drop_index('alembic_version_pkc_1720839554322_index', table_name='alembic_version')

    # Create old index
    op.create_index('alembic_version_pkc', 'alembic_version', ['version_num'], unique=True)

    # Change column comment back
    op.execute('COMMENT ON COLUMN alembic_version.version_num IS NULL')

    # Rename column back
    op.alter_column('alembic_version', 'version_num',
                    new_column_name='version_num')

    # Change column type back
    op.alter_column('alembic_version', 'version_num',
                    existing_type=sa.String(length=32),
                    type_=sa.String(length=32),
                    existing_nullable=False)
