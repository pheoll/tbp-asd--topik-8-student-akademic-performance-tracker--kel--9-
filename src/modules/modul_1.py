"""
Modul 1 - Doubly Linked List Transkrip Nilai
============================================
Bertanggung jawab atas operasi manajemen nilai mahasiswa melalui DLL transkripsi
yang tersimpan di setiap node BST.
 
Fungsi utama:
    - input_nilai      : tambah nilai ke DLL transkripsi mahasiswa (O(1))
    - hapus_nilai      : hapus nilai terakhir dari DLL (undo, O(1))
    - lihat_transkripsi: tampilkan seluruh transkrip nilai (O(n))
    - filter_semester  : tampilkan nilai berdasarkan semester tertentu (O(n))
    - hitung_ipk       : hitung dan perbarui IPK mahasiswa dari DLL (O(n))
"""
 
from doubly_linked_list import NilaiMatkul, GRADE_MAP
 
 
# ------------------------------------------------------------------ #
#  INPUT NILAI                                                         #
# ------------------------------------------------------------------ #
 
def input_nilai(bst_node, kode_mk: str, nama_mk: str, sks: int,
                grade: str, semester: int) -> bool:
    """
    Tambahkan nilai matakuliah ke DLL transkripsi mahasiswa.
    Setelah insert, IPK mahasiswa otomatis dihitung ulang.
 
    Big-O Waktu : O(n) total — O(1) tambah_nilai + O(n) hitung_ipk
                  di mana n = jumlah matakuliah yang sudah ditempuh
    Big-O Ruang : O(1) — hanya 1 node DLL baru
 
    Args:
        bst_node  : BSTNodeMhs — node BST mahasiswa yang bersangkutan
        kode_mk   : kode matakuliah (contoh: 'ELT101')
        nama_mk   : nama lengkap matakuliah
        sks       : jumlah SKS matakuliah
        grade     : grade yang diperoleh (A, A-, B+, B, B-, C+, C, D, E)
        semester  : semester pengambilan (1–8)
 
    Return:
        True jika berhasil, False jika grade tidak valid
    """
    # Validasi grade
    if grade not in GRADE_MAP:
        print(f"[ERROR] Grade '{grade}' tidak valid. "
              f"Pilihan: {', '.join(GRADE_MAP.keys())}")
        return False
 
    # Validasi semester
    if not (1 <= semester <= 8):
        print(f"[ERROR] Semester '{semester}' tidak valid. Harus antara 1–8.")
        return False
 
    nilai = NilaiMatkul(
        kode_mk=kode_mk,
        nama_mk=nama_mk,
        sks=sks,
        grade=grade,
        semester=semester
    )
 
    # Sisip ke tail DLL — O(1)
    bst_node.transkripsi.tambah_nilai(nilai)
 
    # Hitung ulang IPK dari DLL — O(n)
    bst_node.mhs.ipk = bst_node.transkripsi.hitung_ipk()
 
    return True
 
 
# ------------------------------------------------------------------ #
#  HAPUS NILAI TERAKHIR (UNDO)                                         #
# ------------------------------------------------------------------ #
 
def hapus_nilai_terakhir(bst_node):
    """
    Hapus nilai terakhir dari DLL transkripsi mahasiswa (operasi undo).
    Setelah hapus, IPK mahasiswa otomatis dihitung ulang.
 
    Big-O Waktu : O(n) total — O(1) hapus_terakhir + O(n) hitung_ipk
    Big-O Ruang : O(1)
 
    Args:
        bst_node: BSTNodeMhs — node BST mahasiswa yang bersangkutan
 
    Return:
        NilaiMatkul yang dihapus, atau None jika transkripsi kosong
    """
    # Hapus tail DLL — O(1)
    dihapus = bst_node.transkripsi.hapus_terakhir()
 
    if dihapus is None:
        print(f"[INFO] Transkripsi {bst_node.mhs.nim} kosong, tidak ada yang bisa di-undo.")
        return None
 
    # Hitung ulang IPK setelah undo — O(n)
    bst_node.mhs.ipk = bst_node.transkripsi.hitung_ipk()
 
    return dihapus
 
 
# ------------------------------------------------------------------ #
#  LIHAT TRANSKRIPSI LENGKAP                                           #
# ------------------------------------------------------------------ #
 
def lihat_transkripsi(bst_node) -> None:
    """
    Tampilkan seluruh transkrip nilai mahasiswa dari DLL (traversal maju).
 
    Big-O Waktu : O(n) — traversal semua node DLL
    Big-O Ruang : O(n) — list semua nilai dari semua_nilai()
 
    Args:
        bst_node: BSTNodeMhs — node BST mahasiswa yang bersangkutan
    """
    mhs = bst_node.mhs
    semua = bst_node.transkripsi.semua_nilai()
 
    print(f"\n{'='*60}")
    print(f"  TRANSKRIP NILAI - {mhs.nama} ({mhs.nim})")
    print(f"  Prodi: {mhs.prodi} | Angkatan: {mhs.angkatan}")
    print(f"{'='*60}")
 
    if not semua:
        print("  [INFO] Belum ada nilai yang diinput.")
        print(f"{'='*60}\n")
        return
 
    # Kelompokkan per semester untuk tampilan yang rapi
    # O(n) traversal sekali, grouping menggunakan dict
    per_semester = {}
    for nilai in semua:
        per_semester.setdefault(nilai.semester, []).append(nilai)
 
    total_bobot = 0.0
    total_sks = 0
 
    for sem in sorted(per_semester.keys()):
        print(f"\n  Semester {sem}:")
        print(f"  {'Kode':<10} {'Nama MK':<30} {'SKS':>4} {'Grade':>6} {'Bobot':>7}")
        print(f"  {'-'*60}")
        for n in per_semester[sem]:
            bobot = GRADE_MAP.get(n.grade, 0.0) * n.sks
            total_bobot += bobot
            total_sks += n.sks
            print(f"  {n.kode_mk:<10} {n.nama_mk:<30} {n.sks:>4} {n.grade:>6} {bobot:>7.2f}")
 
    ips_per_sem = {}
    for sem, nilai_list in per_semester.items():
        b = sum(GRADE_MAP.get(n.grade, 0.0) * n.sks for n in nilai_list)
        s = sum(n.sks for n in nilai_list)
        ips_per_sem[sem] = b / s if s > 0 else 0.0
 
    print(f"\n  {'─'*60}")
    print(f"  IPS per Semester:")
    for sem in sorted(ips_per_sem.keys()):
        print(f"    Semester {sem}: {ips_per_sem[sem]:.2f}")
 
    ipk = total_bobot / total_sks if total_sks > 0 else 0.0
    print(f"\n  Total SKS Ditempuh : {total_sks}")
    print(f"  IPK Kumulatif      : {ipk:.2f}")
    print(f"{'='*60}\n")
 
 
# ------------------------------------------------------------------ #
#  FILTER SEMESTER                                                     #
# ------------------------------------------------------------------ #
 
def filter_semester(bst_node, semester: int) -> None:
    """
    Tampilkan nilai mahasiswa untuk semester tertentu (traversal maju DLL).
 
    Big-O Waktu : O(n) — semester_ke() menelusuri semua node DLL
    Big-O Ruang : O(k) — k = jumlah nilai pada semester tersebut
 
    Args:
        bst_node : BSTNodeMhs
        semester : nomor semester yang ingin ditampilkan (1–8)
    """
    mhs = bst_node.mhs
    # Traversal DLL filter by semester — O(n)
    nilai_list = bst_node.transkripsi.semester_ke(semester)
 
    print(f"\n  Nilai Semester {semester} - {mhs.nama} ({mhs.nim}):")
    if not nilai_list:
        print(f"  [INFO] Tidak ada nilai untuk semester {semester}.")
        return
 
    print(f"  {'Kode':<10} {'Nama MK':<30} {'SKS':>4} {'Grade':>6}")
    print(f"  {'-'*55}")
    total_sks = 0
    total_bobot = 0.0
    for n in nilai_list:
        bobot = GRADE_MAP.get(n.grade, 0.0) * n.sks
        total_bobot += bobot
        total_sks += n.sks
        print(f"  {n.kode_mk:<10} {n.nama_mk:<30} {n.sks:>4} {n.grade:>6}")
 
    ips = total_bobot / total_sks if total_sks > 0 else 0.0
    print(f"  {'─'*55}")
    print(f"  IPS Semester {semester}: {ips:.2f} | SKS: {total_sks}\n")
 
 
# ------------------------------------------------------------------ #
#  TAMPILKAN IPK                                                       #
# ------------------------------------------------------------------ #
 
def tampilkan_ipk(bst_node) -> float:
    """
    Hitung ulang dan tampilkan IPK mahasiswa dari DLL transkripsi.
 
    Big-O Waktu : O(n) — hitung_ipk() traversal semua node DLL
    Big-O Ruang : O(1)
 
    Args:
        bst_node: BSTNodeMhs
 
    Return:
        float IPK terkini
    """
    # Hitung ulang dari DLL untuk memastikan akurasi — O(n)
    ipk = bst_node.transkripsi.hitung_ipk()
    bst_node.mhs.ipk = ipk
 
    mhs = bst_node.mhs
    print(f"\n  IPK {mhs.nama} ({mhs.nim}): {ipk:.2f}"
          f"  | Total MK: {len(bst_node.transkripsi)}\n")
    return ipk
 