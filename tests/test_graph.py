from src.data_structures.graph import GraphPrereq
from data_structures.doubly_linked_list import GRADE_MAP

def test_graph_prereq():
    graph = GraphPrereq()
    
    # Tambah matakuliah
    graph.tambah_matkul("ELT101", "Kalkulus")
    graph.tambah_matkul("ELT102", "Fisika")
    graph.tambah_matkul("ELT201", "Elektronika")
    
    # Tambah prasyarat
    graph.tambah_prasyarat("ELT201", "ELT101")  # ELT101 prasyarat ELT201
    graph.tambah_prasyarat("ELT201", "ELT102")
    
    # Topological Sort
    urutan = graph.topological_sort()
    assert len(urutan) > 0  # Harus ada urutan valid
    
    print("Topological Sort:", urutan)
    