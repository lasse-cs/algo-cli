class MinHeap:
    def __init__(self):
        self._items = []

    def push(self, item: int) -> None:
        self._items.append(item)
        self._bubble_up()

    def _bubble_up(self) -> None:
        index = len(self) - 1
        while index > 0:
            parent = self._parent(index)
            value = self._items[index]
            parent_value = self._items[parent]

            if value >= parent_value:
                break

            self._items[index], self._items[parent] = (
                self._items[parent],
                self._items[index],
            )
            index = parent

    def pop(self) -> int:
        heap_length = len(self)
        if heap_length == 0:
            raise IndexError("pop from empty heap")
        if heap_length == 1:
            return self._items.pop()

        item = self._items[0]
        self._items[0] = self._items.pop()
        self._bubble_down()
        return item

    def _bubble_down(self) -> None:
        index = 0
        while index < len(self):
            value = self._items[index]
            left = self._left(index)
            right = self._right(index)
            if left >= len(self):
                break
            child = left
            if right < len(self) and self._items[right] < self._items[left]:
                child = right
            if value <= self._items[child]:
                break

            self._items[index], self._items[child] = (
                self._items[child],
                self._items[index],
            )
            index = child

    def _parent(self, index: int) -> int:
        return (index - 1) // 2

    def _left(self, index: int) -> int:
        return 2 * index + 1

    def _right(self, index: int) -> int:
        return 2 * index + 2

    def peek(self) -> int:
        if not self:
            raise IndexError("peek from empty heap")
        return self._items[0]

    def __len__(self) -> int:
        return len(self._items)

    def __bool__(self) -> bool:
        return len(self) > 0
