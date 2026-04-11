from hypothesis import given, strategies as st

from solution import merge_sort


@given(st.lists(st.integers()))
def test_matches_builtin(items):
    items_copy = items[:]
    assert sorted(items_copy) == merge_sort(items)
