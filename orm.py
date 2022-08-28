from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy.orm import mapper, relationship

import model

metadata = MetaData()

order_line = Table(
    "order_line",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255), nullable=False),
    Column("quantity", Integer, nullable=False),
    Column("order_id", String(255), nullable=False)
)


def start_mappers():
    order_lines_mapper = mapper(model.OrderLine, order_line)
