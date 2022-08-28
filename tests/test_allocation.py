from datetime import date, timedelta

import pytest

from model import OrderLine, Batch, allocate, OutOfStock

ORDER_REFERENCE = "order-ref"
BATCH_REFERENCE = "batch-001"

TODAY = date.today()
TOMORROW = TODAY + timedelta(days=1)
LATER = TODAY + timedelta(days=100)


def prepare_batch_and_order(sku: str, batch_quantity: int, order_quantity: int) -> tuple[Batch, OrderLine]:
    return (
        Batch("batch--01", sku, batch_quantity, eta=date.today()),
        OrderLine("order-123", sku, order_quantity)
    )


def test_when_order_is_allocated_to_the_batch_then_available_quantity_is_reduced():
    batch_quantity = 20
    order_quantity = 2
    expected_result = 18

    batch = Batch("batch-001", "SMALL-TABLE", quantity=batch_quantity, eta=date.today())
    line = OrderLine("order-ref", "SMALL-TABLE", order_quantity)

    batch.allocate(line)

    assert batch.available_quantity == expected_result


def test_when_available_quantity_is_more_than_order_line_then_order_is_allocated():
    batch, order_line = prepare_batch_and_order("ELEGANT-LAMP", 20, 2)

    assert batch.can_allocate(order_line)


def test_when_available_quantity_is_less_than_order_line_then_order_is_not_allocated():
    batch, order_line = prepare_batch_and_order("ELEGANT-LAMP", 2, 20)

    assert batch.can_allocate(order_line) is False


def test_when_available_quantity_is_equal_to_the_order_line_then_order_is_allocated():
    batch, order_line = prepare_batch_and_order("ELEGANT-LAMP", 2, 2)

    assert batch.can_allocate(order_line)


def test_when_skus_do_not_match_then_order_line_is_not_allocated():
    batch = Batch("batch-001", "UNCOMFORTABLE-CHAIR", 100, eta=None)
    order_line = OrderLine("order-123", "EXPENSIVE-TOASTER", 10)

    assert batch.can_allocate(order_line) is False


def test_when_deallocating_unallocated_line_then_available_quantity_does_not_change():
    batch_quantity = 20
    order_quantity = 2
    expected_result = 20

    batch = Batch(BATCH_REFERENCE, "SMALL-TABLE", quantity=batch_quantity, eta=date.today())
    line = OrderLine(ORDER_REFERENCE, "SMALL-TABLE", order_quantity)

    batch.deallocate(line)

    assert batch.available_quantity == expected_result


def test_when_order_is_allocated_to_the_same_batch_twice_then_quantity_is_not_reduced():
    batch_quantity = 20
    order_quantity = 2
    expected_result = 18

    batch = Batch(BATCH_REFERENCE, "SMALL-TABLE", quantity=batch_quantity, eta=date.today())
    line = OrderLine(ORDER_REFERENCE, "SMALL-TABLE", order_quantity)

    batch.allocate(line)
    batch.allocate(line)

    assert batch.available_quantity == expected_result


def test_when_order_is_allocated_then_in_stock_batch_is_prioritized():
    sku = "RETRO-CLOCK"
    in_stock_quantity = 100
    shipment_batch_quantity = 100
    order_line_quantity = 10

    in_stock_expected_result = 90
    shipment_batch_expected_result = 100

    in_stock_batch = Batch("in-stock-batch", sku, in_stock_quantity, eta=None)
    shipment_batch = Batch("shipment-batch", sku, shipment_batch_quantity, eta=date.today() + timedelta(days=1))
    order_line = OrderLine("order-line", sku, order_line_quantity)

    allocate(order_line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == in_stock_expected_result
    assert shipment_batch.available_quantity == shipment_batch_expected_result


def test_when_order_is_allocated_then_it_prefers_earlier_batches():
    sku = "MINIMALIST-SPOON"

    today_batch_quantity = 100
    tomorrow_batch_quantity = 100
    later_batch_quantity = 100

    order_quantity = 10

    today_batch_expected_result = 90
    tomorrow_batch_expected_result = 100
    later_batch_expected_result = 100

    today_batch = Batch("today", sku, today_batch_quantity, eta=TODAY)
    tomorrow_batch = Batch("tomorrow", sku, tomorrow_batch_quantity, eta=TOMORROW)
    later_batch = Batch("later", sku, later_batch_quantity, eta=LATER)

    order_line = OrderLine("order-line", sku, order_quantity)

    allocate(order_line, [later_batch, tomorrow_batch, today_batch])

    assert today_batch.available_quantity == today_batch_expected_result
    assert tomorrow_batch.available_quantity == tomorrow_batch_expected_result
    assert later_batch.available_quantity == later_batch_expected_result


def test_when_order_is_allocated_then_allocated_batch_reference_is_returned():
    sku = "HIGHBROW-POSTER"

    in_stock_quantity = 100
    shipment_quantity = 100

    order_quantity = 10

    in_stock_batch = Batch("in-stock-reference", sku, in_stock_quantity, eta=None)
    shipment_batch = Batch("shipment-batch-reference", sku, shipment_quantity, eta=TOMORROW)

    order_line = OrderLine("order-line", sku, order_quantity)

    allocation = allocate(order_line, [in_stock_batch, shipment_batch])

    assert allocation == in_stock_batch.reference


def test_when_order_cannot_be_allocated_then_exception_is_raised():
    sku = "SMALL-FORK"

    batch = Batch("batch", sku, 10, eta=TODAY)
    order_line = OrderLine("order", sku, 10)

    allocate(order_line, [batch])

    with pytest.raises(OutOfStock, match=sku):
        allocate(order_line, [batch])
