from data_structures.bst import BSTMahasiswa

# buat object BST
bst = BSTMahasiswa()

# tambah mahasiswa
bst.root = bst.insert(bst.root, 98, "Aflah")
bst.root = bst.insert(bst.root, 75, "Budi")
bst.root = bst.insert(bst.root, 120, "Citra")

# cari mahasiswa
hasil = bst.search(bst.root, 98)

print("HASIL SEARCH")
print("================")

if hasil:
    print("NIM  :", hasil.nim)
    print("Nama :", hasil.nama)

# tampil inorder
print("\nDATA MAHASISWA")
print("================")

bst.inorder(bst.root)