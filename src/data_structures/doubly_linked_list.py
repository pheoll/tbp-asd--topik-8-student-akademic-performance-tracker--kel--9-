from dataclasses import dataclass


@dataclass
class NilaiMatkul:
    kode_mk: str
    nama_mk: str
    sks: int
    grade: str
    semester: int


GRADE_MAP = {
    'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7,
    'C+': 2.3, 'C': 2.0, 'D': 1.0, 'E': 0.0
}


class DLLNode:
    """Node Doubly Linked List."""

    def __init__(self, data=None):
        self.data = data
        self.prev = None
        self.next = None


class TranskripNilai:
    """
    Doubly Linked List menyimpan riwayat nilai per semester.

    Struktur:
        head <-> node1 <-> node2 <-> ... <-> tail

    Alasan DLL dipilih:
        - tambah_nilai (tail): O(1) karena ada pointer tail langsung
        - hapus_terakhir (undo): O(1) karena tail langsung diakses
        - traversal maju-mundur: O(n) untuk filter semester
        - overhead: 2 pointer per node (prev + next) vs 1 pointer SLL
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def tambah_nilai(self, nilai: NilaiMatkul):
        """
        Sisip node baru di tail (insert tail).

        Big-O Waktu : O(1) — pointer tail langsung, tidak perlu traversal
        Big-O Ruang : O(1) — hanya membuat 1 node baru
        """
        node = DLLNode(nilai)
        if self.tail is None:
            # DLL masih kosong, head dan tail sama
            self.head = node
            self.tail = node
        else:
            # Sambungkan node baru di belakang tail saat ini
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self._size += 1

    def hapus_terakhir(self):
        """
        Hapus node dari tail (undo input nilai terakhir).

        Big-O Waktu : O(1) — tail langsung diakses, tidak perlu traversal
        Big-O Ruang : O(1) — tidak ada alokasi memori tambahan

        Return:
            NilaiMatkul yang dihapus, atau None jika DLL kosong
        """
        if self.tail is None:
            # DLL kosong, tidak ada yang bisa dihapus
            return None

        data = self.tail.data

        if self.head == self.tail:
            # Hanya 1 node tersisa, kosongkan DLL
            self.head = None
            self.tail = None
        else:
            # Geser tail ke node sebelumnya, putus link ke node lama
            self.tail = self.tail.prev
            self.tail.next = None

        self._size -= 1
        return data

    def semester_ke(self, sem: int):
        """
        Filter dan kembalikan list nilai untuk semester tertentu.
        Traversal dilakukan dari head ke tail (maju).

        Big-O Waktu : O(n) — harus menelusuri semua node untuk filter
        Big-O Ruang : O(k) — k = jumlah nilai pada semester sem

        Args:
            sem: nomor semester yang dicari

        Return:
            list NilaiMatkul yang semesternya == sem
        """
        hasil = []
        current = self.head
        while current is not None:
            if current.data.semester == sem:
                hasil.append(current.data)
            current = current.next
        return hasil

    def hitung_ipk(self):
        """
        Hitung IPK berdasarkan semua nilai dalam DLL.
        Rumus: sum(grade_value * sks) / sum(sks)
        Traversal dilakukan dari head ke tail (maju).

        Big-O Waktu : O(n) — menelusuri seluruh node sekali
        Big-O Ruang : O(1) — hanya menyimpan akumulator

        Return:
            float IPK, atau 0.0 jika belum ada nilai
        """
        total_bobot = 0.0
        total_sks = 0
        current = self.head
        while current is not None:
            grade_val = GRADE_MAP.get(current.data.grade, 0.0)
            total_bobot += grade_val * current.data.sks
            total_sks += current.data.sks
            current = current.next

        if total_sks == 0:
            return 0.0
        return total_bobot / total_sks

    def semua_nilai(self):
        """
        Kembalikan semua nilai sebagai list (traversal maju).

        Big-O Waktu : O(n)
        Big-O Ruang : O(n)
        """
        hasil = []
        current = self.head
        while current is not None:
            hasil.append(current.data)
            current = current.next
        return hasil

    def __len__(self):
        return self._size
