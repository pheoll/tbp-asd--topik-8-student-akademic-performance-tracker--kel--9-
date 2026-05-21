# =========================================
# NODE MAHASISWA
# =========================================

class NodeMahasiswa:

    def __init__(self, nim, nama):

        self.nim = nim
        self.nama = nama

        self.left = None
        self.right = None


# =========================================
# BST MAHASISWA
# =========================================

class BSTMahasiswa:

    def __init__(self):

        self.root = None

    # =====================================
    # INSERT
    # =====================================

    def insert(self, root, nim, nama):

        # jika kosong
        if root is None:
            return NodeMahasiswa(nim, nama)

        # masuk kiri
        if nim < root.nim:
            root.left = self.insert(root.left, nim, nama)

        # masuk kanan
        elif nim > root.nim:
            root.right = self.insert(root.right, nim, nama)

        return root

    # =====================================
    # SEARCH
    # =====================================

    def search(self, root, nim):

        # tidak ditemukan
        if root is None:
            return None

        # ditemukan
        if root.nim == nim:
            return root

        # cari kiri
        if nim < root.nim:
            return self.search(root.left, nim)

        # cari kanan
        return self.search(root.right, nim)

    # =====================================
    # INORDER
    # =====================================

    def inorder(self, root):

        if root:

            self.inorder(root.left)

            print(root.nim, "-", root.nama)

            self.inorder(root.right)