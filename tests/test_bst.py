import sys
import os

# =========================================
# AGAR FOLDER PROJECT TERBACA
# =========================================

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)

from src.data_structures.bst import BSTMahasiswa


# =========================================
# TEST INSERT
# =========================================

def test_insert_mahasiswa():

    bst = BSTMahasiswa()

    bst.root = bst.insert(bst.root, 98, "Aflah")

    hasil = bst.search(bst.root, 98)

    assert hasil is not None
    assert hasil.nama == "Aflah"


# =========================================
# TEST SEARCH
# =========================================

def test_search_mahasiswa():

    bst = BSTMahasiswa()

    bst.root = bst.insert(bst.root, 75, "Budi")

    hasil = bst.search(bst.root, 75)

    assert hasil.nim == 75
    assert hasil.nama == "Budi"