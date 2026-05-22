from modules.modul1 import ModulStackUndo
from modules.modul2 import ModulBST
from modules.modul3 import ModulGraph   # asumsi modul3 sudah ada
from modules.modul5 import ModulRanking
from data_structures.doubly_linked_list import NilaiMatkul
from data_structures.bst import Mahasiswa   # pastikan Mahasiswa ada di bst.py

class CLI_Akademik:
    """Modul 6 - Command Line Interface Utama"""
    
    def __init__(self):
        self.modul_bst = ModulBST()
        self.modul_stack = ModulStackUndo(self.modul_bst)
        self.modul_graph = ModulGraph()      # nanti diisi
        self.modul_ranking = ModulRanking(self.modul_bst)

    def jalankan(self):
        print("\n=== Student Academic Performance Tracker ===")
        print("Ketik 'BANTUAN' untuk melihat daftar perintah\n")
        
        while True:
            try:
                cmd = input("\n>>> ").strip().upper().split()
                if not cmd:
                    continue
                    
                if cmd[0] == "KELUAR":
                    print("Terima kasih telah menggunakan sistem!")
                    break
                    
                elif cmd[0] == "BANTUAN":
                    self._tampilkan_bantuan()
                    
                elif cmd[0] == "CARI_MHS" and len(cmd) > 1:
                    node = self.modul_bst.cari_mahasiswa(cmd[1])
                    if node:
                        print(f"✅ Ditemukan: {node.mhs.nama} ({node.mhs.prodi}) - IPK: {node.mhs.ipk:.2f}")
                    else:
                        print("❌ Mahasiswa tidak ditemukan")
                        
                elif cmd[0] == "INPUT_NILAI" and len(cmd) >= 6:
                    nim = cmd[1]
                    kode = cmd[2]
                    sks = int(cmd[3])
                    grade = cmd[4]
                    sem = int(cmd[5])
                    nilai = NilaiMatkul(kode, f"Matkul-{kode}", sks, grade, sem)
                    if self.modul_bst.input_nilai(nim, nilai):
                        self.modul_stack.catat_operasi(nim, nilai)
                        print(f"✅ Nilai {kode} berhasil ditambahkan")
                        
                elif cmd[0] == "UNDO_NILAI" and len(cmd) > 1:
                    self.modul_stack.undo_terakhir()
                    
                elif cmd[0] == "TRANSKRIPSI" and len(cmd) > 1:
                    transkrip = self.modul_bst.tampilkan_transkripsi(cmd[1])
                    for n in transkrip:
                        print(f"{n.kode_mk} - {n.grade} ({n.semester})")
                        
                elif cmd[0] == "IPK" and len(cmd) > 1:
                    print(f"IPK: {self.modul_bst.hitung_ipk(cmd[1]):.2f}")
                    
                elif cmd[0] == "RANKING_IPK":
                    ranking = self.modul_ranking.ranking_ipk(10)
                    print("=== TOP 10 Ranking IPK ===")
                    for i, mhs in enumerate(ranking, 1):
                        print(f"{i}. {mhs.nama} ({mhs.nim}) - IPK: {mhs.ipk:.2f}")
                        
                elif cmd[0] == "URUTAN_MATKUL":
                    urutan = self.modul_graph.topological_sort()
                    print("Urutan Matakuliah yang Valid:", urutan)
                    
                else:
                    print("❌ Perintah tidak dikenal. Ketik BANTUAN")
                    
            except Exception as e:
                print(f"Error: {e}")

    def _tampilkan_bantuan(self):
        print("""
Perintah yang tersedia:
  CARI_MHS <nim>
  INPUT_NILAI <nim> <kode_mk> <sks> <grade> <semester>
  UNDO_NILAI <nim>
  TRANSKRIPSI <nim>
  IPK <nim>
  RANKING_IPK
  URUTAN_MATKUL
  KELUAR
        """)
        