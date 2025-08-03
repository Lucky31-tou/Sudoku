def constraint_indices(row, col, digit):
    ''' Calcule les 4 indices pour chaques contraintes '''
    case = 9*row + col
    ligne = 81 + 9*row + digit
    colonne = 162 + 9*col + digit
    block = 243 + 9*((row//3)*3 + (col//3)) + digit
    return [case, ligne, colonne, block]

def generate_exact_cover_matrix():
    ''' Génère toutes les lignes de la matrice '''
    matrix = []
    for row in range(9):
        for col in range(9):
            for digit in range(9):
                line = constraint_indices(row, col, digit)
                matrix.append(line)
    return matrix

def valid_rows_from_grid(grid):
    '''
    À partir d'une grille 9x9 avec des entiers de 0 (vide) à 9,
    retourne les indices des lignes valides dans la matrice.
    '''
    valid_rows = []
    for row in range(9):
        for col in range(9):
            val = grid[row][col]
            if val == 0:
                # case vide : on garde toutes les lignes possibles
                for digit in range(9):
                    valid_rows.append((row * 81) + (col * 9) + digit)
            else:
                # case remplie : on garde uniquement le placement imposé
                digit = val - 1
                valid_rows.append((row * 81) + (col * 9) + digit)
    return valid_rows



class DLXNode:
    def __init__(self):
        self.left = self.right = self.up = self.down = self
        self.column = None
        self.row_id = None
        self.col_id = None
        self.size = 0

class DLX:
    def __init__(self, matrix):
        self.header = DLXNode()
        self.columns = []
        self.solution = []
        self.build(matrix)
        self.nb_solutions = 0
        self.max_solutions = 2  # On s’arrête dès qu’on trouve 2 solutions

    def build(self, matrix):
        n_cols = 324  # Pour le sudoku standard 9x9
        self.columns = [DLXNode() for _ in range(n_cols)]
        # Chaînage horizontal des colonnes
        prev = self.header
        for i, col in enumerate(self.columns):
            col.col_id = i
            col.size = 0
            col.left = prev
            prev.right = col
            prev = col
            # Chaînage vertical init
            col.up = col.down = col
        prev.right = self.header
        self.header.left = prev

        # Ajout des lignes
        for r, cols in enumerate(matrix):
            first = None
            for c in cols:
                col = self.columns[c]
                node = DLXNode()
                node.column = col
                node.row_id = r
                node.col_id = c
                # insertion verticale
                node.down = col
                node.up = col.up
                col.up.down = node
                col.up = node
                col.size += 1
                # insertion horizontale
                if first is None:
                    first = node
                    node.left = node.right = node
                else:
                    node.left = first.left
                    node.right = first
                    first.left.right = node
                    first.left = node

    def cover(self, col):
        col.right.left = col.left
        col.left.right = col.right
        i = col.down
        while i != col:
            j = i.right
            while j != i:
                j.down.up = j.up
                j.up.down = j.down
                j.column.size -= 1
                j = j.right
            i = i.down

    def uncover(self, col):
        i = col.up
        while i != col:
            j = i.left
            while j != i:
                j.column.size += 1
                j.down.up = j
                j.up.down = j
                j = j.left
            i = i.up
        col.right.left = col
        col.left.right = col

    def search(self, k=0):
        if self.header.right == self.header:
            self.nb_solutions += 1
            yield list(self.solution)
            if self.nb_solutions >= self.max_solutions:
                return
        else:
            # Choisir la colonne la plus petite (plus contraignante)
            col = self.header.right
            c = col.right
            while c != self.header:
                if c.size < col.size:
                    col = c
                c = c.right
            if col.size == 0:
                return

            self.cover(col)
            r = col.down
            while r != col:
                self.solution.append(r.row_id)
                j = r.right
                while j != r:
                    self.cover(j.column)
                    j = j.right
                yield from self.search(k + 1)
                j = r.left
                while j != r:
                    self.uncover(j.column)
                    j = j.left
                self.solution.pop()
                r = r.down
            self.uncover(col)
