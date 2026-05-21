"""
Modul 3 - Stack Undo Input Nilai
==================================
Bertanggung jawab atas manajemen riwayat operasi INPUT_NILAI menggunakan Stack.
 
Setiap kali INPUT_NILAI dijalankan, operasi dicatat ke dalam Stack global.
Ketika UNDO_NILAI dipanggil:
    1. Pop dari Stack -> dapatkan operasi terakhir (NIM mahasiswa yang diinput)
    2. Panggil hapus_nilai_terakhir di DLL transkripsi mahasiswa tersebut
    3. Update IPK mahasiswa
 
Prinsip LIFO memastikan UNDO selalu membatalkan operasi yang paling terakhir
dilakukan, terlepas dari mahasiswa mana yang diinput terakhir.
 
Fungsi utama:
    - catat_operasi   : push operasi INPUT_NILAI ke Stack (O(1))
    - undo_operasi    : pop Stack + hapus dari DLL + update IPK (O(n))
    - lihat_riwayat   : tampilkan isi Stack tanpa mengubah (O(n) traversal)
"""
 
import sys
import os
 
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'data_structures'))
 
from stack import Stack
from doubly_linked_list import GRADE_MAP
 
 
# ------------------------------------------------------------------ #
#  CATAT OPERASI INPUT NILAI KE STACK                                  #
# ------------------------------------------------------------------ #
 
def catat_operasi(undo_stack: Stack, nim: str, nilai) -> None:
    """
    Push informasi operasi INPUT_NILAI ke Stack global.
    Dipanggil setiap kali modul_1.input_nilai berhasil dieksekusi.
 
    Struktur data yang di-push (dict):
        {
            'nim'   : str,          # NIM mahasiswa
            'nilai' : NilaiMatkul   # objek nilai yang baru saja diinput
        }
 
    Big-O Waktu : O(1) — Stack.push() insert di depan linked list
    Big-O Ruang : O(1) — 1 node baru di Stack
 
    Args:
        undo_stack : Stack global riwayat operasi
        nim        : NIM mahasiswa yang baru diinput nilainya
        nilai      : objek NilaiMatkul yang baru ditambahkan
    """
    operasi = {
        'nim'  : nim,
        'nilai': nilai
    }
    # Push ke Stack — O(1)
    undo_stack.push(operasi)
 
 
# ------------------------------------------------------------------ #
#  UNDO OPERASI TERAKHIR                                               #
# ------------------------------------------------------------------ #
 
def undo_operasi(undo_stack: Stack, bst) -> bool:
    """
    Batalkan operasi INPUT_NILAI terakhir yang tersimpan di Stack.
 
    Langkah:
        1. Pop Stack -> dapatkan dict operasi terakhir (O(1))
        2. Cari node BST mahasiswa yang bersangkutan (O(log n))
        3. Hapus nilai terakhir dari DLL transkripsinya (O(1))
        4. Hitung ulang IPK (O(m)) di mana m = jumlah MK mahasiswa
 
    Big-O Waktu : O(log n + m) — search BST O(log n) + hitung_ipk O(m)
    Big-O Ruang : O(1)
 
    Args:
        undo_stack : Stack global riwayat operasi
        bst        : BSTMahasiswa untuk mencari node mahasiswa
 
    Return:
        True jika undo berhasil, False jika Stack kosong
    """
    # Pop Stack — O(1)
    operasi = undo_stack.pop()
 
    if operasi is None:
        print("\n  [INFO] Tidak ada operasi yang bisa di-undo. Stack kosong.\n")
        return False
 
    nim    = operasi['nim']
    nilai  = operasi['nilai']
 
    # Cari node BST mahasiswa — O(log n)
    node = bst.search(nim)
 
    if node is None:
        print(f"\n  [ERROR] Mahasiswa NIM '{nim}' tidak ditemukan di BST.\n")
        return False
 
    # Hapus nilai terakhir dari DLL — O(1)
    dihapus = node.transkripsi.hapus_terakhir()
 
    if dihapus is None:
        print(f"\n  [INFO] Transkripsi {nim} sudah kosong, tidak ada yang bisa dihapus.\n")
        return False
 
    # Hitung ulang IPK setelah undo — O(m)
    node.mhs.ipk = node.transkripsi.hitung_ipk()
 
    print(f"\n  [UNDO] Berhasil membatalkan input nilai:")
    print(f"         NIM    : {nim} ({node.mhs.nama})")
    print(f"         MK     : {dihapus.kode_mk} – {dihapus.nama_mk}")
    print(f"         Grade  : {dihapus.grade} | SKS: {dihapus.sks} | Sem: {dihapus.semester}")
    print(f"         IPK baru: {node.mhs.ipk:.2f}\n")
 
    return True
 
 
# ------------------------------------------------------------------ #
#  LIHAT RIWAYAT STACK (TANPA MENGUBAH ISI)                            #
# ------------------------------------------------------------------ #
 
def lihat_riwayat(undo_stack: Stack) -> None:
    """
    Tampilkan seluruh isi Stack riwayat operasi dari top ke bottom
    tanpa mengubah isi Stack (read-only traversal).
 
    Big-O Waktu : O(k) — k = jumlah operasi dalam Stack
    Big-O Ruang : O(1) — tidak ada alokasi tambahan, traversal via pointer
 
    Args:
        undo_stack: Stack global riwayat operasi
    """
    if undo_stack.is_empty():
        print("\n  [INFO] Stack riwayat kosong. Belum ada operasi INPUT_NILAI.\n")
        return
 
    print(f"\n  {'='*60}")
    print(f"  RIWAYAT OPERASI INPUT NILAI (Top → Bottom)")
    print(f"  Total operasi dalam stack: {len(undo_stack)}")
    print(f"  {'='*60}")
    print(f"  {'No':>4} {'NIM':<14} {'Kode MK':<10} {'Grade':>6} {'SKS':>4} {'Sem':>4}")
    print(f"  {'-'*60}")
 
    # Traversal Stack dari top ke bottom via pointer next — O(k)
    current = undo_stack.top
    urutan = 1
    while current is not None:
        op = current.data
        nim   = op['nim']
        nilai = op['nilai']
        print(f"  {urutan:>4} {nim:<14} {nilai.kode_mk:<10} "
              f"{nilai.grade:>6} {nilai.sks:>4} {nilai.semester:>4}")
        current = current.next
        urutan += 1
 
    print(f"  {'='*60}")
    print(f"  [CATATAN] UNDO akan membatalkan baris no.1 (top stack)\n")