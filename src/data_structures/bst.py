from dataclasses import dataclass
from typing import Optional

# =========================
# DOUBLE LINKED LIST NILAI
# =========================

@dataclass
class NodeNilai:
    kode_mk: str
    nama_mk: str
    sks: int
    grade: str
    prev: Optional['NodeNilai'] = None
    next: Optional['NodeNilai'] = None


class DoublyLinkedListNilai:
    def __init__(self):
        self.head = None
        self.tail = None

    # tambah nilai
    def tambah_nilai(self, kode_mk, nama_mk, sks, grade):
        baru = NodeNilai(kode_mk, nama_mk, sks, grade)

        if self.head is None:
            self.head = self.tail = baru
        else:
            self.tail.next = baru
            baru.prev = self.tail
            self.tail = baru

    # tampilkan transkrip
    def tampilkan(self):
        temp = self.head

        while temp:
            print(f"{temp.kode_mk} | {temp.nama_mk} | {temp.sks} SKS | Grade {temp.grade}")
            temp = temp.next

    # hitung IPK
    def hitung_ipk(self):
        bobot = {
            'A': 4,
            'B+': 3.5,
            'B': 3,
            'C+': 2.5,
            'C': 2,
            'D': 1,
            'E': 0
        }

        total_nilai = 0
        total_sks = 0

        temp = self.head

        while temp:
            total_nilai += bobot[temp.grade] * temp.sks
            total_sks += temp.sks
            temp = temp.next

        if total_sks == 0:
            return 0

        return round(total_nilai / total_sks, 2)


# =========================
# NODE BST MAHASISWA
# =========================

class NodeMahasiswa:
    def __init__(self, nim, nama):
        self.nim = nim
        self.nama = nama
        self.transkrip = DoublyLinkedListNilai()
        self.left = None
        self.right = None


# =========================
# BST MAHASISWA
# =========================

class BSTMahasiswa:
    def __init__(self):
        self.root = None

    # INSERT MAHASISWA
    def insert(self, root, nim, nama):
        if root is None:
            return NodeMahasiswa(nim, nama)

        if nim < root.nim:
            root.left = self.insert(root.left, nim, nama)

        elif nim > root.nim:
            root.right = self.insert(root.right, nim, nama)

        return root

    # SEARCH MAHASISWA
    def search(self, root, nim):
        if root is None or root.nim == nim:
            return root

        if nim < root.nim:
            return self.search(root.left, nim)
        else:
            return self.search(root.right, nim)

    # INORDER
    def inorder(self, root):
        if root:
            self.inorder(root.left)

            print("========================")
            print(f"NIM  : {root.nim}")
            print(f"Nama : {root.nama}")
            print(f"IPK  : {root.transkrip.hitung_ipk()}")
            print("Transkrip:")
            root.transkrip.tampilkan()

            self.inorder(root.right)


# =========================
# PROGRAM UTAMA
# =========================

bst = BSTMahasiswa()

# tambah mahasiswa
bst.root = bst.insert(bst.root, 98, "Aflah")
bst.root = bst.insert(bst.root, 75, "Budi")
bst.root = bst.insert(bst.root, 120, "Citra")

# tambah nilai mahasiswa
mhs1 = bst.search(bst.root, 98)
mhs1.transkrip.tambah_nilai("IF101", "Algoritma", 3, "A")
mhs1.transkrip.tambah_nilai("IF102", "Struktur Data", 3, "B+")

mhs2 = bst.search(bst.root, 75)
mhs2.transkrip.tambah_nilai("IF201", "Basis Data", 2, "B")
mhs2.transkrip.tambah_nilai("IF202", "Python", 3, "A")

mhs3 = bst.search(bst.root, 120)
mhs3.transkrip.tambah_nilai("IF301", "AI", 3, "A")

# tampilkan semua data
print("\nDATA MAHASISWA")
print("========================")
bst.inorder(bst.root)

# pencarian mahasiswa
print("\nPENCARIAN MAHASISWA")
print("========================")

cari = bst.search(bst.root, 98)

if cari:
    print(f"Data ditemukan: {cari.nama}")
    print(f"IPK : {cari.transkrip.hitung_ipk()}")
else:
    print("Data tidak ditemukan")