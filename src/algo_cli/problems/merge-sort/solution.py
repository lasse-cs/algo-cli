def merge_sort(array: list[int]) -> list[int]:
    temp = [0] * len(array)

    def sort_range(start: int, end: int) -> None:
        if end - start <= 1:
            return

        mid = (start + end) // 2
        sort_range(start, mid)
        sort_range(mid, end)

        left = start
        right = mid
        write = start

        while left < mid and right < end:
            if array[left] <= array[right]:
                temp[write] = array[left]
                left += 1
            else:
                temp[write] = array[right]
                right += 1
            write += 1

        while left < mid:
            temp[write] = array[left]
            left += 1
            write += 1

        while right < end:
            temp[write] = array[right]
            right += 1
            write += 1

        for idx in range(start, end):
            array[idx] = temp[idx]

    sort_range(0, len(array))
    return array
