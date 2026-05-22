import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# =========================================
# DATACLASS MAHASISWA
# =========================================
class Mahasiswa:
    """
    Objek data mahasiswa yang disimpan di setiap node BST.

    Atribut:
        nim      : NIM mahasiswa (kunci BST), format '21XXXXXXXX'
        nama     : nama lengkap mahasiswa
        prodi    : program studi
        angkatan : tahun angkatan (2021/2022/2023)
        ipk      : IPK kumulatif, dihitung ulang dari DLL transkripsi
    """
    def __init__(self, nim, nama, prodi='', angkatan=2021, ipk=0.0):
        self.nim      = nim
        self.nama     = nama
        self.prodi    = prodi
        self.angkatan = angkatan
        self.ipk      = ipk

    def __repr__(self):
        return f"Mahasiswa({self.nim}, {self.nama}, IPK={self.ipk:.2f})"


# =========================================
# NODE BST MAHASISWA
# =========================================
class BSTNodeMhs:
    """
    Node BST yang menyimpan objek Mahasiswa + DLL transkripsi nilai.

    Big-O ruang per node: O(1) untuk pointer + O(m) untuk DLL transkripsi
    di mana m = jumlah matakuliah yang ditempuh mahasiswa tersebut.
    """
    def __init__(self, mhs):
        self.mhs = mhs
        # Setiap node punya DLL transkripsi sendiri
        # Import lazy untuk menghindari circular import
        from doubly_linked_list import TranskripNilai
        self.transkripsi = TranskripNilai()
        self.left  = None
        self.right = None


# =========================================
# BST MAHASISWA
# =========================================
class BSTMahasiswa:
    """
    Binary Search Tree dengan kunci = NIM mahasiswa (string).

    Properti BST:
        node.left.mhs.nim  < node.mhs.nim  (subtree kiri lebih kecil)
        node.right.mhs.nim > node.mhs.nim  (subtree kanan lebih besar)

    Big-O rata-rata (BST seimbang, tinggi h = log n):
        insert     : O(log n)
        search     : O(log n)
        update_ipk : O(log n) + O(m)
        inorder    : O(n)
        range_ipk  : O(n)

    Big-O worst-case (BST miring, NIM dimasukkan berurutan):
        semua operasi : O(n)
        Mitigasi: pre-shuffle data sebelum insert (lihat modul_2.py)
    """

    def __init__(self):
        self.root = None

    # =====================================
    # INSERT
    # Big-O Waktu: O(log n) rata-rata, O(n) worst-case
    # Big-O Ruang: O(log n) stack rekursi
    # =====================================
    def insert(self, mhs):
        """Sisipkan objek Mahasiswa ke BST berdasarkan NIM."""
        self.root = self._insert_rekursif(self.root, mhs)

    def _insert_rekursif(self, node, mhs):
        """Helper rekursif insert."""
        if node is None:
            return BSTNodeMhs(mhs)
        if mhs.nim < node.mhs.nim:
            node.left  = self._insert_rekursif(node.left,  mhs)
        elif mhs.nim > node.mhs.nim:
            node.right = self._insert_rekursif(node.right, mhs)
        # NIM sama = duplikat, diabaikan
        return node

    # =====================================
    # SEARCH
    # Big-O Waktu: O(log n) rata-rata, O(n) worst-case
    # Big-O Ruang: O(log n) stack rekursi
    # =====================================
    def search(self, nim):
        """
        Cari mahasiswa berdasarkan NIM.
        Return: BSTNodeMhs jika ditemukan, None jika tidak ada.
        """
        return self._search_rekursif(self.root, nim)

    def _search_rekursif(self, node, nim):
        """Helper rekursif search."""
        if node is None:
            return None
        if nim == node.mhs.nim:
            return node
        elif nim < node.mhs.nim:
            return self._search_rekursif(node.left,  nim)
        else:
            return self._search_rekursif(node.right, nim)

    # =====================================
    # UPDATE IPK
    # Big-O Waktu: O(log n) search + O(m) hitung_ipk
    # Big-O Ruang: O(log n) stack rekursi
    # =====================================
    def update_ipk(self, nim):
        """
        Cari node mahasiswa lalu hitung ulang IPK dari DLL transkripsinya.
        Dipanggil setiap kali INPUT_NILAI atau UNDO_NILAI dijalankan.
        """
        node = self.search(nim)
        if node is not None:
            # Hitung ulang IPK dari seluruh node DLL — O(m)
            node.mhs.ipk = node.transkripsi.hitung_ipk()

    # =====================================
    # INORDER TRAVERSAL
    # Big-O Waktu: O(n) — setiap node dikunjungi tepat sekali
    # Big-O Ruang: O(n) list hasil + O(h) stack rekursi
    # =====================================
    def inorder(self):
        """
        Kembalikan list objek Mahasiswa terurut NIM ascending.
        Inorder BST selalu terurut karena properti BST.
        """
        hasil = []
        self._inorder_rekursif(self.root, hasil)
        return hasil

    def _inorder_rekursif(self, node, hasil):
        """Helper rekursif inorder: kiri -> root -> kanan."""
        if node is None:
            return
        self._inorder_rekursif(node.left,  hasil)
        hasil.append(node.mhs)
        self._inorder_rekursif(node.right, hasil)

    # =====================================
    # RANGE IPK
    # Big-O Waktu: O(n) — inorder penuh + filter
    # Big-O Ruang: O(n)
    # Catatan: BST diindeks NIM bukan IPK, sehingga tidak bisa O(log n).
    # Untuk O(log n + k) perlu secondary BST dengan kunci IPK
    # (lihat Pertanyaan Analisis no.2 di laporan)
    # =====================================
    def range_ipk(self, low, high):
        """
        Kembalikan list Mahasiswa dengan IPK dalam rentang [low, high].
        """
        semua = self.inorder()
        return [mhs for mhs in semua if low <= mhs.ipk <= high]