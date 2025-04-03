"""change price to str

Revision ID: 72c91e801a2b
Revises: 3f260d0c6b3e
Create Date: 2025-04-03 22:22:16.143901

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision: str = '72c91e801a2b'
down_revision: Union[str, None] = '3f260d0c6b3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create a new table with the updated schema
    op.create_table(
        "lots_new",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("auction_id", sa.Integer, sa.ForeignKey("auctions.id")),
        sa.Column("lot_link", sa.String, unique=True),
        sa.Column("lot_title", sa.String),
        sa.Column("lot_number", sa.String),
        sa.Column("price", sa.String),  # Change type to String
        sa.Column("image_links", sa.String),
        sa.Column("is_scraped", sa.Boolean, default=False),
        sa.Column("status", sa.String),
        sa.Column("created_at", sa.DateTime, default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column("scraped_at", sa.DateTime, nullable=True),
        sa.Column("lot_description", sa.String, nullable=True),
    )

    # Copy data from the old table to the new table
    op.execute(
        """
        INSERT INTO lots_new (id, auction_id, lot_link, lot_title, lot_number, price, image_links, is_scraped, status, created_at, updated_at, scraped_at, lot_description)
        SELECT id, auction_id, lot_link, lot_title, lot_number, price, image_links, is_scraped, status, created_at, updated_at, scraped_at, lot_description
        FROM lots
        """
    )

    # Drop the old table
    op.drop_table("lots")

    # Rename the new table to the original table name
    op.rename_table("lots_new", "lots")


def downgrade() -> None:
    """Downgrade schema."""
    # Revert the changes by recreating the old table with the original schema
    op.create_table(
        "lots_old",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("auction_id", sa.Integer, sa.ForeignKey("auctions.id")),
        sa.Column("lot_link", sa.String, unique=True),
        sa.Column("lot_title", sa.String),
        sa.Column("lot_number", sa.String),
        sa.Column("price", sa.Float),  # Revert type to Float
        sa.Column("image_links", sa.String),
        sa.Column("is_scraped", sa.Boolean, default=False),
        sa.Column("status", sa.String),
        sa.Column("lot_description", sa.String, nullable=True),
        sa.Column("created_at", sa.DateTime, default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column("scraped_at", sa.DateTime, nullable=True),
    )

    # Copy data back to the old table
    op.execute(
        """
        INSERT INTO lots_old (id, auction_id, lot_link, lot_title, lot_number, price, image_links, is_scraped, status, created_at, updated_at, scraped_at, lot_description)
        SELECT id, auction_id, lot_link, lot_title, lot_number, price, image_links, is_scraped, status, created_at, updated_at, scraped_at, lot_description
        FROM lots
        """
    )

    # Drop the current table
    op.drop_table("lots")

    # Rename the old table back to the original name
    op.rename_table("lots_old", "lots")
