from typing import Optional, Any, List

class Node:
    """Node untuk Linked List Queue"""
    def __init__(self, data: Any):
        self.data = data
        self.next: Optional['Node'] = None


class Queue:
    """Queue menggunakan Doubly Ended Linked List (FIFO)"""
    
    def __init__(self):
        self.front: Optional[Node] = None
        self.rear: Optional[Node] = None
        self._size: int = 0

    def enqueue(self, data: Any) -> None:
        """Menambahkan elemen di belakang (rear) - Big-O: O(1)"""
        new_node = Node(data)
        
        if self.rear is None:  # Queue kosong
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
            
        self._size += 1

    def dequeue(self) -> Optional[Any]:
        """Menghapus dan mengembalikan elemen di depan (front) - Big-O: O(1)"""
        if self.is_empty():
            return None
        
        assert self.front is not None
        removed_data = self.front.data
        self.front = self.front.next
        
        # Jika queue menjadi kosong setelah dequeue
        if self.front is None:
            self.rear = None
            
        self._size -= 1
        return removed_data

    def peek(self) -> Optional[Any]:
        """Melihat elemen terdepan tanpa menghapus - Big-O: O(1)"""
        if self.is_empty():
            return None
        assert self.front is not None
        return self.front.data

    def is_empty(self) -> bool:
        """Cek apakah queue kosong"""
        return self.front is None

    def size(self) -> int:
        """Mengembalikan jumlah elemen dalam queue"""
        return self._size

    def __len__(self) -> int:
        return self._size

    def clear(self) -> None:
        """Mengosongkan queue"""
        self.front = None
        self.rear = None
        self._size = 0

    def to_list(self) -> List[Any]:
        """Mengubah queue menjadi list (untuk debugging)"""
        result = []
        current = self.front
        while current is not None:
            result.append(current.data)
            current = current.next
        return result