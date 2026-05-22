class LLNode:
    """Node Singly Linked List untuk Stack."""

    def __init__(self, data=None):
        self.data = data
        self.next: "LLNode | None" = None


class Stack:
    """
    Stack berbasis Linked List untuk menyimpan riwayat operasi INPUT_NILAI.

    Prinsip: LIFO (Last In First Out)
    Setiap elemen yang di-push terakhir akan di-pop pertama kali,
    sehingga UNDO selalu membatalkan operasi yang paling terakhir dilakukan.

    Struktur internal:
        top -> node_terbaru -> node_sebelumnya -> ... -> None

    Setiap elemen stack menyimpan dict:
        {
            'nim'    : str,   # NIM mahasiswa
            'nilai'  : NilaiMatkul  # objek nilai yang di-input
        }
    """

    def __init__(self):
        self.top = None
        self._size = 0

    def push(self, data):
        """
        Tambahkan elemen baru ke atas stack (top).

        Big-O Waktu : O(1) — insert di depan linked list, tidak perlu traversal
        Big-O Ruang : O(1) — hanya membuat 1 node baru

        Args:
            data: objek apapun yang ingin disimpan (dict operasi INPUT_NILAI)
        """
        node = LLNode(data)
        # Node baru menunjuk ke top lama, lalu top diperbarui ke node baru
        node.next = self.top
        self.top = node
        self._size += 1

    def pop(self):
        """
        Ambil dan hapus elemen dari atas stack (top).

        Big-O Waktu : O(1) — akses langsung ke top, tidak perlu traversal
        Big-O Ruang : O(1) — tidak ada alokasi memori tambahan

        Return:
            data dari top, atau None jika stack kosong
        """
        if self.top is None:
            # Stack kosong, tidak ada yang bisa di-pop
            return None

        data = self.top.data
        # Geser top ke node berikutnya (node lama di bawah top)
        self.top = self.top.next
        self._size -= 1
        return data

    def peek(self):
        """
        Lihat elemen teratas tanpa menghapusnya.

        Big-O Waktu : O(1)
        Big-O Ruang : O(1)

        Return:
            data dari top, atau None jika stack kosong
        """
        if self.top is None:
            return None
        return self.top.data

    def is_empty(self):
        """
        Cek apakah stack kosong.

        Big-O Waktu : O(1)
        Big-O Ruang : O(1)
        """
        return self.top is None

    def __len__(self):
        return self._size
