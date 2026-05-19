# =========================
# NODE (DOUBLE LINKED LIST)
# =========================

class DLLNode:
    """Node Double Linked List"""
    def __init__(self, mk, sks, grade, semester):
        self.mk = mk
        self.sks = sks
        self.grade = grade
        self.semester = semester

        self.prev = None
        self.next = None

# =========================
# ==Transkrip Nilai (DLL)==
# =========================

class TranskripNilai:
    """Double Linked List menyimpan riwayat nilai per semester."""
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def tambah_nilai (self, mk, sks, grade, semester):
        """Sisip di tail. Big-O: O(1) dengan pointer tail."""
        baru = DLLNode(mk, sks, grade, semester)
        if self.head is None:
            self.head = self.tail = baru
        else:
            self.tail.next = baru
            baru.prev = self.tail
            self.tail = baru

        self.size += 1
    def hapus_terakhir (self):
        """Hapus dari tail (undo input) dengan pointer tail."""
        if self.tail is None:
            return
        self.size -= 1

        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
    def tampilkan_transkrip(self):
        """Tampilkan semua nilai dari head ke tail."""
        current = self.head
        while current is not None:
            print(f"MK: {current.mk}, SKS: {current.sks}, Grade: {current.grade}, Semester: {current.semester}")
            current = current.next
    def semester_ke (self, sem):
        """Filter nilai semester tertentu. Big-O: O(n) karena harus cek semua node."""
        current = self.head
        while current:
            if current.semester == sem:
                print(
                    current.mk,
                    current.grade
                    )
            current = current.next
    def hitung_ipk (self):
        """Hitung IPK dari semua nilai. Big-O: O(n)."""
        current = self.head
        total_bobot = 0
        total_sks = 0

        Konfersi = {
            'A': 4.0,
            'A-': 3.7,
            'B+': 3.3,
            'B': 3.0,
            'B-': 2.7,
            'C+': 2.3,
            'C': 2.0,
            'D': 1.0,
            'E': 0.0
        }
        while current:
            bobot = Konfersi.get(current.grade, 0)
            total_bobot += bobot * current.sks
            total_sks += current.sks

            current = current.next

        if total_sks == 0:
            return 0
        return round(total_bobot / total_sks, 2)
