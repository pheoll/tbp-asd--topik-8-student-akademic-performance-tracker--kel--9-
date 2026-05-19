"""
MODUL 2: BST Data Mahasiswa
============================
- Kunci = NIM mahasiswa
- Setiap node menyimpan objek Mahasiswa + referensi ke DLL transkripnya
- Operasi: insert, search, update_ipk, inorder, range_ipk
- Big-O: O(log n) rata-rata
"""
 
import random
 
random.seed(31)
 
# ──────────────────────────────────────────
# GRADE & SETUP
# ──────────────────────────────────────────
GRADE_POINT = {
    'A': 4.0, 'A-': 3.7,
    'B+': 3.3, 'B': 3.0, 'B-': 2.7,
    'C+': 2.3, 'C': 2.0,
    'D': 1.0,  'E': 0.0
}
GRADES = list(GRADE_POINT.keys())
PRODI_CODES = ['ELT', 'INF', 'MES', 'SIP', 'KIM']
 
def generate_kode_mk():
    mks = []
    for prodi in PRODI_CODES:
        for i in range(1, 9):
            mks.append(f"{prodi}{i:03d}")
    return mks
 
ALL_MK = generate_kode_mk()   # 40 MK
 
 
# ──────────────────────────────────────────
# MODUL 1 (ringkas) – DLL Transkrip Nilai
# ──────────────────────────────────────────
 
class NodeNilai:
    def __init__(self, kode_mk, sks, grade, semester):
        self.kode_mk  = kode_mk
        self.sks      = sks
        self.grade    = grade
        self.semester = semester
        self.prev     = None
        self.next     = None
 
 
class TranskripNilai:
    """Doubly Linked List nilai – dipakai oleh setiap node BST."""
 
    def __init__(self):
        self.head = None
        self.tail = None
        self.total_node = 0
 
    # O(1) – insert di ekor
    def tambah_nilai(self, kode_mk, sks, grade, semester):
        node = NodeNilai(kode_mk, sks, grade, semester)
        if self.tail is None:           # DLL masih kosong
            self.head = self.tail = node
        else:
            node.prev    = self.tail
            self.tail.next = node
            self.tail    = node
        self.total_node += 1
 
    # O(1) – hapus ekor (untuk UNDO)
    def hapus_terakhir(self):
        if self.tail is None:
            return None
        hapus = self.tail
        if self.head == self.tail:      # hanya satu node
            self.head = self.tail = None
        else:
            self.tail      = self.tail.prev
            self.tail.next = None
        self.total_node -= 1
        return hapus
 
    # O(n) – filter berdasarkan semester
    def filter_semester(self, semester):
        hasil = []
        cur = self.head
        while cur:
            if cur.semester == semester:
                hasil.append(cur)
            cur = cur.next
        return hasil
 
    # O(n) – hitung IPK dari seluruh nilai
    def hitung_ipk(self):
        total_bobot = 0.0
        total_sks   = 0
        cur = self.head
        while cur:
            total_bobot += GRADE_POINT[cur.grade] * cur.sks
            total_sks   += cur.sks
            cur = cur.next
        return round(total_bobot / total_sks, 2) if total_sks > 0 else 0.0
 
    # tampilkan semua nilai (untuk TRANSKRIPSI)
    def tampilkan(self):
        cur = self.head
        while cur:
            print(f"  Sem {cur.semester} | {cur.kode_mk} | SKS: {cur.sks} "
                  f"| Grade: {cur.grade} ({GRADE_POINT[cur.grade]})")
            cur = cur.next
 
 
# ──────────────────────────────────────────
# Class Mahasiswa
# ──────────────────────────────────────────
 
class Mahasiswa:
    def __init__(self, nim, nama, prodi, angkatan):
        self.nim      = nim
        self.nama     = nama
        self.prodi    = prodi
        self.angkatan = angkatan
 
    def __repr__(self):
        return f"Mahasiswa({self.nim}, {self.nama}, {self.prodi})"
 
 
# ──────────────────────────────────────────
# MODUL 2: BST Data Mahasiswa
# ──────────────────────────────────────────
 
class BSTNodeMhs:
    def __init__(self, mhs):
        self.mhs        = mhs                 # objek Mahasiswa
        self.transkripsi = TranskripNilai()   # DLL nilai milik mahasiswa ini
        self.left       = None
        self.right      = None
 
 
class BSTMahasiswa:
    def __init__(self):
        self.root = None
 
    # ── INSERT ────────────────────────────────────────────────
    def insert(self, mhs):
        """
        Masukkan mahasiswa ke BST berdasarkan NIM.
        Big-O: O(log n) rata-rata, O(n) worst case (pohon miring).
        """
        if self.root is None:
            self.root = BSTNodeMhs(mhs)
        else:
            self._insert_rekursif(self.root, mhs)
 
    def _insert_rekursif(self, node, mhs):
        if mhs.nim < node.mhs.nim:
            if node.left is None:
                node.left = BSTNodeMhs(mhs)       # tempat kosong → taruh di sini
            else:
                self._insert_rekursif(node.left, mhs)
        elif mhs.nim > node.mhs.nim:
            if node.right is None:
                node.right = BSTNodeMhs(mhs)
            else:
                self._insert_rekursif(node.right, mhs)
        # NIM sama → abaikan (duplikat tidak diperbolehkan)
 
    # ── SEARCH ───────────────────────────────────────────────
    def search(self, nim):
        """
        Cari mahasiswa berdasarkan NIM.
        Kembalikan BSTNodeMhs jika ditemukan, None jika tidak.
        Big-O: O(log n) rata-rata.
        """
        return self._search_rekursif(self.root, nim)
 
    def _search_rekursif(self, node, nim):
        if node is None:
            return None                           # tidak ditemukan
        if nim == node.mhs.nim:
            return node                           # ketemu!
        elif nim < node.mhs.nim:
            return self._search_rekursif(node.left, nim)
        else:
            return self._search_rekursif(node.right, nim)
 
    # ── UPDATE IPK ───────────────────────────────────────────
    def update_ipk(self, nim):
        """
        Cari node lalu hitung ulang IPK dari DLL transkripsinya.
        Big-O: O(log n) untuk search + O(n_nilai) untuk hitung IPK.
        """
        node = self.search(nim)
        if node is None:
            print(f"[!] Mahasiswa NIM {nim} tidak ditemukan.")
            return None
        ipk_baru = node.transkripsi.hitung_ipk()
        print(f"[✓] IPK {node.mhs.nama} ({nim}) diperbarui → {ipk_baru}")
        return ipk_baru
 
    # ── INORDER (daftar terurut NIM) ─────────────────────────
    def inorder(self):
        """
        Traversal inorder → menghasilkan list node terurut dari NIM terkecil.
        Big-O: O(n).
        """
        hasil = []
        self._inorder_rekursif(self.root, hasil)
        return hasil
 
    def _inorder_rekursif(self, node, hasil):
        if node is None:
            return
        self._inorder_rekursif(node.left, hasil)
        hasil.append(node)
        self._inorder_rekursif(node.right, hasil)
 
    # ── RANGE IPK ────────────────────────────────────────────
    def range_ipk(self, low, high):
        """
        Kembalikan list node yang IPK-nya berada dalam rentang [low, high].
        Big-O: O(n) – harus cek semua node (IPK tidak disimpan di BST key).
        """
        semua  = self.inorder()
        hasil  = []
        for node in semua:
            ipk = node.transkripsi.hitung_ipk()
            if low <= ipk <= high:
                hasil.append((node, ipk))
        return hasil
 
 
# ──────────────────────────────────────────
# GENERATE DATA: 60 mahasiswa, 40 MK, 8 sem
# ──────────────────────────────────────────
 
def generate_data():
    bst = BSTMahasiswa()
    nama_contoh = [
        "Aldi","Budi","Citra","Dewi","Eko","Fajar","Gita","Hana",
        "Irfan","Joko","Kiki","Lina","Miko","Nani","Omar","Putri",
        "Qori","Rudi","Sari","Tono","Umar","Vina","Widi","Xena",
        "Yudi","Zara","Agus","Bella","Cahya","Dani","Elsa","Feri",
        "Galih","Hendra","Indah","Johan","Kartika","Lutfi","Maya","Noval",
        "Okta","Prima","Quincy","Reza","Siska","Teguh","Ulfa","Vito",
        "Wahyu","Xander","Yanti","Zahra","Andi","Bagas","Clara","Dinda",
        "Evan","Fira","Gilang","Hesti"
    ]
 
    for i in range(60):
        nim     = f"21{(i+1):08d}"
        nama    = nama_contoh[i]
        prodi   = random.choice(PRODI_CODES)
        angkatan = 2021
        mhs     = Mahasiswa(nim, nama, prodi, angkatan)
        bst.insert(mhs)
 
        # Isi DLL transkrip: tiap mhs dapat nilai di 40 MK selama 8 semester
        node_bst = bst.search(nim)
        mk_per_sem = len(ALL_MK) // 8   # 5 MK/semester
        for sem in range(1, 9):
            mks_sem = ALL_MK[(sem-1)*mk_per_sem : sem*mk_per_sem]
            for kode in mks_sem:
                sks   = random.choice([2, 3, 4])
                grade = random.choice(GRADES)
                node_bst.transkripsi.tambah_nilai(kode, sks, grade, sem)
 
    return bst