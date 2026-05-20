from dataclasses import dataclass
from typing import Optional


@dataclass
class Mahasiswa:
    nim: str
    nama: str
    prodi: str
    angkatan: int
    status: int = 0
    ipk: float = 0.0


class BSTNodeMhs:
    """Node BST yang menyimpan objek Mahasiswa + referensi ke DLL transkripsinya."""

    def __init__(self, mhs: Mahasiswa):
        self.mhs = mhs
        # Import di sini untuk menghindari circular import
        from doubly_linked_list import TranskripNilai
        self.transkripsi = TranskripNilai()
        self.left = None
        self.right = None


class BSTMahasiswa:
    """
    Binary Search Tree dengan kunci = NIM mahasiswa (string).

    Properti BST:
        - node.left.mhs.nim  < node.mhs.nim  (semua di subtree kiri lebih kecil)
        - node.right.mhs.nim > node.mhs.nim  (semua di subtree kanan lebih besar)

    Big-O rata-rata (BST seimbang, h = log n):
        insert  : O(log n)
        search  : O(log n)
        delete  : O(log n)
        inorder : O(n)

    Big-O worst-case (BST miring/degenerate, NIM dimasukkan berurutan):
        semua operasi : O(n)  — BST menjadi linked list linear

    Catatan: gunakan pre-shuffle data sebelum insert untuk menghindari worst-case.
    """

    def __init__(self):
        self.root = None

    # ------------------------------------------------------------------ #
    #  INSERT                                                              #
    # ------------------------------------------------------------------ #

    def insert(self, mhs: Mahasiswa):
        """
        Sisipkan mahasiswa baru ke BST berdasarkan NIM.

        Big-O Waktu : O(log n) rata-rata, O(n) worst-case (BST miring)
        Big-O Ruang : O(log n) stack rekursi rata-rata, O(n) worst-case

        Args:
            mhs: objek Mahasiswa yang akan disisipkan
        """
        self.root = self._insert_rekursif(self.root, mhs)

    def _insert_rekursif(self, node: Optional[BSTNodeMhs], mhs: Mahasiswa) -> BSTNodeMhs:
        """Helper rekursif untuk insert."""
        if node is None:
            # Posisi kosong ditemukan, buat node baru
            return BSTNodeMhs(mhs)

        if mhs.nim < node.mhs.nim:
            # NIM lebih kecil, masuk ke subtree kiri
            node.left = self._insert_rekursif(node.left, mhs)
        elif mhs.nim > node.mhs.nim:
            # NIM lebih besar, masuk ke subtree kanan
            node.right = self._insert_rekursif(node.right, mhs)
        # Jika NIM sama, tidak dimasukkan (NIM unik)

        return node

    # ------------------------------------------------------------------ #
    #  SEARCH                                                              #
    # ------------------------------------------------------------------ #

    def search(self, nim: str) -> Optional[BSTNodeMhs]:
        """
        Cari node BST berdasarkan NIM.

        Big-O Waktu : O(log n) rata-rata, O(n) worst-case
        Big-O Ruang : O(log n) stack rekursi rata-rata

        Args:
            nim: NIM mahasiswa yang dicari

        Return:
            BSTNodeMhs jika ditemukan, None jika tidak ada
        """
        return self._search_rekursif(self.root, nim)

    def _search_rekursif(self, node: Optional[BSTNodeMhs], nim: str) -> Optional[BSTNodeMhs]:
        """Helper rekursif untuk search."""
        if node is None:
            # Tidak ditemukan
            return None

        if nim == node.mhs.nim:
            # NIM cocok, kembalikan node ini
            return node
        elif nim < node.mhs.nim:
            # NIM lebih kecil, cari di subtree kiri
            return self._search_rekursif(node.left, nim)
        else:
            # NIM lebih besar, cari di subtree kanan
            return self._search_rekursif(node.right, nim)

    # ------------------------------------------------------------------ #
    #  UPDATE IPK                                                          #
    # ------------------------------------------------------------------ #

    def update_ipk(self, nim: str):
        """
        Cari node mahasiswa, lalu hitung ulang IPK dari DLL transkripsinya.

        Big-O Waktu : O(log n) untuk search + O(m) untuk hitung_ipk
                      di mana m = jumlah matakuliah mahasiswa tersebut
        Big-O Ruang : O(log n) stack rekursi

        Args:
            nim: NIM mahasiswa yang IPK-nya akan diperbarui
        """
        node = self.search(nim)
        if node is not None:
            # Hitung ulang IPK dari seluruh node DLL transkripsi
            node.mhs.ipk = node.transkripsi.hitung_ipk()

    # ------------------------------------------------------------------ #
    #  INORDER TRAVERSAL                                                   #
    # ------------------------------------------------------------------ #

    def inorder(self):
        """
        Kembalikan list objek Mahasiswa dalam urutan NIM ascending (inorder traversal).
        Inorder BST selalu menghasilkan urutan terurut karena properti BST.

        Big-O Waktu : O(n) — setiap node dikunjungi tepat sekali
        Big-O Ruang : O(n) untuk list hasil + O(h) stack rekursi

        Return:
            list Mahasiswa terurut berdasarkan NIM
        """
        hasil = []
        self._inorder_rekursif(self.root, hasil)
        return hasil

    def _inorder_rekursif(self, node: Optional[BSTNodeMhs], hasil: list):
        """Helper rekursif inorder: kiri -> root -> kanan."""
        if node is None:
            return
        self._inorder_rekursif(node.left, hasil)
        hasil.append(node.mhs)
        self._inorder_rekursif(node.right, hasil)

    # ------------------------------------------------------------------ #
    #  RANGE IPK                                                           #
    # ------------------------------------------------------------------ #

    def range_ipk(self, low: float, high: float):
        """
        Kembalikan list mahasiswa yang IPK-nya berada dalam rentang [low, high].

        Catatan Big-O:
            BST diindeks berdasarkan NIM, bukan IPK. Oleh karena itu tidak bisa
            memanfaatkan properti BST untuk memangkas pencarian berdasarkan IPK.
            Seluruh tree harus ditelusuri (inorder traversal + filter).

        Big-O Waktu : O(n) — inorder traversal penuh lalu filter IPK
        Big-O Ruang : O(n) untuk list hasil + O(h) stack rekursi

        Optimasi lanjutan (lihat Pertanyaan Analisis no.2):
            Gunakan secondary BST dengan kunci IPK untuk O(log n + k).

        Args:
            low  : batas bawah IPK (inklusif)
            high : batas atas IPK (inklusif)

        Return:
            list Mahasiswa dengan IPK dalam [low, high]
        """
        semua = self.inorder()
        return [mhs for mhs in semua if low <= mhs.ipk <= high]
