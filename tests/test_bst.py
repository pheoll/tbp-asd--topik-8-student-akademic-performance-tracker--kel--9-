from typing import Optional, List


class Mahasiswa:
    def __init__(self, nim: str, nama: str):
        self.nim = nim
        self.nama = nama

    def __lt__(self, other: 'Mahasiswa') -> bool:
        return self.nim < other.nim

    def __gt__(self, other: 'Mahasiswa') -> bool:
        return self.nim > other.nim

    def __eq__(self, other: 'Mahasiswa') -> bool:
        if not isinstance(other, Mahasiswa):
            return False
        return self.nim == other.nim


class Node:
    def __init__(self, data: Mahasiswa):
        self.data: Mahasiswa = data
        self.left: Optional['Node'] = None
        self.right: Optional['Node'] = None


class BSTMahasiswa:
    def __init__(self):
        self.root: Optional[Node] = None
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def insert(self, nim: str, nama: str) -> None:
        """Insert Mahasiswa baru berdasarkan NIM (BST property)"""
        mahasiswa = Mahasiswa(nim, nama)
        if self.root is None:
            self.root = Node(mahasiswa)
        else:
            self._insert_recursive(self.root, mahasiswa)
        self._size += 1

    def _insert_recursive(self, node: Node, mahasiswa: Mahasiswa) -> None:
        if mahasiswa < node.data:
            if node.left is None:
                node.left = Node(mahasiswa)
            else:
                self._insert_recursive(node.left, mahasiswa)
        elif mahasiswa > node.data:
            if node.right is None:
                node.right = Node(mahasiswa)
            else:
                self._insert_recursive(node.right, mahasiswa)
        # Jika nim sama, abaikan atau update (sesuai kebutuhan, biasanya abaikan)

    def search(self, nim: str) -> Optional[Mahasiswa]:
        """Cari mahasiswa berdasarkan NIM"""
        current = self.root
        while current is not None:
            if nim == current.data.nim:
                return current.data
            elif nim < current.data.nim:
                current = current.left
            else:
                current = current.right
        return None

    def inorder(self) -> List[Mahasiswa]:
        """Traversal inorder (urut berdasarkan NIM)"""
        result: List[Mahasiswa] = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node: Optional[Node], result: List[Mahasiswa]) -> None:
        if node is not None:
            self._inorder_recursive(node.left, result)
            result.append(node.data)
            self._inorder_recursive(node.right, result)

    def minimum(self) -> Optional[Mahasiswa]:
        """Mahasiswa dengan NIM terkecil"""
        if self.root is None:
            return None
        current = self.root
        while current.left is not None:
            current = current.left
        return current.data

    def maximum(self) -> Optional[Mahasiswa]:
        """Mahasiswa dengan NIM terbesar"""
        if self.root is None:
            return None
        current = self.root
        while current.right is not None:
            current = current.right
        return current.data