"""
main.py - Entry Point CLI
Student Academic Performance Tracker
=====================================
Topik 8 | ELT60213 Algoritma dan Struktur Data | TA 2025/2026

Perintah CLI yang tersedia:
    CARI_MHS <nim>
    INPUT_NILAI <nim> <kode_mk> <sks> <grade> <semester>
    UNDO_NILAI <nim>
    TRANSKRIPSI <nim>
    IPK <nim>
    RANKING_IPK
    FILTER_IPK <min> <max>
    PRASYARAT_CEK <nim> <kode_mk>
    URUTAN_MATKUL
    BANTUAN
    KELUAR
"""

import sys
import os

# Tambahkan src/data_structures/ dan src/modules/ ke path
_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_DIR, 'data_structures'))
sys.path.insert(0, os.path.join(_DIR, 'modules'))

# ── Import data structures ──────────────────────────────────────────
from stack import Stack

# ── Import modul aplikasi ───────────────────────────────────────────
from modul_1 import input_nilai, hapus_nilai_terakhir, lihat_transkripsi, tampilkan_ipk
from modul_2 import inisialisasi_bst, cari_mahasiswa, daftar_mahasiswa, filter_range_ipk
from modul_3 import catat_operasi, undo_operasi, lihat_riwayat
from modul_4 import inisialisasi_kurikulum, urutan_matkul, cek_prasyarat


# ================================================================== #
#  BANNER & BANTUAN                                                    #
# ================================================================== #

BANNER = """
╔══════════════════════════════════════════════════════════════╗
║     STUDENT ACADEMIC PERFORMANCE TRACKER                     ║
║     ELT60213 Algoritma dan Struktur Data | TA 2025/2026      ║
║     Topik 8 | BST + DLL + Stack + Graph DAG                  ║
╚══════════════════════════════════════════════════════════════╝
"""

BANTUAN_TEXT = """
┌─────────────────────────────────────────────────────────────────┐
│  DAFTAR PERINTAH                                                │
├──────────────────────────────────┬──────────────────────────────┤
│  CARI_MHS <nim>                  │  Cari data mahasiswa (O(log n))│
│  INPUT_NILAI <nim> <kode> <sks>  │  Input nilai matakuliah       │
│             <grade> <semester>   │  Big-O: O(1) DLL + O(log n)  │
│  UNDO_NILAI <nim>                │  Batalkan input terakhir (O(1))│
│  TRANSKRIPSI <nim>               │  Lihat transkrip nilai (O(n)) │
│  IPK <nim>                       │  Tampilkan IPK (O(n))         │
│  RANKING_IPK                     │  Ranking semua mahasiswa (O(n))│
│  FILTER_IPK <min> <max>          │  Filter berdasarkan IPK (O(n))│
│  PRASYARAT_CEK <nim> <kode>      │  Cek prasyarat MK (O(deg))    │
│  URUTAN_MATKUL                   │  Topological sort DAG (O(V+E))│
│  DAFTAR_MHS                      │  Daftar semua mahasiswa (O(n))│
│  BANTUAN                         │  Tampilkan menu ini           │
│  KELUAR                          │  Keluar dari program          │
└──────────────────────────────────┴──────────────────────────────┘
Grade valid: A, A-, B+, B, B-, C+, C, D, E
Semester   : 1 – 8
"""


# ================================================================== #
#  MODUL 5: RANKING & SORTING IPK (Merge Sort pada Linked List)     #
# ================================================================== #

def _merge_sort_mhs(mhs_list):
    """
    Merge Sort pada list Mahasiswa berdasarkan IPK descending.

    Big-O Waktu : O(n log n) — lebih efisien dari Insertion Sort O(n²)
    Big-O Ruang : O(n) — list tambahan saat merge

    Perbandingan Merge Sort vs Insertion Sort untuk N=60:
        Merge Sort   : ~60 * log2(60) ≈ 354 operasi
        Insertion Sort: ~60² / 2      ≈ 1800 operasi
    """
    if len(mhs_list) <= 1:
        return mhs_list

    mid   = len(mhs_list) // 2
    kiri  = _merge_sort_mhs(mhs_list[:mid])
    kanan = _merge_sort_mhs(mhs_list[mid:])

    return _merge(kiri, kanan)


def _merge(kiri, kanan):
    """Helper merge: gabungkan dua list terurut menjadi satu (descending IPK)."""
    hasil = []
    i = j = 0
    while i < len(kiri) and j < len(kanan):
        # Descending: IPK lebih besar di depan
        if kiri[i].ipk >= kanan[j].ipk:
            hasil.append(kiri[i])
            i += 1
        else:
            hasil.append(kanan[j])
            j += 1
    hasil.extend(kiri[i:])
    hasil.extend(kanan[j:])
    return hasil


def tampilkan_ranking(bst):
    """
    Tampilkan ranking semua mahasiswa berdasarkan IPK menggunakan Merge Sort.

    Big-O Waktu : O(n) inorder + O(n log n) merge sort = O(n log n)
    Big-O Ruang : O(n)
    """
    # Ambil semua mahasiswa via inorder BST — O(n)
    semua = bst.inorder()

    if not semua:
        print("\n  [INFO] Belum ada mahasiswa.\n")
        return

    # Merge Sort berdasarkan IPK descending — O(n log n)
    terurut = _merge_sort_mhs(semua)

    print(f"\n  {'='*70}")
    print(f"  RANKING IPK — Merge Sort O(n log n) | N={len(terurut)}")
    print(f"  {'='*70}")
    print(f"  {'Rank':>5} {'NIM':<14} {'Nama':<20} {'Prodi':<18} {'IPK':>5}")
    print(f"  {'-'*70}")

    for rank, mhs in enumerate(terurut, 1):
        print(f"  {rank:>5} {mhs.nim:<14} {mhs.nama:<20} {mhs.prodi:<18} {mhs.ipk:>5.2f}")

    print(f"  {'='*70}\n")


# ================================================================== #
#  MAIN CLI LOOP                                                       #
# ================================================================== #

def main():
    print(BANNER)
    print("  Menginisialisasi sistem...")

    # Inisialisasi BST dengan 60 mahasiswa (seed=31)
    bst = inisialisasi_bst(60)
    print(f"  ✓ BST: 60 mahasiswa berhasil dimuat (pre-shuffle, O(n log n))")

    # Inisialisasi Stack global untuk undo
    undo_stack = Stack()
    print(f"  ✓ Stack: riwayat undo siap (O(1) push/pop)")

    # Inisialisasi Graph DAG prasyarat matakuliah
    graph = inisialisasi_kurikulum()
    print(f"  ✓ Graph DAG: 40 MK, 55 relasi prasyarat dimuat (O(V+E))")

    print(f"\n  Ketik BANTUAN untuk daftar perintah.\n")

    # ── Loop utama CLI ──────────────────────────────────────────────
    while True:
        try:
            raw = input("  >> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Keluar dari program. Sampai jumpa!\n")
            break

        if not raw:
            continue

        parts  = raw.split()
        perintah = parts[0].upper()
        args     = parts[1:]

        # ── BANTUAN ────────────────────────────────────────────────
        if perintah == 'BANTUAN':
            print(BANTUAN_TEXT)

        # ── CARI_MHS <nim> ─────────────────────────────────────────
        elif perintah == 'CARI_MHS':
            if len(args) < 1:
                print("  [ERROR] Penggunaan: CARI_MHS <nim>\n")
                continue
            cari_mahasiswa(bst, args[0])

        # ── INPUT_NILAI <nim> <kode> <sks> <grade> <semester> ──────
        elif perintah == 'INPUT_NILAI':
            if len(args) < 5:
                print("  [ERROR] Penggunaan: INPUT_NILAI <nim> <kode_mk> <sks> <grade> <semester>\n")
                continue
            nim, kode, grade = args[0], args[1], args[3]
            try:
                sks      = int(args[2])
                semester = int(args[4])
            except ValueError:
                print("  [ERROR] SKS dan semester harus berupa angka.\n")
                continue

            # Cari node BST mahasiswa — O(log n)
            node = bst.search(nim)
            if node is None:
                print(f"  [ERROR] Mahasiswa NIM '{nim}' tidak ditemukan.\n")
                continue

            # Gunakan kode sebagai nama MK juga (bisa dikembangkan)
            nama_mk = kode

            # Input nilai ke DLL — O(1) tambah + O(n) hitung_ipk
            berhasil = input_nilai(node, kode, nama_mk, sks, grade, semester)

            if berhasil:
                # Catat ke Stack undo — O(1)
                nilai_baru = node.transkripsi.tail.data
                catat_operasi(undo_stack, nim, nilai_baru)
                print(f"  [OK] Nilai {kode} ({grade}) untuk {nim} berhasil diinput.")
                print(f"  [Big-O] DLL insert tail O(1) | IPK dihitung ulang O(n) | Stack push O(1)")
                print(f"  IPK terbaru: {node.mhs.ipk:.2f}\n")

        # ── UNDO_NILAI <nim> ───────────────────────────────────────
        elif perintah == 'UNDO_NILAI':
            if len(args) < 1:
                print("  [ERROR] Penggunaan: UNDO_NILAI <nim>\n")
                continue
            # Undo berdasarkan NIM spesifik dari Stack — O(log n)
            # Cari operasi terakhir untuk NIM ini di stack
            nim_target = args[0]
            node = bst.search(nim_target)
            if node is None:
                print(f"  [ERROR] Mahasiswa NIM '{nim_target}' tidak ditemukan.\n")
                continue

            # Pop Stack dan hapus dari DLL — O(1) + O(log n)
            berhasil = undo_operasi(undo_stack, bst)
            if berhasil:
                print(f"  [Big-O] Stack pop O(1) | DLL hapus tail O(1) | IPK hitung ulang O(n)\n")

        # ── TRANSKRIPSI <nim> ──────────────────────────────────────
        elif perintah == 'TRANSKRIPSI':
            if len(args) < 1:
                print("  [ERROR] Penggunaan: TRANSKRIPSI <nim>\n")
                continue
            node = bst.search(args[0])
            if node is None:
                print(f"  [INFO] Mahasiswa NIM '{args[0]}' tidak ditemukan.\n")
                continue
            lihat_transkripsi(node)
            print(f"  [Big-O] DLL traversal O(n) di mana n = jumlah MK ditempuh\n")

        # ── IPK <nim> ──────────────────────────────────────────────
        elif perintah == 'IPK':
            if len(args) < 1:
                print("  [ERROR] Penggunaan: IPK <nim>\n")
                continue
            node = bst.search(args[0])
            if node is None:
                print(f"  [INFO] Mahasiswa NIM '{args[0]}' tidak ditemukan.\n")
                continue
            tampilkan_ipk(node)
            print(f"  [Big-O] BST search O(log n) | DLL hitung_ipk O(n)\n")

        # ── RANKING_IPK ────────────────────────────────────────────
        elif perintah == 'RANKING_IPK':
            tampilkan_ranking(bst)

        # ── FILTER_IPK <min> <max> ─────────────────────────────────
        elif perintah == 'FILTER_IPK':
            if len(args) < 2:
                print("  [ERROR] Penggunaan: FILTER_IPK <min> <max>\n")
                continue
            try:
                low  = float(args[0])
                high = float(args[1])
            except ValueError:
                print("  [ERROR] Nilai IPK harus berupa angka desimal (contoh: 3.0 4.0)\n")
                continue
            filter_range_ipk(bst, low, high)
            print(f"  [Big-O] Inorder traversal O(n) + filter O(n) = O(n)\n")

        # ── PRASYARAT_CEK <nim> <kode_mk> ─────────────────────────
        elif perintah == 'PRASYARAT_CEK':
            if len(args) < 2:
                print("  [ERROR] Penggunaan: PRASYARAT_CEK <nim> <kode_mk>\n")
                continue
            node = bst.search(args[0])
            if node is None:
                print(f"  [INFO] Mahasiswa NIM '{args[0]}' tidak ditemukan.\n")
                continue
            cek_prasyarat(graph, node, args[1])
            print(f"  [Big-O] O(deg + m) di mana deg = jumlah prasyarat, m = MK di transkrip\n")

        # ── URUTAN_MATKUL ──────────────────────────────────────────
        elif perintah == 'URUTAN_MATKUL':
            urutan_matkul(graph)

        # ── DAFTAR_MHS ─────────────────────────────────────────────
        elif perintah == 'DAFTAR_MHS':
            daftar_mahasiswa(bst)
            print(f"  [Big-O] BST inorder O(n)\n")

        # ── KELUAR ─────────────────────────────────────────────────
        elif perintah == 'KELUAR':
            print("\n  Terima kasih telah menggunakan Academic Performance Tracker!")
            print("  Sampai jumpa!\n")
            break

        else:
            print(f"  [ERROR] Perintah '{perintah}' tidak dikenal. Ketik BANTUAN untuk daftar perintah.\n")


# ================================================================== #
#  ENTRY POINT                                                         #
# ================================================================== #

if __name__ == '__main__':
    main()