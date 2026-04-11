# Minimum Heap

Implement a minimum heap.

This should be a class `MinHeap`. It should have the following methods:
- `push(self, item: int) -> None` which adds an item to the heap.
- `peek(self) -> int` which returns the minimal value currently in the heap. If the heap is empty, raise an `IndexError`.
- `pop(self) -> int` which returns the minimal value currently in the heap, and removes it. If the heap is empty, raise an `IndexError`.
- `__len__(self) -> int` which returns the number of items currently in the heap.
- `__bool__(self) -> bool` which returns `True` if there are items in the heap, and `False` otherwise.