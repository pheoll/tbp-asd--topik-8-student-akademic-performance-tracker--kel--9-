from collections import deque


class GraphPrereq:
    """
    Directed Acyclic Graph (DAG) untuk memodelkan prasyarat matakuliah.

    Representasi: Adjacency List
        self.adj  : dict { kode_mk -> list[kode_prasyarat] }
                    edge A -> B berarti A adalah prasyarat B
                    (untuk mengetahui prasyarat suatu MK, lihat self.adj[kode_mk])
        self.matkul: dict { kode_mk -> nama_mk }

    Pemilihan Adjacency List vs Adjacency Matrix:
        - Adjacency List  : O(V+E) ruang — efisien untuk sparse graph (E << V²)
        - Adjacency Matrix: O(V²) ruang  — boros untuk kurikulum 40 MK, 55 relasi
        Kurikulum ini sparse (55 edge dari maks 40*39=1560), sehingga adj list dipilih.

    Big-O ringkasan:
        tambah_matkul     : O(1)
        tambah_prasyarat  : O(1)
        topological_sort  : O(V+E)
        prasyarat_terpenuhi: O(deg(v)) di mana deg = jumlah prasyarat MK tersebut
    """

    def __init__(self):
        # kode_mk -> list kode prasyaratnya
        self.adj = {}
        # kode_mk -> nama lengkap matakuliah
        self.matkul = {}

    # ------------------------------------------------------------------ #
    #  TAMBAH MATAKULIAH                                                   #
    # ------------------------------------------------------------------ #

    def tambah_matkul(self, kode: str, nama: str):
        """
        Daftarkan matakuliah baru ke graph.

        Big-O Waktu : O(1) — insert ke dict
        Big-O Ruang : O(1) — satu entry baru di adj dan matkul

        Args:
            kode: kode unik matakuliah (contoh: 'ELT101')
            nama: nama lengkap matakuliah
        """
        if kode not in self.adj:
            self.adj[kode] = []
        self.matkul[kode] = nama

    # ------------------------------------------------------------------ #
    #  TAMBAH PRASYARAT                                                    #
    # ------------------------------------------------------------------ #

    def tambah_prasyarat(self, kode_mk: str, kode_prasyarat: str):
        """
        Tambahkan relasi prasyarat: kode_prasyarat harus lulus sebelum kode_mk.
        Dalam representasi adj list: self.adj[kode_mk] menyimpan daftar prasyaratnya.

        Big-O Waktu : O(1) — append ke list adjacency
        Big-O Ruang : O(1) — satu entry baru di list

        Args:
            kode_mk        : matakuliah yang memiliki prasyarat
            kode_prasyarat : matakuliah yang harus lulus terlebih dahulu
        """
        # Pastikan kedua kode terdaftar di graph
        if kode_mk not in self.adj:
            self.adj[kode_mk] = []
        if kode_prasyarat not in self.adj:
            self.adj[kode_prasyarat] = []

        # Tambahkan prasyarat ke daftar prasyarat kode_mk
        if kode_prasyarat not in self.adj[kode_mk]:
            self.adj[kode_mk].append(kode_prasyarat)

    # ------------------------------------------------------------------ #
    #  TOPOLOGICAL SORT (Kahn's Algorithm)                                 #
    # ------------------------------------------------------------------ #

    def topological_sort(self):
        """
        Hasilkan urutan pengambilan matakuliah yang valid menggunakan Kahn's Algorithm.

        Kahn's Algorithm (BFS-based):
            1. Hitung in-degree setiap node (berapa MK lain yang membutuhkan node ini
               sebagai prasyarat — bukan berapa prasyarat yang dimiliki node ini).
            2. Masukkan semua node dengan in-degree = 0 ke queue (bisa langsung diambil).
            3. Selama queue tidak kosong:
               a. Dequeue satu MK, tambahkan ke hasil urutan.
               b. Untuk setiap MK lain yang memiliki MK ini sebagai prasyarat,
                  kurangi in-degree-nya. Jika in-degree menjadi 0, enqueue.
            4. Jika panjang hasil == jumlah node: tidak ada siklus (valid DAG).
               Jika hasil < jumlah node: ada siklus (tidak semua node bisa diproses).

        Big-O Waktu : O(V+E) — setiap vertex dan edge diproses tepat sekali
        Big-O Ruang : O(V+E) — in_degree dict + reverse_adj + queue + hasil

        Return:
            list kode_mk dalam urutan topologis yang valid,
            atau list kosong jika terdeteksi siklus (DAG tidak valid)
        """
        # Langkah 1: Bangun reverse adjacency list
        # reverse_adj[A] = list MK yang memerlukan A sebagai prasyarat
        # (arah edge dibalik: prasyarat -> MK yang membutuhkan)
        in_degree = {kode: 0 for kode in self.adj}
        reverse_adj = {kode: [] for kode in self.adj}

        for mk, prasyarat_list in self.adj.items():
            for p in prasyarat_list:
                # mk membutuhkan p, jadi in-degree mk bertambah
                in_degree[mk] += 1
                # p mengarah ke mk dalam reverse graph
                if p in reverse_adj:
                    reverse_adj[p].append(mk)

        # Langkah 2: Masukkan semua MK tanpa prasyarat ke queue
        queue = deque()
        for kode, deg in in_degree.items():
            if deg == 0:
                queue.append(kode)

        hasil = []

        # Langkah 3: Proses BFS
        while queue:
            mk = queue.popleft()
            hasil.append(mk)

            # Kurangi in-degree MK yang membutuhkan mk ini sebagai prasyarat
            for mk_berikut in reverse_adj[mk]:
                in_degree[mk_berikut] -= 1
                if in_degree[mk_berikut] == 0:
                    queue.append(mk_berikut)

        # Langkah 4: Deteksi siklus
        # Jika ada siklus, beberapa node tidak pernah mencapai in-degree 0
        # sehingga tidak masuk ke hasil
        if len(hasil) != len(self.adj):
            # Siklus terdeteksi — kembalikan list kosong sebagai tanda error
            return []

        return hasil

    # ------------------------------------------------------------------ #
    #  CEK PRASYARAT TERPENUHI                                             #
    # ------------------------------------------------------------------ #

    def prasyarat_terpenuhi(self, nim_node, kode_mk: str) -> bool:
        """
        Cek apakah semua prasyarat untuk kode_mk sudah lulus oleh mahasiswa.
        Syarat lulus: grade >= C (grade value >= 2.0).

        Big-O Waktu : O(deg(kode_mk) * m) di mana:
                        deg = jumlah prasyarat kode_mk
                        m   = jumlah matakuliah dalam transkripsi mahasiswa
                      Dalam praktik ≈ O(deg) karena m kecil dan konstan per mahasiswa
        Big-O Ruang : O(m) untuk list semua nilai mahasiswa

        Args:
            nim_node : BSTNodeMhs — node BST mahasiswa yang akan diperiksa
            kode_mk  : kode matakuliah yang ingin diambil

        Return:
            True jika semua prasyarat sudah lulus atau tidak ada prasyarat,
            False jika ada prasyarat yang belum lulus atau belum diambil
        """
        from doubly_linked_list import GRADE_MAP

        if kode_mk not in self.adj:
            # MK tidak terdaftar di graph, anggap tidak ada prasyarat
            return True

        prasyarat_list = self.adj[kode_mk]

        if not prasyarat_list:
            # MK tidak memiliki prasyarat
            return True

        # Ambil semua nilai mahasiswa dari DLL transkripsi
        semua_nilai = nim_node.transkripsi.semua_nilai()

        # Buat dict { kode_mk: grade } untuk pencarian O(1) per prasyarat
        nilai_dict = {n.kode_mk: n.grade for n in semua_nilai}

        for p in prasyarat_list:
            if p not in nilai_dict:
                # Prasyarat belum pernah diambil
                return False
            grade_val = GRADE_MAP.get(nilai_dict[p], 0.0)
            if grade_val < 2.0:
                # Prasyarat diambil tapi nilainya di bawah C (tidak lulus)
                return False

        return True
