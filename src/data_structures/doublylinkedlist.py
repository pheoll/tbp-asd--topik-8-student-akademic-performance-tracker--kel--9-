from dataclasses import dataclass
from typing import Optional

# =========================
# NODE DOUBLY LINKED LIST
# =========================

@dataclass
class Node:
    kode_mk: str
    nama_mk: str
    sks: int
    grade: str
    prev: Optional['Node'] = None
    next: Optional['Node'] = None


# =========================
# DOUBLY LINKED LIST
# =========================

class DoublyLinkedList:

    def __init__(self):
        self.head = None
        self.tail = None

    # TAMBAH DATA DI AKHIR
    def tambah_nilai(self, kode_mk, nama_mk, sks, grade):

        baru = Node(kode_mk, nama_mk, sks, grade)

        # jika list kosong
        if self.head is None:
            self.head = baru
            self.tail = baru

        else:
            self.tail.next = baru
            baru.prev = self.tail
            self.tail = baru

    # HAPUS DATA TERAKHIR
    def hapus_terakhir(self):

        if self.head is None:
            print("Data kosong")
            return

        # jika hanya 1 data
        if self.head == self.tail:
            self.head = None
            self.tail = None

        else:
            self.tail = self.tail.prev
            self.tail.next = None

    # TAMPILKAN MAJU
    def tampil_maju(self):

        if self.head is None:
            print("Data kosong")
            return

        temp = self.head

        print("\nTRANSAKSI NILAI (MAJU)")
        print("========================")

        while temp:
            print(f"{temp.kode_mk} | {temp.nama_mk} | {temp.sks} SKS | Grade {temp.grade}")
            temp = temp.next

    # TAMPILKAN MUNDUR
    def tampil_mundur(self):

        if self.tail is None:
            print("Data kosong")
            return

        temp = self.tail

        print("\nTRANSAKSI NILAI (MUNDUR)")
        print("========================")

        while temp:
            print(f"{temp.kode_mk} | {temp.nama_mk} | {temp.sks} SKS | Grade {temp.grade}")
            temp = temp.prev

    # HITUNG IPK
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
# PROGRAM UTAMA
# =========================

dll = DoublyLinkedList()

# tambah data
dll.tambah_nilai("IF101", "Algoritma", 3, "A")
dll.tambah_nilai("IF102", "Struktur Data", 3, "B+")
dll.tambah_nilai("IF103", "Basis Data", 2, "B")

# tampil maju
dll.tampil_maju()

# tampil mundur
dll.tampil_mundur()

# hitung IPK
print("\nIPK :", dll.hitung_ipk())

# hapus data terakhir
dll.hapus_terakhir()

# tampil setelah dihapus
print("\nSETELAH HAPUS DATA TERAKHIR")
dll.tampil_maju()