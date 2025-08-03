import copy 
from generate import*
from random import*
from dancing_links import*

def test_solu_dlx(grid):
    matrix = generate_exact_cover_matrix()
    valid_rows = valid_rows_from_grid(grid)
    # On filtre la matrice avec les lignes valides uniquement
    submatrix = [matrix[r] for r in valid_rows]

    dlx = DLX(submatrix)
    dlx.max_solutions = 2  # On s’arrête si on trouve 2 solutions

    nb_solutions = 0
    for _ in dlx.search():
        nb_solutions += 1
        if nb_solutions >= 2:
            break

    return nb_solutions



def nb_case(grid):
    ''' Compte le nombre de case remplie '''
    nb = 0
    for row in grid: # Parcours les lignes 
        for num in row: # Parcoures les chiffres de la ligne
            if num != 0:
                nb += 1
    return nb


def remove(grid, nb):
    ''' Enlève des numéros dans la grille '''
    # On ne travaille qu'avec la liste des cases qui sont remplies
    filled_case = [(x, y) for x in range(9) for y in range(9)]
    shuffle(filled_case)

    while nb_case(grid) > nb and filled_case:
        # Définie la case à enlevé 
        row, col = filled_case.pop()
        if grid[row][col] == 0:
            continue

        # On garde la valeur de la case
        val = grid[row][col]
        grid[row][col] = 0

        if test_solu_dlx(grid) != 1:
            grid[row][col] = val

    return grid
        

def ask_num_case():
    ''' Demande la difficulté '''
    val_att = ["1", "2", "3", "4"]
    mode = input("Choisissez la difficulté (1: facile, 2: moyen, 3: difficile) : ")
    while not mode in val_att:
        mode = input("Choisissez la difficulté (1: facile, 2: moyen, 3: difficile) : ")
    
    mode = int(mode)
    if mode == 1:
        num_case = 36
    elif mode == 2:
        num_case = 28
    elif mode == 3:
        num_case = 22

    return num_case  


if __name__=="__main__":
    # Définir la difficulté
    num_case = ask_num_case()

    # Générer la grille
    grid_fill = generate()
    fill_grid_recursive(grid_fill)
    print("Voici la grille complète")
    display_grid(grid_fill)
    print("-" * 25)
    
    # Retirer des cases
    grid = copy.deepcopy(grid_fill)
    print("Grille incomplète")
    display_grid(remove(grid, num_case))
    print("\nNombre de solution : ", test_solu_dlx(grid))
    print("Nombre de cases remplies : ", nb_case(grid), "\n")
    