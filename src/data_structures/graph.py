# =========================
# GRAPH PRASYARAT MATA KULIAH
# =========================

class Graph:

    def __init__(self):
        self.graph = {}

    # TAMBAH MATA KULIAH
    def tambah_matkul(self, matkul):

        if matkul not in self.graph:
            self.graph[matkul] = []

    # TAMBAH PRASYARAT
    def tambah_prasyarat(self, matkul, prasyarat):

        self.tambah_matkul(matkul)
        self.tambah_matkul(prasyarat)

        self.graph[prasyarat].append(matkul)

    # TAMPILKAN GRAPH
    def tampilkan_graph(self):

        print("GRAPH PRASYARAT MATA KULIAH")
        print("============================")

        for matkul in self.graph:
            print(matkul, "->", self.graph[matkul])

    # DFS
    def dfs(self, start, visited=None):

        if visited is None:
            visited = set()

        visited.add(start)

        print(start, end=" ")

        for tetangga in self.graph[start]:
            if tetangga not in visited:
                self.dfs(tetangga, visited)

    # BFS
    def bfs(self, start):

        visited = []
        queue = []

        visited.append(start)
        queue.append(start)

        while queue:

            s = queue.pop(0)
            print(s, end=" ")

            for tetangga in self.graph[s]:
                if tetangga not in visited:
                    visited.append(tetangga)
                    queue.append(tetangga)


# =========================
# PROGRAM UTAMA
# =========================

g = Graph()

# tambah relasi prasyarat
g.tambah_prasyarat("Struktur Data", "Algoritma")
g.tambah_prasyarat("Basis Data", "Struktur Data")
g.tambah_prasyarat("AI", "Basis Data")
g.tambah_prasyarat("Machine Learning", "AI")

# tampil graph
g.tampilkan_graph()

# DFS
print("\nDFS Traversal")
print("================")
g.dfs("Algoritma")

# BFS
print("\n\nBFS Traversal")
print("================")
g.bfs("Algoritma")