"""
TOPIK 8 - Student Academic Performance Tracker
Domain: Sistem Monitoring Akademik Mahasiswa
Struktur Data: BST, Doubly Linked List, Stack, Graph (DAG)
"""
 
import numpy as np
import time
import random
 
np.random.seed(31)
random.seed(31)
 
# ============================================================
# MODUL 1: DOUBLY LINKED LIST - Transkrip Nilai
# ============================================================
 
class NilaiNode:
    def _init_(self, kode_mk, nama_mk, semester, nilai_huruf, sks):
        self.kode_mk = kode_mk
        self.nama_mk = nama_mk
        self.semester = semester
        self.nilai_huruf = nilai_huruf
        self.sks = sks
        self.prev = None
        self.next = None
 
class DoublyLinkedListTranskrip:
    GRADE_POINT = {
        'A': 4.0, 'A-': 3.7,
        'B+': 3.3, 'B': 3.0, 'B-': 2.7,
        'C+': 2.3, 'C': 2.0,
        'D': 1.0, 'E': 0.0
    }
 
    def _init_(self):
        self.head = None
        self.tail = None
        self.size = 0
 
    def tambah_nilai(self, kode_mk, nama_mk, semester, nilai_huruf, sks):
        """Insert tail O(1)"""
        node = NilaiNode(kode_mk, nama_mk, semester, nilai_huruf, sks)
        if self.tail is None:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self.size += 1
 
    def hapus_terakhir(self):
        """Remove tail O(1) - undo input nilai"""
        if self.tail is None:
            return None
        removed = self.tail
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
        self.size -= 1
        return removed
 
    def filter_semester(self, k):
        """Traverse forward O(n)"""
        result = []
        curr = self.head
        while curr:
            if curr.semester == k:
                result.append(curr)
            curr = curr.next
        return result
 
    def hitung_ipk(self):
        """Traverse semua node O(n)"""
        total_bobot = 0.0
        total_sks = 0
        curr = self.head
        while curr:
            poin = self.GRADE_POINT.get(curr.nilai_huruf, 0.0)
            total_bobot += poin * curr.sks
            total_sks += curr.sks
            curr = curr.next
        return round(total_bobot / total_sks, 2) if total_sks > 0 else 0.0
 
    def hitung_ips(self, semester):
        """Hitung IPS untuk semester tertentu"""
        total_bobot = 0.0
        total_sks = 0
        for node in self.filter_semester(semester):
            poin = self.GRADE_POINT.get(node.nilai_huruf, 0.0)
            total_bobot += poin * node.sks
            total_sks += node.sks
        return round(total_bobot / total_sks, 2) if total_sks > 0 else 0.0
 
    def tampilkan_transkrip(self):
        """Tampilkan semua nilai"""
        if not self.head:
            print("  [Transkrip kosong]")
            return
        curr = self.head
        print(f"  {'Kode':<8} {'Nama MK':<30} {'Sem':<5} {'Nilai':<6} {'SKS'}")
        print("  " + "-"*60)
        while curr:
            print(f"  {curr.kode_mk:<8} {curr.nama_mk:<30} {curr.semester:<5} {curr.nilai_huruf:<6} {curr.sks}")
            curr = curr.next
 
 
# ============================================================
# MODUL 2: BST - Data Mahasiswa
# ============================================================
 
class MahasiswaNode:
    def _init_(self, nim, nama, prodi):
        self.nim = nim
        self.nama = nama
        self.prodi = prodi
        self.transkrip = DoublyLinkedListTranskrip()
        self.left = None
        self.right = None
 
class BSTMahasiswa:
    def _init_(self):
        self.root = None
        self.size = 0
 
    def insert(self, nim, nama, prodi):
        """Insert O(log n) average"""
        node = MahasiswaNode(nim, nama, prodi)
        if self.root is None:
            self.root = node
        else:
            self._insert_rec(self.root, node)
        self.size += 1
        return node
 
    def _insert_rec(self, curr, node):
        if node.nim < curr.nim:
            if curr.left is None:
                curr.left = node
            else:
                self._insert_rec(curr.left, node)
        else:
            if curr.right is None:
                curr.right = node
            else:
                self._insert_rec(curr.right, node)
 
    def search(self, nim):
        """Search O(log n) average"""
        return self._search_rec(self.root, nim)
 
    def _search_rec(self, curr, nim):
        if curr is None or curr.nim == nim:
            return curr
        if nim < curr.nim:
            return self._search_rec(curr.left, nim)
        return self._search_rec(curr.right, nim)
 
    def inorder(self):
        """Inorder traversal - sorted by NIM"""
        result = []
        self._inorder_rec(self.root, result)
        return result
 
    def _inorder_rec(self, curr, result):
        if curr:
            self._inorder_rec(curr.left, result)
            result.append(curr)
            self._inorder_rec(curr.right, result)
 
    def range_search(self, nim_low, nim_high):
        """Cari mahasiswa dalam range NIM"""
        result = []
        self._range_rec(self.root, nim_low, nim_high, result)
        return result
 
    def _range_rec(self, curr, low, high, result):
        if curr is None:
            return
        if low <= curr.nim <= high:
            result.append(curr)
        if curr.nim > low:
            self._range_rec(curr.left, low, high, result)
        if curr.nim < high:
            self._range_rec(curr.right, low, high, result)
 
 
# ============================================================
# MODUL 3: STACK - Riwayat Operasi (Undo)
# ============================================================
 
class StackNode:
    def _init_(self, data):
        self.data = data
        self.next = None
 
class Stack:
    def _init_(self, max_size=100):
        self.top = None
        self.size = 0
        self.max_size = max_size
 
    def push(self, data):
        """Push O(1)"""
        if self.size >= self.max_size:
            return False
        node = StackNode(data)
        node.next = self.top
        self.top = node
        self.size += 1
        return True
 
    def pop(self):
        """Pop O(1)"""
        if self.is_empty():
            return None
        data = self.top.data
        self.top = self.top.next
        self.size -= 1
        return data
 
    def peek(self):
        return self.top.data if self.top else None
 
    def is_empty(self):
        return self.size == 0
 
    def tampilkan(self):
        curr = self.top
        items = []
        while curr:
            items.append(str(curr.data))
            curr = curr.next
        print("  Stack (top→bottom):", " → ".join(items) if items else "[kosong]")
 
 
# ============================================================
# MODUL 4: GRAPH DAG - Prasyarat Matakuliah
# ============================================================
 
class GraphDAG:
    def _init_(self):
        self.adjacency = {}   # kode_mk -> list of kode_mk (prasyarat ke)
        self.prerequisites = {}  # kode_mk -> list prasyarat yang dibutuhkan
        self.mk_info = {}     # kode_mk -> (nama, sks, semester)
 
    def tambah_mk(self, kode, nama, sks, semester_min):
        """Tambah matakuliah ke graph"""
        if kode not in self.adjacency:
            self.adjacency[kode] = []
        if kode not in self.prerequisites:
            self.prerequisites[kode] = []
        self.mk_info[kode] = (nama, sks, semester_min)
 
    def tambah_prasyarat(self, mk_prasyarat, mk_tujuan):
        """Tambah edge: mk_prasyarat -> mk_tujuan O(1)"""
        if mk_prasyarat not in self.adjacency:
            self.adjacency[mk_prasyarat] = []
        if mk_tujuan not in self.prerequisites:
            self.prerequisites[mk_tujuan] = []
        self.adjacency[mk_prasyarat].append(mk_tujuan)
        self.prerequisites[mk_tujuan].append(mk_prasyarat)
 
    def validasi_pengambilan(self, mahasiswa_node, kode_mk):
        """Cek apakah semua prasyarat sudah lulus"""
        prasyarat_list = self.prerequisites.get(kode_mk, [])
        if not prasyarat_list:
            return True, []
        
        lulus = set()
        curr = mahasiswa_node.transkrip.head
        while curr:
            if curr.nilai_huruf not in ('D', 'E'):
                lulus.add(curr.kode_mk)
            curr = curr.next
        
        belum_lulus = [p for p in prasyarat_list if p not in lulus]
        return len(belum_lulus) == 0, belum_lulus
 
    def topological_sort(self):
        """Kahn's algorithm BFS O(V+E)"""
        in_degree = {mk: 0 for mk in self.adjacency}
        for mk in self.adjacency:
            for tujuan in self.adjacency[mk]:
                in_degree[tujuan] = in_degree.get(tujuan, 0) + 1
 
        queue = [mk for mk in in_degree if in_degree[mk] == 0]
        result = []
        while queue:
            node = queue.pop(0)
            result.append(node)
            for tujuan in self.adjacency.get(node, []):
                in_degree[tujuan] -= 1
                if in_degree[tujuan] == 0:
                    queue.append(tujuan)
        return result
 
    def get_jalur_belajar(self, kode_mk):
        """DFS untuk mendapatkan semua prasyarat rekursif"""
        visited = set()
        path = []
        self._dfs_prasyarat(kode_mk, visited, path)
        return path
 
    def _dfs_prasyarat(self, kode, visited, path):
        if kode in visited:
            return
        visited.add(kode)
        for prasyarat in self.prerequisites.get(kode, []):
            self._dfs_prasyarat(prasyarat, visited, path)
        path.append(kode)
 
    def tampilkan_graph(self):
        print("\n  === Struktur Prasyarat Matakuliah ===")
        for mk, tujuan_list in self.adjacency.items():
            nama = self.mk_info.get(mk, (mk,))[0]
            for t in tujuan_list:
                nama_t = self.mk_info.get(t, (t,))[0]
                print(f"  {mk} ({nama}) → {t} ({nama_t})")
 
 
# ============================================================
# DATA GENERATOR
# ============================================================
 
KODE_PRODI = ['ELT', 'INF', 'MES', 'SIP', 'KIM']
GRADE_LIST = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'D', 'E']
GRADE_WEIGHTS = [10, 15, 20, 20, 15, 10, 5, 3, 2]
 
NAMA_DEPAN = ['Andi', 'Budi', 'Citra', 'Dewi', 'Eko', 'Fajar', 'Gita', 'Hendra',
               'Indah', 'Joko', 'Kartika', 'Lina', 'Made', 'Nisa', 'Oscar',
               'Putri', 'Rizky', 'Sari', 'Tono', 'Udin', 'Vina', 'Wahyu',
               'Xena', 'Yoga', 'Zahra', 'Agus', 'Bayu', 'Candra', 'Dina', 'Evan']
NAMA_BELAKANG = ['Santoso', 'Wijaya', 'Kusuma', 'Hartono', 'Pratama', 'Suharto',
                  'Rahayu', 'Setiawan', 'Nugroho', 'Hidayat', 'Saputra', 'Lestari',
                  'Wibowo', 'Permata', 'Utama', 'Siregar', 'Nasution', 'Harahap',
                  'Tampubolon', 'Manurung', 'Simbolon', 'Purba', 'Sinaga', 'Ginting',
                  'Situmorang', 'Panjaitan', 'Lumban', 'Siahaan', 'Hutapea', 'Simanjuntak']
 
def generate_matakuliah():
    """Generate 40 matakuliah dengan struktur prodi"""
    mk_list = []
    # Matakuliah umum (semua prodi)
    mk_umum = [
        ('MTK101', 'Matematika Dasar', 3, 1),
        ('FIS101', 'Fisika Dasar', 3, 1),
        ('KIM101', 'Kimia Dasar', 2, 1),
        ('INF101', 'Pemrograman Dasar', 3, 1),
        ('ENG101', 'Bahasa Inggris Teknik', 2, 1),
        ('MTK201', 'Kalkulus', 3, 2),
        ('STA201', 'Statistika', 3, 2),
        ('INF201', 'Struktur Data', 3, 2),
        ('INF202', 'Algoritma', 3, 2),
        ('ENG201', 'Bahasa Inggris Lanjut', 2, 2),
    ]
    # Matakuliah prodi ELT
    mk_elt = [
        ('ELT301', 'Rangkaian Listrik', 3, 3),
        ('ELT302', 'Elektronika Dasar', 3, 3),
        ('ELT401', 'Sistem Kendali', 3, 4),
        ('ELT402', 'Elektronika Daya', 3, 4),
        ('ELT501', 'Sistem Tenaga', 3, 5),
        ('ELT502', 'Mesin Listrik', 3, 5),
        ('ELT601', 'PLC & Otomasi', 3, 6),
        ('ELT701', 'Proyek Akhir I', 4, 7),
    ]
    # Matakuliah prodi INF
    mk_inf = [
        ('INF301', 'Basis Data', 3, 3),
        ('INF302', 'Pemrograman OOP', 3, 3),
        ('INF401', 'Jaringan Komputer', 3, 4),
        ('INF402', 'Rekayasa Perangkat Lunak', 3, 4),
        ('INF501', 'Kecerdasan Buatan', 3, 5),
        ('INF502', 'Keamanan Sistem', 3, 5),
        ('INF601', 'Machine Learning', 3, 6),
        ('INF701', 'Skripsi I', 4, 7),
    ]
    # Matakuliah prodi MES
    mk_mes = [
        ('MES301', 'Mekanika Teknik', 3, 3),
        ('MES302', 'Termodinamika', 3, 3),
        ('MES401', 'Mekanika Fluida', 3, 4),
        ('MES402', 'Perpindahan Panas', 3, 4),
        ('MES501', 'Desain Mesin', 3, 5),
        ('MES502', 'Manufaktur', 3, 5),
        ('MES601', 'CAD/CAM', 3, 6),
        ('MES701', 'Tugas Akhir I', 4, 7),
    ]
    # Matakuliah prodi SIP & KIM (shared)
    mk_sipkim = [
        ('SIP301', 'Mekanika Tanah', 3, 3),
        ('SIP302', 'Beton Bertulang', 3, 3),
        ('KIM301', 'Kimia Organik', 3, 3),
        ('KIM302', 'Kimia Analitik', 3, 3),
        ('SIP401', 'Manajemen Konstruksi', 3, 4),
        ('KIM401', 'Kimia Industri', 3, 4),
    ]
    mk_list = mk_umum + mk_elt + mk_inf + mk_mes + mk_sipkim
    return mk_list[:40]
 
def generate_prasyarat(dag, mk_list):
    """Tambah relasi prasyarat antar matakuliah"""
    prasyarat_pairs = [
        ('MTK101', 'MTK201'), ('MTK101', 'STA201'), ('MTK101', 'FIS101'),
        ('FIS101', 'ELT301'), ('FIS101', 'MES301'), ('FIS101', 'MES302'),
        ('INF101', 'INF201'), ('INF101', 'INF202'), ('INF101', 'INF301'),
        ('INF201', 'INF301'), ('INF201', 'INF302'), ('INF201', 'INF401'),
        ('INF302', 'INF402'), ('INF302', 'INF501'), ('INF302', 'INF601'),
        ('INF501', 'INF601'), ('INF401', 'INF502'),
        ('ELT301', 'ELT302'), ('ELT302', 'ELT401'), ('ELT302', 'ELT402'),
        ('ELT401', 'ELT501'), ('ELT401', 'ELT601'), ('ELT501', 'ELT701'),
        ('MES301', 'MES401'), ('MES302', 'MES401'), ('MES302', 'MES402'),
        ('MES401', 'MES501'), ('MES501', 'MES601'), ('MES601', 'MES701'),
        ('KIM101', 'KIM301'), ('KIM301', 'KIM302'), ('KIM301', 'KIM401'),
        ('SIP301', 'SIP302'), ('SIP302', 'SIP401'), ('MTK201', 'SIP301'),
    ]
    mk_kode_set = {mk[0] for mk in mk_list}
    for p, t in prasyarat_pairs:
        if p in mk_kode_set and t in mk_kode_set:
            dag.tambah_prasyarat(p, t)
 
def generate_data():
    """Generate semua data sesuai spesifikasi"""
    bst = BSTMahasiswa()
    dag = GraphDAG()
    stack_ops = Stack(max_size=500)
 
    # Generate matakuliah
    mk_list = generate_matakuliah()
    for kode, nama, sks, sem in mk_list:
        dag.tambah_mk(kode, nama, sks, sem)
    generate_prasyarat(dag, mk_list)
 
    # Generate 60 mahasiswa
    nim_list = set()
    while len(nim_list) < 60:
        nim = f"21{random.randint(10000000, 99999999)}"
        nim_list.add(nim)
    nim_list = sorted(nim_list)
 
    for i, nim in enumerate(nim_list):
        nama = f"{random.choice(NAMA_DEPAN)} {random.choice(NAMA_BELAKANG)}"
        prodi = random.choice(KODE_PRODI)
        mhs = bst.insert(nim, nama, prodi)
 
        # Matakuliah umum (semester 1-2)
        mk_umum = [mk for mk in mk_list if mk[3] <= 2]
        # Matakuliah prodi
        mk_prodi = [mk for mk in mk_list if mk[0].startswith(prodi) or mk[3] <= 2]
 
        # Generate nilai 8 semester
        for sem in range(1, 9):
            mk_sem = [mk for mk in mk_prodi if mk[3] == sem]
            if not mk_sem:
                mk_sem = [mk for mk in mk_list if mk[3] == sem]
            for mk in mk_sem[:min(6, len(mk_sem))]:
                nilai = random.choices(GRADE_LIST, weights=GRADE_WEIGHTS)[0]
                mhs.transkrip.tambah_nilai(mk[0], mk[1], sem, nilai, mk[2])
                stack_ops.push(f"ADD|{nim}|{mk[0]}|{nilai}")
 
    return bst, dag, stack_ops, mk_list
 
 
# ============================================================
# EKSPERIMEN PERFORMA
# ============================================================
 
def eksperimen_performa(bst, dag):
    """Perbandingan runtime dengan 3 ukuran dataset"""
    print("\n" + "="*65)
    print("  EKSPERIMEN PERBANDINGAN PERFORMA")
    print("="*65)
 
    datasets = [10, 30, 60]
    semua_mahasiswa = bst.inorder()
 
    print(f"\n  {'Operasi':<30} {'n=10':>10} {'n=30':>10} {'n=60':>10}")
    print("  " + "-"*62)
 
    # Test BST Search
    times = []
    for n in datasets:
        subset = semua_mahasiswa[:n]
        t0 = time.perf_counter()
        for mhs in subset:
            bst.search(mhs.nim)
        t1 = time.perf_counter()
        times.append(f"{(t1-t0)*1000:.4f}ms")
    print(f"  {'BST Search (semua)':<30} {times[0]:>10} {times[1]:>10} {times[2]:>10}")
 
    # Test Hitung IPK
    times = []
    for n in datasets:
        subset = semua_mahasiswa[:n]
        t0 = time.perf_counter()
        for mhs in subset:
            mhs.transkrip.hitung_ipk()
        t1 = time.perf_counter()
        times.append(f"{(t1-t0)*1000:.4f}ms")
    print(f"  {'Hitung IPK (DLL traverse)':<30} {times[0]:>10} {times[1]:>10} {times[2]:>10}")
 
    # Test Filter Semester
    times = []
    for n in datasets:
        subset = semua_mahasiswa[:n]
        t0 = time.perf_counter()
        for mhs in subset:
            mhs.transkrip.filter_semester(3)
        t1 = time.perf_counter()
        times.append(f"{(t1-t0)*1000:.4f}ms")
    print(f"  {'Filter Semester DLL':<30} {times[0]:>10} {times[1]:>10} {times[2]:>10}")
 
    # Test Topological Sort
    times = []
    for n in datasets:
        t0 = time.perf_counter()
        for _ in range(n):
            dag.topological_sort()
        t1 = time.perf_counter()
        times.append(f"{(t1-t0)*1000:.4f}ms")
    print(f"  {'Topological Sort DAG':<30} {times[0]:>10} {times[1]:>10} {times[2]:>10}")
 
    # Test Inorder BST
    times = []
    for n in datasets:
        t0 = time.perf_counter()
        for _ in range(n):
            bst.inorder()
        t1 = time.perf_counter()
        times.append(f"{(t1-t0)*1000:.4f}ms")
    print(f"  {'BST Inorder Traversal':<30} {times[0]:>10} {times[1]:>10} {times[2]:>10}")
 
    print(f"\n  Keterangan: runtime akumulatif untuk n operasi/mahasiswa")
    print("  Big-O: BST Search O(log n), IPK O(n), Filter O(n), Topo O(V+E)")
 
 
# ============================================================
# ANALISIS LANJUTAN (5 Pertanyaan)
# ============================================================
 
def analisis_lanjutan(bst, dag):
    print("\n" + "="*65)
    print("  5 PERTANYAAN ANALISIS LANJUTAN")
    print("="*65)
 
    semua = bst.inorder()
 
    print("\n  1. Mahasiswa dengan IPK tertinggi dan terendah?")
    ipk_list = [(m.nim, m.nama, m.transkrip.hitung_ipk()) for m in semua]
    ipk_list.sort(key=lambda x: x[2])
    print(f"     Terendah : {ipk_list[0][1]} ({ipk_list[0][0]}) - IPK {ipk_list[0][2]}")
    print(f"     Tertinggi: {ipk_list[-1][1]} ({ipk_list[-1][0]}) - IPK {ipk_list[-1][2]}")
 
    print("\n  2. Trade-off: mengapa BST lebih efisien dari list untuk pencarian?")
    print("     BST: O(log n) search vs list O(n) linear scan.")
    print("     BST menggunakan properti BST untuk eliminasi setengah pohon")
    print("     setiap langkah. Untuk 60 mahasiswa: BST ~6 langkah, list ~30.")
    print("     Trade-off: BST butuh O(n) memori ekstra untuk pointer left/right.")
 
    print("\n  3. Mengapa DLL dipilih vs Array untuk transkrip?")
    print("     DLL: insert O(1) tail, delete O(1) tail (undo).")
    print("     Array: insert O(1) amortized, tapi delete butuh O(n) shift.")
    print("     DLL unggul untuk operasi undo berulang dan traversal dua arah.")
 
    print("\n  4. Apakah DAG bisa mendeteksi siklus prasyarat?")
    topo = dag.topological_sort()
    total_mk = len(dag.adjacency)
    if len(topo) == total_mk:
        print(f"     YA - Topological sort berhasil ({len(topo)} node).")
        print("     Jika ada siklus, Kahn's algo akan menghasilkan < total node.")
    else:
        print(f"     TERDETEKSI SIKLUS! Hanya {len(topo)}/{total_mk} node terurut.")
 
    print("\n  5. Kompleksitas validasi pengambilan matakuliah?")
    print("     validasi_pengambilan: O(P + T)")
    print("     P = jumlah prasyarat MK tersebut (edge dari prasyarat ke MK)")
    print("     T = jumlah nilai di transkrip mahasiswa (DLL traverse)")
    print("     Untuk kasus terburuk: O(40) MK transkrip + O(5) prasyarat = O(n)")
 
 
# ============================================================
# CLI MENU
# ============================================================
 
def menu_utama(bst, dag, stack_ops):
    while True:
        print("\n" + "="*65)
        print("  STUDENT ACADEMIC PERFORMANCE TRACKER - TOPIK 8")
        print("="*65)
        print("  [1] Cari Mahasiswa (BST Search)")
        print("  [2] Tampilkan Transkrip Nilai (DLL)")
        print("  [3] Tambah Nilai Baru")
        print("  [4] Undo Input Nilai Terakhir (Stack)")
        print("  [5] Hitung IPK & IPS per Semester")
        print("  [6] Filter Nilai per Semester")
        print("  [7] Validasi Pengambilan MK (DAG)")
        print("  [8] Topological Sort Matakuliah")
        print("  [9] Daftar Semua Mahasiswa (Inorder BST)")
        print("  [10] Eksperimen Performa")
        print("  [11] Analisis Lanjutan (5 Pertanyaan)")
        print("  [12] Tampilkan Riwayat Operasi (Stack)")
        print("  [0] Keluar")
        print("-"*65)
        pilihan = input("  Pilih menu: ").strip()
 
        if pilihan == '1':
            nim = input("  Masukkan NIM: ").strip()
            mhs = bst.search(nim)
            if mhs:
                print(f"\n  ✓ Ditemukan: {mhs.nama} | NIM: {mhs.nim} | Prodi: {mhs.prodi}")
                print(f"    IPK: {mhs.transkrip.hitung_ipk()} | Total MK: {mhs.transkrip.size}")
            else:
                print("  ✗ Mahasiswa tidak ditemukan.")
 
        elif pilihan == '2':
            nim = input("  Masukkan NIM: ").strip()
            mhs = bst.search(nim)
            if mhs:
                print(f"\n  Transkrip: {mhs.nama} ({mhs.nim})")
                mhs.transkrip.tampilkan_transkrip()
                print(f"\n  IPK Kumulatif: {mhs.transkrip.hitung_ipk()}")
            else:
                print("  ✗ Mahasiswa tidak ditemukan.")
 
        elif pilihan == '3':
            nim = input("  NIM Mahasiswa: ").strip()
            mhs = bst.search(nim)
            if not mhs:
                print("  ✗ Mahasiswa tidak ditemukan.")
                continue
            kode = input("  Kode MK: ").strip()
            nama_mk = input("  Nama MK: ").strip()
            try:
                sem = int(input("  Semester (1-8): ").strip())
                sks = int(input("  SKS: ").strip())
            except ValueError:
                print("  ✗ Input tidak valid.")
                continue
            nilai = input("  Nilai (A/A-/B+/B/B-/C+/C/D/E): ").strip()
            if nilai not in DoublyLinkedListTranskrip.GRADE_POINT:
                print("  ✗ Nilai tidak valid.")
                continue
            # Validasi prasyarat
            valid, belum = dag.validasi_pengambilan(mhs, kode)
            if not valid:
                print(f"  ⚠️ Prasyarat belum terpenuhi: {', '.join(belum)}")
                konfirm = input("  Tetap tambahkan? (y/n): ").strip().lower()
                if konfirm != 'y':
                    continue
            mhs.transkrip.tambah_nilai(kode, nama_mk, sem, nilai, sks)
            stack_ops.push(f"ADD|{nim}|{kode}|{nilai}")
            print(f"  ✓ Nilai {nilai} untuk {kode} berhasil ditambahkan.")
 
        elif pilihan == '4':
            nim = input("  NIM Mahasiswa: ").strip()
            mhs = bst.search(nim)
            if not mhs:
                print("  ✗ Mahasiswa tidak ditemukan.")
                continue
            removed = mhs.transkrip.hapus_terakhir()
            if removed:
                stack_ops.push(f"UNDO|{nim}|{removed.kode_mk}")
                print(f"  ✓ Undo: Nilai {removed.nilai_huruf} untuk {removed.kode_mk} dihapus.")
            else:
                print("  ✗ Transkrip kosong, tidak ada yang di-undo.")
 
        elif pilihan == '5':
            nim = input("  NIM Mahasiswa: ").strip()
            mhs = bst.search(nim)
            if not mhs:
                print("  ✗ Mahasiswa tidak ditemukan.")
                continue
            print(f"\n  IPK Kumulatif: {mhs.transkrip.hitung_ipk()}")
            print("  IPS per Semester:")
            for s in range(1, 9):
                ips = mhs.transkrip.hitung_ips(s)
                mk_sem = mhs.transkrip.filter_semester(s)
                if mk_sem:
                    print(f"    Semester {s}: IPS = {ips} ({len(mk_sem)} MK)")
 
        elif pilihan == '6':
            nim = input("  NIM Mahasiswa: ").strip()
            mhs = bst.search(nim)
            if not mhs:
                print("  ✗ Mahasiswa tidak ditemukan.")
                continue
            try:
                sem = int(input("  Semester yang dicari: ").strip())
            except ValueError:
                print("  ✗ Input tidak valid.")
                continue
            hasil = mhs.transkrip.filter_semester(sem)
            if hasil:
                print(f"\n  Nilai Semester {sem} - {mhs.nama}:")
                print(f"  {'Kode':<8} {'Nama MK':<30} {'Nilai':<6} {'SKS'}")
                print("  " + "-"*55)
                for n in hasil:
                    print(f"  {n.kode_mk:<8} {n.nama_mk:<30} {n.nilai_huruf:<6} {n.sks}")
            else:
                print(f"  Tidak ada nilai untuk semester {sem}.")
 
        elif pilihan == '7':
            nim = input("  NIM Mahasiswa: ").strip()
            mhs = bst.search(nim)
            if not mhs:
                print("  ✗ Mahasiswa tidak ditemukan.")
                continue
            kode = input("  Kode MK yang ingin diambil: ").strip()
            valid, belum = dag.validasi_pengambilan(mhs, kode)
            if valid:
                print(f"  ✓ {mhs.nama} BOLEH mengambil {kode}. Semua prasyarat terpenuhi.")
            else:
                print(f"  ✗ Belum boleh! Prasyarat yang belum lulus: {', '.join(belum)}")
 
        elif pilihan == '8':
            topo = dag.topological_sort()
            print("\n  Urutan Topological Sort Matakuliah:")
            for i, mk in enumerate(topo, 1):
                info = dag.mk_info.get(mk, (mk, 0, 0))
                print(f"  {i:>3}. {mk:<10} {info[0]:<30} SKS:{info[1]} Sem:{info[2]}")
 
        elif pilihan == '9':
            semua = bst.inorder()
            print(f"\n  Total Mahasiswa: {len(semua)}")
            print(f"  {'No':<4} {'NIM':<15} {'Nama':<25} {'Prodi':<6} {'IPK'}")
            print("  " + "-"*60)
            for i, m in enumerate(semua, 1):
                print(f"  {i:<4} {m.nim:<15} {m.nama:<25} {m.prodi:<6} {m.transkrip.hitung_ipk()}")
 
        elif pilihan == '10':
            eksperimen_performa(bst, dag)
 
        elif pilihan == '11':
            analisis_lanjutan(bst, dag)
 
        elif pilihan == '12':
            print(f"\n  Riwayat {stack_ops.size} operasi terakhir (top=terbaru):")
            stack_ops.tampilkan()
 
        elif pilihan == '0':
            print("\n  Terima kasih! Program selesai.")
            break
        else:
            print("  ✗ Pilihan tidak valid.")
 
        input("\n  [Enter untuk lanjut...]")
 
 
# ============================================================
# MAIN
# ============================================================
 
if _name_ == "_main_":
    print("  Memuat data sistem akademik...")
    print("  (seed=31, 60 mahasiswa, 40 MK, 8 semester)")
    bst, dag, stack_ops, mk_list = generate_data()
    print(f"  ✓ BST: {bst.size} mahasiswa ter-load")
    print(f"  ✓ DAG: {len(dag.adjacency)} matakuliah, {sum(len(v) for v in dag.adjacency.values())} relasi prasyarat")
    print(f"  ✓ Stack: {stack_ops.size} operasi tercatat")
 
    # Tampilkan beberapa NIM contoh untuk demo
    contoh = bst.inorder()[:5]
    print("\n  Contoh NIM untuk demo:")
    for m in contoh:
        print(f"    {m.nim} - {m.nama} ({m.prodi})")
 
    menu_utama(bst, dag, stack_ops)