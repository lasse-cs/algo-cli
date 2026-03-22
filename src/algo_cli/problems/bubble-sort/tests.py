from solution import bubble_sort


def test_empty_list():
    assert [] == bubble_sort([])


def test_single_item_list():
    input = [5]
    assert [5] == bubble_sort(input)


def test_long_list():
    input = [1, 5, 6, 7, 90, 11, 2131, 550, 4, 44, 67895, 10]
    assert sorted(input) == bubble_sort(input)
