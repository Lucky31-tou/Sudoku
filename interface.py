import PySimpleGUI as sg
import generate
import remove
import copy

# --- NOUVEAU ---
def get_num_cases_for_difficulty(difficulty: str) -> int:
    """
    Retourne le nombre de cases à garder pour une difficulté donnée.
    Cette fonction remplace la logique qui était dans remove.ask_num_case().
    """
    if difficulty == 'Facile':
        return 36
    elif difficulty == 'Moyen':
        return 28
    elif difficulty == 'Difficile':
        return 22
    return 28  # Par défaut sur moyen

def ask_difficulty_window():
    """
    Ouvre une fenêtre modale pour demander à l'utilisateur de choisir la difficulté.
    Retourne la difficulté choisie ('Facile', 'Moyen', etc.) ou None si annulé.
    """
    layout = [
        [sg.Text("Choisissez votre niveau de difficulté", font=('Helvetica', 12))],
        [sg.Button('Facile', size=(10, 2)), sg.Button('Moyen', size=(10, 2)), sg.Button('Difficile', size=(10, 2))],
        [sg.Button('Annuler', size=(10, 1))]
    ]
    # modal=True bloque l'interaction avec la fenêtre principale tant que celle-ci est ouverte.
    window = sg.Window('Difficulté', layout, modal=True, element_justification='center')
    
    event, values = window.read()
    window.close()
    
    return event if event not in (sg.WIN_CLOSED, 'Annuler') else None
# --- FIN NOUVEAU ---

def main():
    sg.theme("DarkBlue3")
    GRID_SIZE = 9

    solution_grid = None
    puzzle_grid = None

    # --- MODIFIÉ : Création de la grille avec des espacements pour les blocs 3x3 ---
    grid_layout = []
    for row in range(GRID_SIZE):
        line = []
        for col in range(GRID_SIZE):
            # Calcule l'espacement pour créer des blocs visuels
            pad_left = 8 if col % 3 == 0 and col != 0 else 2
            pad_top = 8 if row % 3 == 0 and row != 0 else 2
            line.append(sg.Input(
                size=(3, 2), font=('Helvetica', 20), justification='center',
                key=(row, col), text_color='white', disabled=True,
                # Le pad est défini comme ((gauche, droite), (haut, bas))
                pad=((pad_left, 2), (pad_top, 2))
            ))
        grid_layout.append(line)
    # --- FIN MODIFICATION ---

    # Boutons
    controls_layout = [
        sg.Button("Nouvelle Partie", key="-NEW-", font=("Helvetica", 12)),
        sg.Button("Vérifier", key="-CHECK-", font=("Helvetica", 12), disabled=True),
        sg.Button("Quitter", font=("Helvetica", 12))
    ]

    # Mise en page
    layout = [
        [sg.Frame('Sudoku', grid_layout, element_justification='center')],
        # On place les boutons dans une colonne pour pouvoir les centrer ensemble
        [sg.Column([controls_layout], element_justification='center')]
    ]

    # Créer la fenêtre
    # Il est préférable d'ajouter finalize=True pour pouvoir utiliser .update()
    # de manière fiable avant même le premier .read()
    window = sg.Window("Sudoku", layout, finalize=True)

    while True:
        event, values = window.read() # Attend une action de l'utilisateur

        # Si Quitter est cliqué 
        if event == sg.WIN_CLOSED or event == "Quitter":
            break

        # Si -NEW- est cliqué
        if event == "-NEW-":
            # Demander la difficulté via la nouvelle fenêtre
            difficulty = ask_difficulty_window()
            if not difficulty: # Si l'utilisateur a cliqué sur Annuler ou fermé la fenêtre
                continue

            num_cases_to_keep = get_num_cases_for_difficulty(difficulty)

            # Générer la grille
            grid_full = generate.generate()
            generate.fill_grid_recursive(grid_full)

            solution_grid = copy.deepcopy(grid_full)

            puzzle_grid = remove.remove(copy.deepcopy(grid_full), num_cases_to_keep)

            # Mettre à jour l'interface graphique
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    cell_value = puzzle_grid[r][c]
                    input_element = window[(r, c)]

                    window[(r, c)].Widget.config(insertbackground='black')

                    if cell_value != 0:
                        input_element.update(
                            value=cell_value,
                            disabled=True,
                            text_color="red"  # Chiffres du puzzle en bleu clair
                        )
                    else:
                        input_element.update(
                            value='',
                            disabled=False,
                            text_color="black"  # Texte de l'utilisateur en blanc
                        )
            # Activation du bouton vérifier
            window["-CHECK-"].update(disabled=False)

        # Si CHECK est cliqué
        elif event == "-CHECK-":
            if solution_grid is None:
                continue # Sécurité

            has_errors = False
            is_complete = True

            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE):
                    user_val_str = values[(i, j)]

                    # Si une case est vide
                    if not user_val_str:
                        is_complete = False
                        continue
                
                    try:
                        user_val_str = int(user_val_str)
                        if user_val_str != solution_grid[i][j]:
                            has_errors = True
                    except ValueError:
                        # Si il ne s'agit pas d'un chiffre
                        has_errors = True

            # On affiche le résultat
            if has_errors:
                sg.popup("Il y a des erreurs dans votre grille. Essayez de les corriger.", title="Erreur")
            elif not is_complete:
                sg.popup("Aucune erreur trouvée pour l'instant, mais la grille n'est pas complète. Continuez !", title="Info")
            else: # Si pas d'erreur et grille complète
                sg.popup("Félicitations ! Vous avez résolu le Sudoku !", title="Gagné !")
    # Fermer la fenêtre
    window.close()


if __name__=="__main__":
    main()