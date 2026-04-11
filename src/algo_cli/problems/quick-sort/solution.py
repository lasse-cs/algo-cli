def quick_sort(array: list[int]) -> list[int]:
    def partition(low: int, high: int) -> int:
        pivot = array[high]
        i = low
        for j in range(low, high):
            if array[j] <= pivot:
                array[i], array[j] = array[j], array[i]
                i += 1
        array[i], array[high] = array[high], array[i]
        return i

    def sort_range(low: int, high: int) -> None:
        if low >= high:
            return
        pivot_index = partition(low, high)
        sort_range(low, pivot_index - 1)
        sort_range(pivot_index + 1, high)

    sort_range(0, len(array) - 1)
    return array
