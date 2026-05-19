import numpy as np

# ==========================================
# 1. KONFIGURASI PARAMETER (BERDASARKAN GAMBAR)
# ==========================================
NUM_MAHASISWA = 60
NUM_MATAKULIAH = 40
SEMESTER_DIKELOLA = 8
RANDOM_SEED = 31
OPERASI_MINIMUM = 250

# Set seed agar hasil random konsisten
np.random.seed(RANDOM_SEED)

# Daftar Grade Sistem beserta Bobot Nilainya untuk hitung IPK
GRADE_SYSTEM = {
    'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 
    'B-': 2.7, 'C+': 2.3, 'C': 2.0, 'D': 1.0, 'E': 0.0
}
GRADES = list(GRADE_SYSTEM.keys())

# Generate Data Dummy Kode Matakuliah (ELT/INF/MES/SIP/KIM)
prodi_list = ['ELT', 'INF', 'MES', 'SIP', 'KIM']
KODE_MK_LIST = [f"{np.random.choice(prodi_list)}{100 + i}" for i in range(NUM_MATAKULIAH)]

# Generate NIM Mahasiswa (Format: 21XXXXXXXXX)
NIM_LIST = [f"21{202600000 + i}" for i in range(NUM_MAHASISWA)]


# ==========================================
# 2. STRUKTUR DATA: DOUBLY LINKED LIST (DLL)
# ==========================================
class NodeNilai:
    """Node untuk menyimpan data nilai mata kuliah."""
    def __init__(self, kode_mk, semester, grade):
        self.kode_mk = kode_mk
        self.semester = semester
        self.grade = grade
        self.next = None
        self.prev = None

class DLLNilaiMahasiswa:
    """Doubly Linked List untuk menampung riwayat nilai per mahasiswa."""
    def __init__(self):
        self.head = None
        self.tail = None

    def tambah_nilai(self, kode_mk, semester, grade):
        """Menambahkan nilai di akhir list (Insert Last) -> O(1)"""
        new_node = NodeNilai(kode_mk, semester, grade)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        return new_node  # Mengembalikan pointer node untuk kebutuhan tracking

    def hapus_terakhir(self):
        """Menghapus nilai terakhir (Delete Last) -> O(1)"""
        if not self.tail:
            return None
        
        node_dihapus = self.tail
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
            
        return node_dihapus

    def hitung_ipk(self):
        """Menghitung ulang IPK berdasarkan seluruh node di DLL."""
        if not self.head:
            return 0.0
        total_bobot = 0.0
        total_mk = 0
        current = self.head
        while current:
            total_bobot += GRADE_SYSTEM[current.grade]
            total_mk += 1
            current = current.next
        return round(total_bobot / total_mk, 2) if total_mk > 0 else 0.0


# ==========================================
# 3. STRUKTUR DATA: MAHASISWA & STACK GLOBAL
# ==========================================
class Mahasiswa:
    def __init__(self, nim):
        self.nim = nim
        self.list_nilai = DLLNilaiMahasiswa()
        self.ipk = 0.0

    def update_ipk(self):
        self.ipk = self.list_nilai.hitung_ipk()

class StackGlobalUndo:
    """Stack Global untuk melacak riwayat operasi secara LIFO."""
    def __init__(self):
        self.items = []

    def push(self, nim, kode_mk):
        # Push informasi operasi terakhir ke stack -> O(1)
        self.items.append({'nim': nim, 'kode_mk': kode_mk})

    def pop(self):
        # Pop riwayat paling atas -> O(1)
        if not self.is_empty():
            return self.items.pop()
        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)


# ==========================================
# 4. SISTEM UTAMA & SIMULASI CLI OPRASI
# ==========================================
class SistemAkademik:
    def __init__(self):
        # Inisialisasi 60 mahasiswa ke dalam database/dictionary
        self.db_mahasiswa = {nim: Mahasiswa(nim) for nim in NIM_LIST}
        self.stack_undo = StackGlobalUndo()

    def insert_nilai(self, nim, kode_mk, semester, grade, verbose=True):
        """Operasi Menambahkan Nilai"""
        mhs = self.db_mahasiswa[nim]
        mhs.list_nilai.tambah_nilai(kode_mk, semester, grade)
        mhs.update_ipk()
        
        # Log ke Stack Global
        self.stack_undo.push(nim, kode_mk)
        
        if verbose:
            print(f"[INSERT] NIM: {nim} | MK: {kode_mk} | Grade: {grade} | IPK Baru: {mhs.ipk}")

    def undo_nilai(self):
        """Operasi Membatalkan Input Terakhir"""
        operasi_terakhir = self.stack_undo.pop()
        
        if not operasi_terakhir:
            print("[UNDO GAGAL] Riwayat stack kosong! Tidak ada operasi yang bisa di-undo.")
            return
        
        nim = operasi_terakhir['nim']
        kode_mk = operasi_terakhir['kode_mk']
        
        mhs = self.db_mahasiswa[nim]
        node_dihapus = mhs.list_nilai.hapus_terakhir()
        mhs.update_ipk()
        
        print(f"[UNDO SUCCESS] Membatalkan input MK {kode_mk} pada NIM {nim} -> IPK Kembali ke: {mhs.ipk}")


# ==========================================
# 5. JALANKAN SIMULASI (MINIMUM 250 OPERASI)
# ==========================================
if __name__ == "__main__":
    sistem = SistemAkademik()
    
    print("=== MEMULAI SIMULASI OPERASI CAMPURAN (MIN. 250 OPERASI) ===")
    
    # Melakukan campuran operasi secara acak sampai minimal 250 operasi
    for i in range(1, OPERASI_MINIMUM + 1):
        # Tentukan jenis operasi: 85% Insert, 15% Undo (agar data tetap terisi)
        jenis_operasi = np.random.choice(['INSERT', 'UNDO'], p=[0.85, 0.15])
        
        print(f"Ops ke-{i:03d} -> ", end="")
        
        if jenis_operasi == 'INSERT' or sistem.stack_undo.is_empty():
            # Pilih komponen random berdasarkan parameter gambar
            mhs_random = np.random.choice(NIM_LIST)
            mk_random = np.random.choice(KODE_MK_LIST)
            sem_random = int(np.random.randint(1, SEMESTER_DIKELOLA + 1))
            grade_random = np.random.choice(GRADES)
            
            sistem.insert_nilai(mhs_random, mk_random, sem_random, grade_random)
        else:
            sistem.undo_nilai()

    print("\n=============================================")
    print(f"Simulasi Selesai. Ukuran Stack Undo tersisa: {sistem.stack_undo.size()} operasi.")
    print("=============================================")