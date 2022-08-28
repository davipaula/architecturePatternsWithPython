import sqlite3

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from model import Batch, OrderLine
from repository import SqlAlchemyRepository

# TODO these tests do not work


# #
# # @pytest.fixture(scope="session")
# # def engine():
# #     return create_engine("postgresql://localhost/test_database")
#
#
# @pytest.fixture
# def session():
#     connection = sqlite3.connect(':memory:')
#     db_session = connection.cursor()
#     yield db_session
#     connection.close()
#
#
# @pytest.fixture
# def setup_db(session):
#     session.execute("""CREATE TABLE oder_line (id text, sku text, quantity integer)""")
#
#
# @pytest.mark.usefixtures("setup_db")
# def insert_order_line(session):
#     order_reference = "order"
#     sku = "GENERIC-SOFA"
#     quantity = 12
#
#     session.execute(
#         f"""
#         INSERT INTO order_line (id, sku, quantity)
#         VALUES ("{order_reference}", "{sku}", {quantity})
#         """
#     )
#
#     order_line_id = session.execute(
#         "SELECT id FROM order_line WHERE order_id=:order_id AND sku=:sku",
#         {"order_id": order_reference, "sku": sku}
#     )
#
#     return [[order_line_id]]
#
#
# def insert_batch(session, batch_id):
#     return ""
#
#
# def test_when_batch_is_saved_to_repository_then_data_is_persisted(session):
#     batch_reference = "batch"
#     sku = "RUSTY-SOAPDISH"
#     batch_quantity = 100
#     eta = None
#
#     batch = Batch(batch_reference, sku, batch_quantity, eta)
#
#     repository = SqlAlchemyRepository(session)
#
#     repository.add(batch)
#     session.commit()
#
#     rows = session.execute("SELECT reference, sku, purchased_quantity, eta FROM batch")
#
#     assert list(rows) == [(batch_reference, sku, batch_quantity, eta)]
#
#
# def test_when_batch_is_retrieved_then_repository_returns_allocations(session):
#     order_line_id = insert_order_line(session)
#
#     first_batch_id = insert_batch(session, "first_batch")
#     second_batch_id = insert_batch(session, "second_batch")
#
#     sku = "GENERIC-SOFA"
#
#     # insert_allocation(session, order_line_id, first_batch_id)
#
#     repository = SqlAlchemyRepository(session)
#
#     retrieved = repository.get("first_batch")
#
#     expected_result = Batch("first_batch", sku, 100, None)
#
#     assert retrieved == expected_result
#     assert retrieved.sku == expected_result.sku
#
#     # Check the assertions below. Where are we defining the relationships? And are these names consistent?
#     # assert retrieved._purchased_quantity == expected_result._purchased_quantity
#     # assert retrieved._allocations == {OrderLine("order", sku, 12)}
