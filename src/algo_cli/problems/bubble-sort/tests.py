from hypothesis import given, strategies as st

from solution import bubble_sort


@given(st.lists(st.integers()))
def test_matches_builtin(items):
    assert sorted(items) == bubble_sort(items)
