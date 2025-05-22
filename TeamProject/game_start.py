# game_start.py

import time
import os
import game_modes as gm 

# --- Configuration ---
GROUP_NAME = "Wave8Coders"

# --- Global Game Settings (MODIFIED!) ---
GLOBAL_GAME_DIFFICULTY_SETTING = "Medium" # Default global difficulty
# MAX_TIME_PER_QUESTION = 10.0 # REMOVED: This constant is now dynamic based on difficulty

# --- Utility Function ---
def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

# --- Initial Game Loading Screen ---
def loading_screen(duration=2, steps=20):
    clear_screen()
    print("\n\n")
    for i in range(steps + 1):
        percentage = int((i / steps) * 100)
        bar = "#" * i + "-" * (steps - i)
        
        print(f"\r[{bar}] Loading Math Fighter... {percentage}%", end="")
        print(f"\n\n\t\t{f'Developed by: {GROUP_NAME}':^40}\033[A\033[A", end="") 

        time.sleep(duration / steps)

    print("\n\n")

# --- Goodbye Loading Screen ---
def goodbye_loading_screen(duration=1.5, steps=15):
    clear_screen()
    print("\n\n")
    for i in range(steps + 1):
        percentage = int((i / steps) * 100)
        bar = "#" * i + "-" * (steps - i)
        
        print(f"\r[{bar}] Shutting Down... {percentage}%", end="")
        print(f"\n\n\t\tThank you for playing!", end="")

        time.sleep(duration / steps)
    
    print("\n\n")

# --- Main Menu Functions ---
def display_main_menu():
    clear_screen()
    print("========================================")
    print("           MATH FIGHTER GAME            ")
    print("========================================")
    print("\n")
    print("1. Normal Mode (10 Bots)")
    print("2. Endless Mode")
    print("3. Player vs Player")
    print("4. Credits")
    print("5. Options")
    print("6. Exit Game")
    print("\n")
    print("========================================")

def get_menu_choice():
    while True:
        try:
            choice = input("Enter your choice (1-6): ")
            choice = int(choice)
            if 1 <= choice <= 6:
                return choice
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# --- Game Mode Functions ---
def start_normal_pvb_game():
    gm.run_pvb_mode(mode="normal")

def start_endless_pvb_game():
    gm.run_pvb_mode(mode="endless")
    
def start_player_vs_player_game():
    clear_screen()
    print("\n--- Starting Player vs Player Game ---\n")
    print("Challenge a friend to a math duel! (Coming Soon!)")
    time.sleep(2)
    input("\nPress Enter to return to main menu...")
    clear_screen()

def show_credits():
    clear_screen()
    print("\n========================================")
    print("              CREDITS                   ")
    print("========================================")
    print(f"  Game Design & Development:            ")
    print(f"      {GROUP_NAME}                  ")
    print("  Members:                    ")
    print("    - Lester Arvid P. Anastacio     ")
    print("    - Angelo M. Quioyo              ")
    print("    - Kerwin Jan B. Catungal        ")
    print("========================================")
    input("\nPress Enter to return to main menu...")
    clear_screen()

# --- Options Menu Function ---
def show_options():
    global GLOBAL_GAME_DIFFICULTY_SETTING 
    clear_screen()
    while True:
        print("\n========================================")
        print("                OPTIONS                 ")
        print("========================================")
        print(f"  Current Difficulty: [{GLOBAL_GAME_DIFFICULTY_SETTING}]")
        print("\n  1. Set Difficulty: Easy")
        print("  2. Set Difficulty: Medium")
        print("  3. Set Difficulty: Hard")
        print("  4. Back to Main Menu")
        print("========================================")

        try:
            choice = input("Enter your choice (1-4): ")
            choice = int(choice)
            if choice == 1:
                GLOBAL_GAME_DIFFICULTY_SETTING = "Easy"
                print("Difficulty set to Easy.")
                time.sleep(1)
            elif choice == 2:
                GLOBAL_GAME_DIFFICULTY_SETTING = "Medium"
                print("Difficulty set to Medium.")
                time.sleep(1)
            elif choice == 3:
                GLOBAL_GAME_DIFFICULTY_SETTING = "Hard"
                print("Difficulty set to Hard.")
                time.sleep(1)
            elif choice == 4:
                clear_screen()
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")
            clear_screen()
        except ValueError:
            print("Invalid input. Please enter a number.")
            time.sleep(1)
            clear_screen()