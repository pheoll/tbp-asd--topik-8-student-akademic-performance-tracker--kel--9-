"""
Modul 4 - Graph DAG Prasyarat Matakuliah
==========================================
Bertanggung jawab atas manajemen kurikulum dan validasi prasyarat matakuliah
menggunakan Directed Acyclic Graph (DAG).
 
Data kurikulum Topik 8:
    - 40 matakuliah dengan kode ELT/INF/MES/SIP/KIM
    - 55 relasi prasyarat (edge DAG)
    - Topological sort menggunakan Kahn's Algorithm
 
Fungsi utama:
    - inisialisasi_kurikulum : daftarkan 40 MK dan 55 prasyarat ke DAG (O(V+E))
    - urutan_matkul          : topological sort DAG (O(V+E))
    - cek_prasyarat          : cek apakah prasyarat MK sudah dipenuhi mahasiswa (O(deg))
"""
 
import sys
import os
 
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'data_structures'))
 
from graph import GraphPrereq
 
 
# ------------------------------------------------------------------ #
#  DATA KURIKULUM (40 MK, 55 RELASI PRASYARAT)                         #
# ------------------------------------------------------------------ #
 
# Daftar 40 matakuliah: (kode, nama)
# Pembagian: ELT=10, INF=10, MES=8, SIP=6, KIM=6
KURIKULUM = [
    # --- Teknik Elektro ---
    ('ELT101', 'Matematika Teknik I'),
    ('ELT102', 'Matematika Teknik II'),
    ('ELT103', 'Fisika Dasar'),
    ('ELT104', 'Rangkaian Listrik I'),
    ('ELT105', 'Rangkaian Listrik II'),
    ('ELT106', 'Elektronika Analog'),
    ('ELT107', 'Elektronika Digital'),
    ('ELT108', 'Sistem Kendali'),
    ('ELT109', 'Mesin Listrik'),
    ('ELT110', 'Tugas Akhir Elektro'),
 
    # --- Informatika ---
    ('INF101', 'Dasar Pemrograman'),
    ('INF102', 'Algoritma dan Struktur Data'),
    ('INF103', 'Basis Data'),
    ('INF104', 'Pemrograman Berorientasi Objek'),
    ('INF105', 'Jaringan Komputer'),
    ('INF106', 'Sistem Operasi'),
    ('INF107', 'Kecerdasan Buatan'),
    ('INF108', 'Pemrograman Web'),
    ('INF109', 'Keamanan Sistem'),
    ('INF110', 'Tugas Akhir Informatika'),
 
    # --- Teknik Mesin ---
    ('MES101', 'Statika dan Mekanika'),
    ('MES102', 'Termodinamika'),
    ('MES103', 'Mekanika Fluida'),
    ('MES104', 'Material Teknik'),
    ('MES105', 'Proses Manufaktur'),
    ('MES106', 'Elemen Mesin'),
    ('MES107', 'Perpindahan Panas'),
    ('MES108', 'Tugas Akhir Mesin'),
 
    # --- Teknik Sipil ---
    ('SIP101', 'Mekanika Tanah'),
    ('SIP102', 'Struktur Baja'),
    ('SIP103', 'Struktur Beton'),
    ('SIP104', 'Hidrologi'),
    ('SIP105', 'Rekayasa Jalan'),
    ('SIP106', 'Tugas Akhir Sipil'),
 
    # --- Teknik Kimia ---
    ('KIM101', 'Kimia Dasar'),
    ('KIM102', 'Termodinamika Kimia'),
    ('KIM103', 'Perpindahan Massa'),
    ('KIM104', 'Reaktor Kimia'),
    ('KIM105', 'Operasi Teknik Kimia'),
    ('KIM106', 'Tugas Akhir Kimia'),
]
 
# 55 relasi prasyarat: (kode_mk, kode_prasyarat)
# Format: MK kiri membutuhkan MK kanan sebagai prasyarat
PRASYARAT = [
    # Elektro
    ('ELT102', 'ELT101'),
    ('ELT104', 'ELT101'),
    ('ELT104', 'ELT103'),
    ('ELT105', 'ELT104'),
    ('ELT106', 'ELT103'),
    ('ELT106', 'ELT104'),
    ('ELT107', 'ELT104'),
    ('ELT108', 'ELT105'),
    ('ELT108', 'ELT106'),
    ('ELT109', 'ELT105'),
    ('ELT110', 'ELT108'),
    ('ELT110', 'ELT109'),
 
    # Informatika
    ('INF102', 'INF101'),
    ('INF103', 'INF101'),
    ('INF104', 'INF101'),
    ('INF105', 'INF103'),
    ('INF106', 'INF104'),
    ('INF107', 'INF102'),
    ('INF107', 'INF104'),
    ('INF108', 'INF103'),
    ('INF108', 'INF104'),
    ('INF109', 'INF105'),
    ('INF109', 'INF106'),
    ('INF110', 'INF107'),
    ('INF110', 'INF108'),
    ('INF110', 'INF109'),
 
    # Mesin
    ('MES102', 'MES101'),
    ('MES103', 'MES101'),
    ('MES103', 'MES102'),
    ('MES104', 'MES101'),
    ('MES105', 'MES104'),
    ('MES106', 'MES101'),
    ('MES106', 'MES105'),
    ('MES107', 'MES102'),
    ('MES107', 'MES103'),
    ('MES108', 'MES106'),
    ('MES108', 'MES107'),
 
    # Sipil
    ('SIP102', 'SIP101'),
    ('SIP103', 'SIP101'),
    ('SIP104', 'SIP101'),
    ('SIP105', 'SIP103'),
    ('SIP105', 'SIP104'),
    ('SIP106', 'SIP102'),
    ('SIP106', 'SIP105'),
 
    # Kimia
    ('KIM102', 'KIM101'),
    ('KIM103', 'KIM101'),
    ('KIM103', 'KIM102'),
    ('KIM104', 'KIM102'),
    ('KIM104', 'KIM103'),
    ('KIM105', 'KIM103'),
    ('KIM105', 'KIM104'),
    ('KIM106', 'KIM104'),
    ('KIM106', 'KIM105'),
]
 
 
# ------------------------------------------------------------------ #
#  INISIALISASI KURIKULUM                                              #
# ------------------------------------------------------------------ #
 
def inisialisasi_kurikulum() -> GraphPrereq:
    """
    Daftarkan semua matakuliah dan relasi prasyarat ke dalam DAG.
 
    Big-O Waktu : O(V + E) — V kali tambah_matkul O(1) + E kali tambah_prasyarat O(1)
                  V=40 matakuliah, E=55 relasi prasyarat
    Big-O Ruang : O(V + E) — adjacency list menyimpan semua node dan edge
 
    Return:
        GraphPrereq yang sudah terisi lengkap
    """
    graph = GraphPrereq()
 
    # Daftarkan semua matakuliah — O(V)
    for kode, nama in KURIKULUM:
        graph.tambah_matkul(kode, nama)
 
    # Daftarkan semua relasi prasyarat — O(E)
    for kode_mk, kode_prasyarat in PRASYARAT:
        graph.tambah_prasyarat(kode_mk, kode_prasyarat)
 
    return graph
 
 
# ------------------------------------------------------------------ #
#  URUTAN MATAKULIAH (TOPOLOGICAL SORT)                                #
# ------------------------------------------------------------------ #
 
def urutan_matkul(graph: GraphPrereq) -> None:
    """
    Tampilkan urutan pengambilan matakuliah yang valid menggunakan
    Kahn's Algorithm (topological sort BFS-based).
 
    Jika terdeteksi siklus (relasi prasyarat melingkar), tampilkan peringatan.
    Dalam kurikulum normal, siklus tidak mungkin terjadi (DAG valid).
 
    Big-O Waktu : O(V + E) — Kahn's Algorithm memproses tiap vertex dan edge sekali
    Big-O Ruang : O(V + E) — in_degree dict + reverse_adj + queue + hasil
 
    Args:
        graph: GraphPrereq yang sudah diinisialisasi
    """
    # Topological sort Kahn's Algorithm — O(V+E)
    urutan = graph.topological_sort()
 
    print(f"\n  {'='*65}")
    print(f"  URUTAN PENGAMBILAN MATAKULIAH (Topological Sort)")
    print(f"  Algoritma: Kahn's Algorithm | Big-O: O(V+E), V=40, E=55")
    print(f"  {'='*65}")
 
    if not urutan:
        print("  [ERROR] Terdeteksi SIKLUS dalam relasi prasyarat!")
        print("  Topological sort tidak valid — periksa data kurikulum.")
        print(f"  {'='*65}\n")
        return
 
    print(f"  Total MK: {len(urutan)}\n")
    print(f"  {'No':>4} {'Kode':<10} {'Nama MK':<35} {'Prasyarat'}")
    print(f"  {'-'*65}")
 
    for i, kode in enumerate(urutan, 1):
        nama = graph.matkul.get(kode, kode)
        prasyarat_list = graph.adj.get(kode, [])
        prasyarat_str = ', '.join(prasyarat_list) if prasyarat_list else '-'
        print(f"  {i:>4} {kode:<10} {nama:<35} {prasyarat_str}")
 
    print(f"  {'='*65}\n")
 
 
# ------------------------------------------------------------------ #
#  CEK PRASYARAT                                                       #
# ------------------------------------------------------------------ #
 
def cek_prasyarat(graph: GraphPrereq, bst_node, kode_mk: str) -> None:
    """
    Cek dan tampilkan apakah mahasiswa sudah memenuhi semua prasyarat
    untuk mengambil matakuliah tertentu.
 
    Syarat lulus prasyarat: grade >= C (nilai bobot >= 2.0).
 
    Big-O Waktu : O(deg + m) — deg = jumlah prasyarat kode_mk, m = jumlah MK di transkripsi
    Big-O Ruang : O(m) — dict nilai mahasiswa untuk lookup O(1) per prasyarat
 
    Args:
        graph    : GraphPrereq
        bst_node : BSTNodeMhs — node BST mahasiswa
        kode_mk  : kode matakuliah yang ingin diambil
    """
    from doubly_linked_list import GRADE_MAP
 
    mhs = bst_node.mhs
 
    if kode_mk not in graph.adj:
        print(f"\n  [INFO] MK '{kode_mk}' tidak terdaftar dalam kurikulum.\n")
        return
 
    nama_mk = graph.matkul.get(kode_mk, kode_mk)
    prasyarat_list = graph.adj.get(kode_mk, [])
 
    print(f"\n  {'='*60}")
    print(f"  CEK PRASYARAT: {kode_mk} – {nama_mk}")
    print(f"  Mahasiswa    : {mhs.nama} ({mhs.nim})")
    print(f"  {'='*60}")
 
    if not prasyarat_list:
        print(f"  [INFO] MK ini tidak memiliki prasyarat. Bisa langsung diambil.")
        print(f"  {'='*60}\n")
        return
 
    # Buat dict nilai mahasiswa untuk lookup O(1) — O(m)
    semua_nilai = bst_node.transkripsi.semua_nilai()
    nilai_dict = {n.kode_mk: n for n in semua_nilai}
 
    print(f"  {'Kode Prasyarat':<15} {'Nama MK':<30} {'Grade':<7} {'Status'}")
    print(f"  {'-'*60}")
 
    semua_terpenuhi = True
 
    # Cek setiap prasyarat — O(deg)
    for p in prasyarat_list:
        nama_p = graph.matkul.get(p, p)
        if p not in nilai_dict:
            status = '✗ Belum diambil'
            grade_str = '-'
            semua_terpenuhi = False
        else:
            grade = nilai_dict[p].grade
            grade_val = GRADE_MAP.get(grade, 0.0)
            grade_str = grade
            if grade_val >= 2.0:
                status = '✓ Lulus'
            else:
                status = f'✗ Tidak lulus ({grade})'
                semua_terpenuhi = False
 
        print(f"  {p:<15} {nama_p:<30} {grade_str:<7} {status}")
 
    print(f"  {'─'*60}")
    if semua_terpenuhi:
        print(f"  HASIL: ✓ Semua prasyarat terpenuhi. {kode_mk} BOLEH diambil.")
    else:
        print(f"  HASIL: ✗ Ada prasyarat yang belum terpenuhi. {kode_mk} BELUM bisa diambil.")
    print(f"  {'='*60}\n")