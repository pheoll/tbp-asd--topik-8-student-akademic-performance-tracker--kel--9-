"""
Modul 2 - BST Data Mahasiswa
=============================
Bertanggung jawab atas operasi BST untuk manajemen data mahasiswa.
Kunci BST = NIM mahasiswa (string, format '21XXXXXXXX').

Fungsi utama:
    - inisialisasi_bst   : generate 60 mahasiswa dengan seed=31 dan insert ke BST (O(n log n))
    - cari_mahasiswa     : search BST berdasarkan NIM (O(log n))
    - daftar_mahasiswa   : tampilkan semua mahasiswa terurut NIM via inorder (O(n))
    - filter_range_ipk   : tampilkan mahasiswa dengan IPK dalam rentang [low, high] (O(n))
"""

import sys
import os
import random

# Tambahkan src/data_structures/ ke path relatif terhadap lokasi FILE INI
# __file__ = .../src/modules/modul_2.py  -> naik 1 level ke src/, lalu masuk data_structures/
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data_structures'))

from bst import BSTMahasiswa, BSTNodeMhs, Mahasiswa

# Seed wajib sesuai panduan — JANGAN diubah agar data dapat direproduksi
random.seed(31)

PRODI = ['Teknik Elektro', 'Informatika', 'Mesin', 'Sipil', 'Kimia']


# ------------------------------------------------------------------ #
#  GENERATE & INISIALISASI BST                                         #
# ------------------------------------------------------------------ #

def generate_mahasiswa(n: int = 60):
    """
    Generate data mahasiswa secara acak dengan seed=31.
    Format NIM: '21XXXXXXXX' (contoh: '2100000001').

    Big-O Waktu : O(n) — loop n kali, setiap iterasi O(1)
    Big-O Ruang : O(n) — list n objek Mahasiswa

    Args:
        n: jumlah mahasiswa yang di-generate (default 60)

    Return:
        list Mahasiswa
    """
    mhs_list = []
    for i in range(1, n + 1):
        nim = f'21{i:08d}'
        prodi = random.choice(PRODI)
        angkatan = random.choice([2021, 2022, 2023])
        mhs_list.append(Mahasiswa(
            nim=nim,
            nama=f'Mahasiswa-{i}',
            prodi=prodi,
            angkatan=angkatan
        ))
    return mhs_list


def inisialisasi_bst(n: int = 60) -> BSTMahasiswa:
    """
    Generate n mahasiswa lalu insert ke BST dengan pre-shuffle untuk
    menghindari BST miring (worst-case O(n) jika NIM dimasukkan berurutan).

    Tanpa shuffle: NIM '2100000001', '2100000002', ... selalu naik
                   -> BST degenerate (miring kanan) -> height = n -> O(n) per operasi
    Dengan shuffle: urutan acak -> BST mendekati seimbang -> height ≈ log n -> O(log n)

    Big-O Waktu : O(n log n) — n kali insert, masing-masing O(log n) rata-rata
    Big-O Ruang : O(n) — n node BST

    Args:
        n: jumlah mahasiswa

    Return:
        BSTMahasiswa yang sudah terisi
    """
    bst = BSTMahasiswa()
    mhs_list = generate_mahasiswa(n)

    # Pre-shuffle untuk menghindari BST miring — O(n)
    random.shuffle(mhs_list)

    # Insert satu per satu ke BST — O(n log n) total
    for mhs in mhs_list:
        bst.insert(mhs)

    return bst


# ------------------------------------------------------------------ #
#  CARI MAHASISWA                                                      #
# ------------------------------------------------------------------ #

def cari_mahasiswa(bst: BSTMahasiswa, nim: str):
    """
    Cari mahasiswa di BST berdasarkan NIM dan tampilkan informasinya.

    Big-O Waktu : O(log n) rata-rata, O(n) worst-case (BST miring)
    Big-O Ruang : O(log n) stack rekursi

    Args:
        bst : BSTMahasiswa
        nim : NIM yang dicari

    Return:
        BSTNodeMhs jika ditemukan, None jika tidak ada
    """
    # Search BST — O(log n)
    node = bst.search(nim)

    if node is None:
        print(f"\n  [INFO] Mahasiswa dengan NIM '{nim}' tidak ditemukan.\n")
        return None

    mhs = node.mhs
    print(f"\n  {'='*50}")
    print(f"  DATA MAHASISWA")
    print(f"  {'='*50}")
    print(f"  NIM      : {mhs.nim}")
    print(f"  Nama     : {mhs.nama}")
    print(f"  Prodi    : {mhs.prodi}")
    print(f"  Angkatan : {mhs.angkatan}")
    print(f"  IPK      : {mhs.ipk:.2f}")
    print(f"  Total MK : {len(node.transkripsi)}")
    print(f"  {'='*50}\n")

    return node


# ------------------------------------------------------------------ #
#  DAFTAR MAHASISWA (INORDER)                                          #
# ------------------------------------------------------------------ #

def daftar_mahasiswa(bst: BSTMahasiswa) -> None:
    """
    Tampilkan semua mahasiswa terurut berdasarkan NIM ascending
    menggunakan inorder traversal BST.

    Big-O Waktu : O(n) — inorder mengunjungi setiap node tepat sekali
    Big-O Ruang : O(n) list hasil + O(h) stack rekursi

    Args:
        bst: BSTMahasiswa
    """
    # Inorder BST — O(n), hasil sudah terurut NIM karena properti BST
    semua = bst.inorder()

    if not semua:
        print("\n  [INFO] BST kosong, belum ada mahasiswa.\n")
        return

    print(f"\n  {'='*70}")
    print(f"  DAFTAR MAHASISWA (Terurut NIM) — Total: {len(semua)}")
    print(f"  {'='*70}")
    print(f"  {'No':>4} {'NIM':<14} {'Nama':<20} {'Prodi':<18} {'Angkatan':>9} {'IPK':>5}")
    print(f"  {'-'*70}")

    for i, mhs in enumerate(semua, 1):
        print(f"  {i:>4} {mhs.nim:<14} {mhs.nama:<20} {mhs.prodi:<18} "
              f"{mhs.angkatan:>9} {mhs.ipk:>5.2f}")

    print(f"  {'='*70}\n")


# ------------------------------------------------------------------ #
#  FILTER RANGE IPK                                                    #
# ------------------------------------------------------------------ #

def filter_range_ipk(bst: BSTMahasiswa, low: float, high: float) -> None:
    """
    Tampilkan mahasiswa yang IPK-nya berada dalam rentang [low, high].

    Catatan Big-O:
        BST diindeks NIM, bukan IPK. Tidak bisa memanfaatkan properti BST
        untuk memangkas pencarian berdasarkan IPK. Seluruh tree harus
        ditelusuri terlebih dahulu (inorder O(n)), baru di-filter.

        Untuk query range_ipk yang lebih cepat (O(log n + k)), diperlukan
        secondary BST dengan kunci IPK — lihat Pertanyaan Analisis no.2.

    Big-O Waktu : O(n) — inorder traversal penuh + filter
    Big-O Ruang : O(n) untuk list hasil inorder

    Args:
        bst  : BSTMahasiswa
        low  : batas bawah IPK (inklusif)
        high : batas atas IPK (inklusif)
    """
    # Inorder + filter IPK — O(n)
    hasil = bst.range_ipk(low, high)

    print(f"\n  {'='*65}")
    print(f"  FILTER IPK [{low:.2f} – {high:.2f}] — Ditemukan: {len(hasil)} mahasiswa")
    print(f"  {'='*65}")

    if not hasil:
        print(f"  [INFO] Tidak ada mahasiswa dengan IPK dalam rentang tersebut.")
        print(f"  {'='*65}\n")
        return

    print(f"  {'No':>4} {'NIM':<14} {'Nama':<20} {'Prodi':<18} {'IPK':>5}")
    print(f"  {'-'*65}")

    for i, mhs in enumerate(hasil, 1):
        print(f"  {i:>4} {mhs.nim:<14} {mhs.nama:<20} {mhs.prodi:<18} {mhs.ipk:>5.2f}")

    print(f"  {'='*65}\n")