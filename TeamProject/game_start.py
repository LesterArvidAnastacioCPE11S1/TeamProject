# game_start.py

import time
import os
import sys
import game_modes as gm
import display_manager as dm

# --- Configuration ---
GROUP_NAME = "Wave8Coders"

# --- Global Game Settings ---
GLOBAL_GAME_DIFFICULTY_SETTING = "Medium" # Default global difficulty

# --- Initial Game Loading Screen ---
def loading_screen(duration=2, steps=20):
    dm.clear_screen()
    
    message_lines = [
        "Loading Math Fighter...",
        "",
        f"Developed by: {GROUP_NAME}"
    ]
    
    box_total_width = dm.draw_box(message_lines, padding_x=2, padding_y=1, fixed_width=40)
    
    left_offset = dm.get_centered_left_padding(box_total_width)

    sys.stdout.write("\n")
    sys.stdout.flush()

    for i in range(steps + 1):
        percentage = int((i / steps) * 100)
        bar_len = box_total_width - 8
        bar = "#" * int(i * bar_len / steps) + "-" * (bar_len - int(i * bar_len / steps))
        bar = bar[:bar_len].ljust(bar_len, '-')

        bar_string = f"[{bar}] {percentage}%"
        
        final_bar_output = " " * left_offset + dm.center_text(bar_string, target_width=box_total_width)
        
        sys.stdout.write(f"\r{final_bar_output}")
        sys.stdout.flush()

        time.sleep(duration / steps)

    sys.stdout.write("\n\n")
    sys.stdout.flush()
    time.sleep(0.5)
    dm.clear_screen()

# --- Goodbye Loading Screen ---
def goodbye_loading_screen(duration=1.5, steps=15):
    dm.clear_screen()
    
    message_lines = [
        "Shutting Down...",
        "",
        "Thank you for playing!"
    ]

    box_total_width = dm.draw_box(message_lines, padding_x=2, padding_y=1, fixed_width=40)

    left_offset = dm.get_centered_left_padding(box_total_width)

    sys.stdout.write("\n")
    sys.stdout.flush()

    for i in range(steps + 1):
        percentage = int((i / steps) * 100)
        bar_len = box_total_width - 8
        bar = "#" * int(i * bar_len / steps) + "-" * (bar_len - int(i * bar_len / steps))
        bar = bar[:bar_len].ljust(bar_len, '-')

        bar_string = f"[{bar}] {percentage}%"
        final_bar_output = " " * left_offset + dm.center_text(bar_string, target_width=box_total_width)
        
        sys.stdout.write(f"\r{final_bar_output}")
        sys.stdout.flush()

        time.sleep(duration / steps)
    
    sys.stdout.write("\n\n")
    sys.stdout.flush()
    time.sleep(0.5)
    dm.clear_screen()

# --- Main Menu Functions ---
def display_main_menu():
    dm.clear_screen()
    menu_options = [
        "1. Normal Mode (10 Bots)",
        "2. Endless Mode",
        "3. Player vs Player",
        "4. Credits",
        "5. Options",
        "6. Exit Game"
    ]
    # This width is captured but not directly used by game_modes, so no issue here.
    MAIN_MENU_BOX_WIDTH = dm.draw_box(menu_options, title="MATH FIGHTER GAME", padding_x=6, padding_y=1, fixed_width=40)

def get_menu_choice():
    while True:
        try:
            prompt_box_width = 40 
            # Use the new dm.get_input_in_box, passing empty string for box_title
            choice_input = dm.get_input_in_box("Enter your choice (1-6): ", box_title="", box_width=prompt_box_width, padding_y=0)

            choice = int(choice_input)
            if 1 <= choice <= 6:
                return choice
            else:
                dm.display_message_box("Invalid choice. Please enter a number between 1 and 6.", title="INVALID INPUT", width=prompt_box_width)
                time.sleep(1.5)
                dm.clear_screen()
                display_main_menu() # Re-display menu after error
        except ValueError:
            dm.display_message_box("Invalid input. Please enter a number.", title="INPUT ERROR", width=prompt_box_width)
            time.sleep(1.5)
            dm.clear_screen()
            display_main_menu() # Re-display menu after error

# --- Game Mode Functions ---
def start_normal_pvb_game():
    global GLOBAL_GAME_DIFFICULTY_SETTING # Declare intent to use global variable
    gm.run_pvb_mode(mode="normal", difficulty_setting=GLOBAL_GAME_DIFFICULTY_SETTING)

def start_endless_pvb_game():
    global GLOBAL_GAME_DIFFICULTY_SETTING # Declare intent to use global variable
    gm.run_pvb_mode(mode="endless", difficulty_setting=GLOBAL_GAME_DIFFICULTY_SETTING)
    
def start_player_vs_player_game():
    dm.clear_screen()
    message = "Player vs Player - Under Construction!\nCheck back in a future update!"
    dm.display_message_box(message, title="WORK IN PROGRESS", width=50)
    time.sleep(2)
    dm.clear_screen()

def show_credits():
    dm.clear_screen()
    credits_lines = [
        "Game Design & Development:",
        "",
        f"        {GROUP_NAME}",
        "",
        "Members:",
        "  - Lester Arvid P. Anastacio",
        "  - Angelo M. Quioyo",
        "  - Kerwin Jan B. Catungal"
    ]
    credits_box_width = dm.draw_box(credits_lines, title="CREDITS", padding_x=4, padding_y=1, fixed_width=40)
    
    prompt_box_width = 40
    # Use the new dm.get_input_in_box, passing empty string for box_title
    dm.get_input_in_box("Press Enter to return to main menu...", box_title="", box_width=prompt_box_width, padding_y=0)
    dm.clear_screen()

# --- Options Menu Function ---
def show_options():
    global GLOBAL_GAME_DIFFICULTY_SETTING # Declare intent to modify global variable
    dm.clear_screen()
    while True:
        options_content = [
            f"Current Difficulty: [{GLOBAL_GAME_DIFFICULTY_SETTING}]",
            "",
            "1. Set Difficulty: Easy",
            "2. Set Difficulty: Medium",
            "3. Set Difficulty: Hard",
            "4. Back to Main Menu"
        ]
        options_box_width = dm.draw_box(options_content, title="OPTIONS", padding_x=4, padding_y=1, fixed_width=40)

        prompt_box_width = 40
        # Use the new dm.get_input_in_box, passing empty string for box_title
        choice_input = dm.get_input_in_box("Enter your choice (1-4): ", box_title="", box_width=prompt_box_width, padding_y=0)

        try:
            choice = int(choice_input)
            if choice == 1:
                GLOBAL_GAME_DIFFICULTY_SETTING = "Easy"
                dm.display_message_box("Difficulty set to Easy.", title="SETTING CHANGED", width=40)
                time.sleep(1)
            elif choice == 2:
                GLOBAL_GAME_DIFFICULTY_SETTING = "Medium"
                dm.display_message_box("Difficulty set to Medium.", title="SETTING CHANGED", width=40)
                time.sleep(1)
            elif choice == 3:
                GLOBAL_GAME_DIFFICULTY_SETTING = "Hard"
                dm.display_message_box("Difficulty set to Hard.", title="SETTING CHANGED", width=40)
                time.sleep(1)
            elif choice == 4:
                dm.clear_screen()
                break
            else:
                dm.display_message_box("Invalid choice. Please enter a number between 1 and 4.", title="INVALID INPUT", width=40)
                time.sleep(1.5)
            dm.clear_screen()
        except ValueError:
            dm.display_message_box("Invalid input. Please enter a number.", title="INPUT ERROR", width=40)
            time.sleep(1.5)
            dm.clear_screen()