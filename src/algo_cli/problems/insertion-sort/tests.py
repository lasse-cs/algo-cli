from solution import insertion_sort


def test_empty_list():
    assert [] == insertion_sort([])


def test_single_item_list():
    input = [5]
    assert [5] == insertion_sort(input)


def test_long_list():
    input = [1, 5, 6, 7, 90, 11, 2131, 550, 4, 44, 67895, 10]
    assert sorted(input) == insertion_sort(input)
