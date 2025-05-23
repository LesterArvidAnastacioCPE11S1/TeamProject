# main.py

import game_start as gs
import display_manager as dm
import time

def main():
    gs.loading_screen() # Call loading screen from game_start

    running = True
    while running:
        gs.display_main_menu() # Display the main menu
        choice = gs.get_menu_choice() # Get user's menu choice

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
            running = False # Set running to False to exit the loop
            gs.goodbye_loading_screen() # Call goodbye screen
            
    print("Exiting Math Fighter. Goodbye!")

if __name__ == "__main__":
    main()