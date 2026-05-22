from typing import List
from modules.modul2 import ModulBST

class ModulRanking:
    """Modul 5 - Ranking & Sorting IPK menggunakan Merge Sort"""
    
    def __init__(self, modul_bst: ModulBST):
        self.modul_bst = modul_bst

    def merge_sort_ipk(self, mahasiswa_list: List) -> List:
        """Merge Sort berdasarkan IPK (descending)"""
        if len(mahasiswa_list) <= 1:
            return mahasiswa_list
        
        mid = len(mahasiswa_list) // 2
        left = self.merge_sort_ipk(mahasiswa_list[:mid])
        right = self.merge_sort_ipk(mahasiswa_list[mid:])
        
        return self._merge(left, right)

    def _merge(self, left: List, right: List) -> List:
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            ipk_left = getattr(left[i], 'ipk', 0.0)
            ipk_right = getattr(right[j], 'ipk', 0.0)
            
            if ipk_left >= ipk_right:   # descending
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
                
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def ranking_ipk(self, top_n: int = 10) -> List:
        """Mengembalikan ranking IPK tertinggi"""
        semua_mhs = self.modul_bst.daftar_semua_mahasiswa()
        sorted_mhs = self.merge_sort_ipk(semua_mhs)
        return sorted_mhs[:top_n]

    def distribusi_ipk(self) -> dict:
        """Distribusi IPK sederhana"""
        semua_mhs = self.modul_bst.daftar_semua_mahasiswa()
        ranges = {"4.0+": 0, "3.5-3.99": 0, "3.0-3.49": 0, "2.5-2.99": 0, "<2.5": 0}
        
        for mhs in semua_mhs:
            ipk = getattr(mhs, 'ipk', 0.0)
            if ipk >= 4.0:
                ranges["4.0+"] += 1
            elif ipk >= 3.5:
                ranges["3.5-3.99"] += 1
            elif ipk >= 3.0:
                ranges["3.0-3.49"] += 1
            elif ipk >= 2.5:
                ranges["2.5-2.99"] += 1
            else:
                ranges["<2.5"] += 1
        return ranges