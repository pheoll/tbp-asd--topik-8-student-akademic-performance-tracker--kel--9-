from typing import Optional, List, Any

class NilaiMatkul:
    def __init__(self, kode_mk: str, nama_mk: str, sks: int, grade: str, semester: int):
        self.kode_mk = kode_mk
        self.nama_mk = nama_mk
        self.sks = sks
        self.grade = grade
        self.semester = semester


GRADE_MAP = {
    'A': 4.0, 'A-': 3.7,
    'B+': 3.3, 'B': 3.0,
    'B-': 2.7, 'C+': 2.3,
    'C': 2.0, 'D': 1.0,
    'E': 0.0
}


class Node:
    def __init__(self, data: Any):
        self.data: Any = data
        self.next: Optional['Node'] = None
        self.prev: Optional['Node'] = None


class TranskripNilai:
    def __init__(self):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self._length: int = 0

    def __len__(self) -> int:
        return self._length

    def tambah_nilai(self, nilai: NilaiMatkul) -> None:
        """Menambahkan nilai di akhir (tail) - O(1)"""
        new_node = Node(nilai)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            assert self.tail is not None
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

        self._length += 1

    def hapus_terakhir(self) -> Optional[NilaiMatkul]:
        """Menghapus node terakhir (tail) - O(1)"""
        if self.tail is None:
            return None

        hasil = self.tail.data

        if self.head == self.tail:          # hanya 1 node
            self.head = None
            self.tail = None
        else:
            assert self.tail.prev is not None
            self.tail.prev.next = None
            self.tail = self.tail.prev

        self._length -= 1
        return hasil

    def semester_ke(self, semester: int) -> List[NilaiMatkul]:
        """Mengembalikan list NilaiMatkul pada semester tertentu"""
        result: List[NilaiMatkul] = []
        current: Optional[Node] = self.head

        while current is not None:
            if current.data.semester == semester:
                result.append(current.data)
            current = current.next

        return result

    def hitung_ipk(self) -> float:
        """Menghitung IPK dari semua nilai"""
        if self.head is None:
            return 0.0

        total_bobot = 0.0
        total_sks = 0
        current: Optional[Node] = self.head

        while current is not None:
            nilai = current.data
            bobot = GRADE_MAP.get(nilai.grade, 0.0)
            total_bobot += bobot * nilai.sks
            total_sks += nilai.sks
            current = current.next

        return total_bobot / total_sks if total_sks > 0 else 0.0

    def semua_nilai(self) -> List[NilaiMatkul]:
        """Mengembalikan semua nilai dalam urutan dari head ke tail"""
        result: List[NilaiMatkul] = []
        current: Optional[Node] = self.head

        while current is not None:
            result.append(current.data)
            current = current.next

        return result
