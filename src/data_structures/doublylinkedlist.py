# ==========================
# NODE (DOUBLE LINKED LIST)
# ==========================

class DLLNode:
    """Node Double Linked List"""

    def __init__(self, mk, sks, grade, semester):

        self.mk = mk
        self.sks = sks
        self.grade = grade
        self.semester = semester

        self.prev = None
        self.next = None


# ==========================
# TRANSKRIP NILAI (DLL)
# ==========================

class TranskripNilai:
    """Double Linked List menyimpan riwayat nilai per semester."""

    def __init__(self):

        self.head = None
        self.tail = None
        self.size = 0

    # ==========================
    # TAMBAH NILAI
    # ==========================

    def tambah_nilai(self, mk, sks, grade, semester):
        """Sisip di tail. Big-O: O(1)"""

        baru = DLLNode(mk, sks, grade, semester)

        # jika linked list kosong
        if self.head is None:
            self.head = self.tail = baru

        else:
            self.tail.next = baru
            baru.prev = self.tail
            self.tail = baru

        self.size += 1

    # ==========================
    # HAPUS TERAKHIR
    # ==========================

    def hapus_terakhir(self):
        """Hapus dari tail (undo input). Big-O: O(1)"""

        if self.tail is None:
            return

        # jika cuma 1 node
        if self.head == self.tail:
            self.head = self.tail = None

        else:
            self.tail = self.tail.prev
            self.tail.next = None

        self.size -= 1

    # ==========================
    # TAMPILKAN TRANSKRIP
    # ==========================

    def tampilkan_transkrip(self):
        """Traverse forward"""

        current = self.head

        while current is not None:

            print(
                f"MK: {current.mk}, "
                f"SKS: {current.sks}, "
                f"Grade: {current.grade}, "
                f"Semester: {current.semester}"
            )

            current = current.next

    # ==========================
    # FILTER SEMESTER
    # ==========================

    def semester_ke(self, sem):
        """Filter nilai semester tertentu. Big-O: O(n)"""

        current = self.head

        while current:

            if current.semester == sem:

                print(
                    f"MK: {current.mk}, "
                    f"Grade: {current.grade}"
                )

            current = current.next

    # ==========================
    # HITUNG IPK
    # ==========================

    def hitung_ipk(self):
        """Hitung IPK dari semua nilai. Big-O: O(n)"""

        konversi = {
            "A": 4.0,
            "A-": 3.7,
            "B+": 3.3,
            "B": 3.0,
            "B-": 2.7,
            "C+": 2.3,
            "C": 2.0,
            "D": 1.0,
            "E": 0.0
        }

        total_bobot = 0
        total_sks = 0

        current = self.head

        while current:

            bobot = konversi.get(current.grade, 0)

            total_bobot += bobot * current.sks
            total_sks += current.sks

            current = current.next

        if total_sks == 0:
            return 0

        return round(total_bobot / total_sks, 2)

    # ==========================
    # LEN
    # ==========================

    def __len__(self):
        return self.size


# ==========================
# TESTING
# ==========================

if __name__ == "__main__":

    transkrip = TranskripNilai()

    transkrip.tambah_nilai(
        "ELT101",
        3,
        "A",
        1
    )

    transkrip.tambah_nilai(
        "INF202",
        4,
        "B+",
        2
    )

    transkrip.tambah_nilai(
        "MAT101",
        2,
        "B",
        1
    )

    print("=== TRANSKRIP ===")
    transkrip.tampilkan_transkrip()

    print("\n=== SEMESTER 1 ===")
    transkrip.semester_ke(1)

    print("\n=== IPK ===")
    print(transkrip.hitung_ipk())

    print("\n=== JUMLAH NODE ===")
    print(len(transkrip))

    print("\n=== HAPUS TERAKHIR ===")
    transkrip.hapus_terakhir()