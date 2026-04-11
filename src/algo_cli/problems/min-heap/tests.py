import pytest

from hypothesis import given, strategies as st

from solution import MinHeap


def test_peek_does_not_remove_item():
    heap = MinHeap()

    heap.push(1)
    heap.push(3)
    heap.push(2)

    assert heap.peek() == 1
    assert len(heap) == 3


@given(st.lists(st.integers()))
def test_heap_sort_property(values):
    heap = MinHeap()
    for value in values:
        heap.push(value)
    result = []
    while heap:
        result.append(heap.pop())
    assert sorted(values) == result


@given(st.lists(st.integers()))
def test_length_after_pushes(values):
    heap = MinHeap()
    for value in values:
        heap.push(value)
    assert len(heap) == len(values)


@given(st.lists(st.integers(), min_size=1))
def test_peek_is_minimum(values):
    heap = MinHeap()
    for value in values:
        heap.push(value)
    assert heap.peek() == min(values)


def test_peek_raises_on_empty():
    heap = MinHeap()
    assert len(heap) == 0
    with pytest.raises(IndexError):
        heap.peek()


@given(st.lists(st.integers(), min_size=1))
def test_pop_gets_minimum_value(values):
    heap = MinHeap()
    for value in values:
        heap.push(value)
    assert heap.pop() == min(values)
    assert len(heap) == len(values) - 1
