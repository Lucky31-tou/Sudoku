import random

def display_grid(grid):
    ''' Afficher une grille '''
    for row in grid:
        print("  ".join(map(str, row)))


def get_col(matrice, index):
    ''' Permet d'obtenir la colonne à partir de l'indice '''
    return [row[index] for row in matrice]


def get_case(row, col, grid):
    ''' Fait une liste avec tous les chiffres d'une case '''
    list_case = []
    start_row = row // 3 * 3
    start_col = col // 3 * 3
    for i in range(3):
        for j in range(3):
            list_case.append(grid[start_row + i][start_col + j])
    return list_case



def find_empty_cell(grid):
    """
    Trouve la première case vide (valeur 0) dans la grille.
    Renvoie (row, col) ou None si la grille est pleine.
    """
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                return (r, c)
    return None


def possibilites(row, col, num, grid):
    ''' Renvoie la liste des possibilitées pour une case donnée '''
    if not num in grid[row]: # Vérifie la ligne 
        if not num in get_col(grid, col): # Vérifie la colonne 
            if not num in get_case(row, col, grid): # Vérifie la case
                return True
    return False
                

def fill_grid_recursive(grid):
    ''' Remplie la grille de manière aléatoire '''
    case = find_empty_cell(grid)
    if not case:
        return True 
    
    row, col = case

    nums = [k for k in range(1, 10)]
    random.shuffle(nums)
    
    for num in nums:
        if possibilites(row, col, num, grid):
            grid[row][col] = num

            if fill_grid_recursive(grid):
                return True
            
            grid[row][col] = 0
    
    return False 

def generate():
    ''' Générer une grille de sudoku vide '''
    grid = [[0 for k in range(9)] for k in range(9)]
    return grid


if __name__=="__main__":
    grid = generate()
    if fill_grid_recursive(grid):
        print("Grille de Sudoku générée avec succès :")
        display_grid(grid)
    else:
        print("Impossible de générer une grille.")