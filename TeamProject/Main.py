# main.py

import time
import os
import game_start as gs 

def run_game():
    """The main game loop."""
    gs.loading_screen() 

    while True:
        gs.display_main_menu() 
        choice = gs.get_menu_choice() 
        
        if choice == 1:
            gs.start_normal_pvb_game() 
        elif choice == 2:
            gs.start_endless_pvb_game() 
        elif choice == 3:
            gs.start_player_vs_player_game() 
        elif choice == 4:
            gs.show_credits()
        elif choice == 5:
            gs.show_options()
        elif choice == 6:
            gs.goodbye_loading_screen() 
            print("\nThanks for playing Math Fighter! Goodbye!")
            time.sleep(1)
            break 

# --- Start the game ---
if __name__ == "__main__":
    run_game()