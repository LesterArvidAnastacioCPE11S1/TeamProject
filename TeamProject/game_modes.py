# game_modes.py

import time
import os
import game_start as gs 
import combat as cl

# --- Constants for Game Mode Logic ---
BASE_PLAYER_STARTING_HP = 100 

BOT_STARTING_HP_NORMAL_MODE = 50 
BOT_HP_INCREASE_NORMAL_MODE = 25
NORMAL_MODE_BOT_COUNT = 10 

BOT_STARTING_HP_ENDLESS_MODE = 80 
BOT_HP_INCREASE_ENDLESS_MODE = 10 
BOT_DIFFICULTY_ADVANCE_RATE_ENDLESS = 3 

BOSS_STAGE_INTERVAL = 10 
PLAYER_PERMANENT_HP_GAIN_PER_BOSS = 100 # NEW: Permanent HP gain for player

# --- Helper function to get global difficulty modifiers ---
def get_global_difficulty_modifiers():
    """
    Returns a dictionary of modifiers based on the global difficulty setting.
    - hp_multiplier: Multiplies base player HP.
    - player_damage_multiplier: Multiplies player's calculated damage.
    - question_difficulty_offset: Adds to the problem's base difficulty.
    - time_limit: The maximum time allowed per question.
    """
    if gs.GLOBAL_GAME_DIFFICULTY_SETTING == "Easy":
        return {"hp_multiplier": 1.5, "player_damage_multiplier": 1.2, "question_difficulty_offset": -2, "time_limit": 15.0} 
    elif gs.GLOBAL_GAME_DIFFICULTY_SETTING == "Medium":
        return {"hp_multiplier": 1.0, "player_damage_multiplier": 1.0, "question_difficulty_offset": 0, "time_limit": 10.0} 
    elif gs.GLOBAL_GAME_DIFFICULTY_SETTING == "Hard":
        return {"hp_multiplier": 0.5, "player_damage_multiplier": 0.8, "question_difficulty_offset": 2, "time_limit": 5.0} 

# --- Function to run Normal Mode ---
def run_normal_pvb_mode():
    modifiers = get_global_difficulty_modifiers()
    player_starting_hp = int(BASE_PLAYER_STARTING_HP * modifiers["hp_multiplier"])
    player = cl.Character("Hero", player_starting_hp)
    global_question_offset = modifiers["question_difficulty_offset"]
    player_damage_multiplier = modifiers["player_damage_multiplier"]
    current_time_limit = modifiers["time_limit"] 

    player_wins = 0
    surrendered_overall = False

    cl.clear_screen()
    print("\n" * 3)
    print(f"You must defeat {NORMAL_MODE_BOT_COUNT} Math-Bots!".center(40))
    time.sleep(2)

    for bot_number_in_normal_mode in range(NORMAL_MODE_BOT_COUNT): 
        if surrendered_overall or player.is_defeated():
            break

        is_boss_stage = (bot_number_in_normal_mode + 1) % BOSS_STAGE_INTERVAL == 0 
        
        scaling_difficulty_level = bot_number_in_normal_mode // 2 
        effective_difficulty = scaling_difficulty_level + global_question_offset
        effective_difficulty = max(0, effective_difficulty)

        if is_boss_stage:
            # Normal Mode bosses don't scale HP/Shield like Endless Mode bosses
            # They use their base BOSS_HEALTH and BOSS_SHIELD
            target = cl.Boss(f"OMEGA BOT", effective_difficulty, scaling_factor=1) 
            print("\n" * 3)
            print("!!! A POWERFUL FOE APPROACHES !!!".center(40))
            time.sleep(1)
        else:
            current_bot_hp = BOT_STARTING_HP_NORMAL_MODE + (bot_number_in_normal_mode * BOT_HP_INCREASE_NORMAL_MODE)
            target = cl.Character(f"Math-Bot {bot_number_in_normal_mode + 1}", current_bot_hp)
        
        cl.clear_screen()
        print(f"\n--- Challenger {bot_number_in_normal_mode + 1} of {NORMAL_MODE_BOT_COUNT}: {target.name}! ---".center(40)) 
        player.display_status()
        target.display_status() 
        print(f"Difficulty Level: {effective_difficulty}".center(40))
        print(f"Time Limit per question: {current_time_limit:.0f} seconds".center(40)) 
        print("\n(Type 'surrender' at any answer prompt to give up)".center(40))
        time.sleep(2)
        cl.clear_screen()

        player_defeated_in_fight, target_defeated_in_fight, surrendered_this_fight = \
            cl.run_single_bot_fight(player, target, effective_difficulty, player_damage_multiplier, current_time_limit) 

        if surrendered_this_fight:
            surrendered_overall = True
            player.hp = 0
            break

        if player_defeated_in_fight:
            break

        if target_defeated_in_fight: 
            cl.clear_screen()
            print("\n" * 3)
            print("  $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print("  $                                       $")
            if is_boss_stage:
                print("  $          BOSS DEFEATED!               $")
            else:
                print("  $          BOT DEFEATED!                $")
            print(f"  $        {target.name} CRUSHED!             $") 
            print("  $                                       $")
            print("  $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print(f"\n{player.name} defeated {target.name}!")
            player_wins += 1
            player.reset_hp() # Player HP restored to current max_hp (which is fixed in normal mode)
            print(f"\n{player.name} HP restored to {player.hp}!")
            time.sleep(3)

    return player_wins, player.is_defeated(), surrendered_overall

# --- Function to run Endless Mode (MODIFIED!) ---
def run_endless_pvb_mode():
    modifiers = get_global_difficulty_modifiers()
    player_starting_hp = int(BASE_PLAYER_STARTING_HP * modifiers["hp_multiplier"])
    player = cl.Character("Hero", player_starting_hp)
    global_question_offset = modifiers["question_difficulty_offset"]
    player_damage_multiplier = modifiers["player_damage_multiplier"]
    current_time_limit = modifiers["time_limit"] 

    player_wins = 0
    surrendered_overall = False

    while not player.is_defeated() and not surrendered_overall:
        is_boss_stage = (player_wins + 1) % BOSS_STAGE_INTERVAL == 0 and player_wins >= 0 
        
        scaling_difficulty_level = player_wins // BOT_DIFFICULTY_ADVANCE_RATE_ENDLESS
        effective_difficulty = scaling_difficulty_level + global_question_offset
        effective_difficulty = max(0, effective_difficulty)

        boss_scaling_factor = 1 # Default for regular bots or first boss
        if is_boss_stage:
            boss_number = (player_wins + 1) // BOSS_STAGE_INTERVAL # 1 for stage 10, 2 for stage 20 etc.
            boss_scaling_factor = boss_number # Example: 1x, 2x, 3x for bosses at stages 10, 20, 30
            
            target = cl.Boss(f"VOID LORD", effective_difficulty, boss_scaling_factor) # Pass scaling factor
            cl.clear_screen()
            print("\n" * 3)
            print("!!! A POWERFUL FOE APPROACHES !!!".center(40))
            time.sleep(1)
        else:
            current_bot_hp = BOT_STARTING_HP_ENDLESS_MODE + (player_wins * BOT_HP_INCREASE_ENDLESS_MODE)
            target = cl.Character(f"Math-Bot {player_wins + 1}", current_bot_hp)

        cl.clear_screen()
        print(f"\n--- Next Challenger: {target.name}! ---".center(40)) 
        player.display_status()
        target.display_status() 
        print(f"Your Wins: {player_wins}".center(40))
        print(f"Difficulty Level: {effective_difficulty}".center(40))
        print(f"Time Limit per question: {current_time_limit:.0f} seconds".center(40)) 
        print("\n(Type 'surrender' at any answer prompt to give up)".center(40))
        time.sleep(2)
        cl.clear_screen()

        player_defeated_in_fight, target_defeated_in_fight, surrendered_this_fight = \
            cl.run_single_bot_fight(player, target, effective_difficulty, player_damage_multiplier, current_time_limit) 

        if surrendered_this_fight:
            surrendered_overall = True
            player.hp = 0
            break
        
        if player_defeated_in_fight:
            break

        if target_defeated_in_fight: 
            cl.clear_screen()
            print("\n" * 3)
            print("  $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print("  $                                       $")
            if is_boss_stage:
                print("  $          BOSS DEFEATED!               $")
                # NEW: Permanent HP gain for player after defeating a boss in Endless Mode
                player.max_hp += PLAYER_PERMANENT_HP_GAIN_PER_BOSS
                print(f"  $        {player.name} GAINED +{PLAYER_PERMANENT_HP_GAIN_PER_BOSS} MAX HP!     $")
            else:
                print("  $          BOT DEFEATED!                $")
            print(f"  $        {target.name} CRUSHED!             $") 
            print("  $                                       $")
            print("  $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print(f"\n{player.name} defeated {target.name}!")
            player_wins += 1
            player.reset_hp() # This now resets to the new, potentially higher max_hp
            print(f"\n{player.name} HP restored to {player.hp}/{player.max_hp}!")
            time.sleep(3)

    return player_wins, player.is_defeated(), surrendered_overall

# --- Main Player vs Bot Game Logic (Dispatcher) ---
def run_pvb_mode(mode="normal"):
    cl.clear_screen()
    print(f"\n--- Player vs Bot: {'Normal Mode' if mode == 'normal' else 'Endless Mode'} ---")
    print(f"--- Global Difficulty: {gs.GLOBAL_GAME_DIFFICULTY_SETTING} ---\n")
    time.sleep(1)

    cl.game_ready_start_countdown()

    player_wins = 0
    player_defeated = False
    surrendered = False
    
    if mode == "normal":
        player_wins, player_defeated, surrendered = run_normal_pvb_mode()
    elif mode == "endless":
        player_wins, player_defeated, surrendered = run_endless_pvb_mode()

    if player_defeated:
        cl.clear_screen()
        print("\n" * 3)
        print("  $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print("  $                                       $")
        if surrendered:
            print("  $          GAME OVER! YOU SURRENDERED.  $")
        else:
            print("  $          GAME OVER! YOU LOST.         $")
        print("  $                                       $")
        print("  $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(f"\nYou fought {player_wins} Math-Bots before your defeat.")
        time.sleep(3)
    elif not player_defeated and mode == "normal":
        cl.clear_screen()
        print("\n" * 3)
        print("  $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print("  $                                       $")
        print("  $        NORMAL MODE COMPLETE!          $")
        print("  $  You are the ultimate Math Fighter!   $")
        print("  $                                       $")
        print("  $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(f"\nYou defeated all {NORMAL_MODE_BOT_COUNT} Math-Bots (including the BOSS!)!")
        time.sleep(3)

    input("\nPress Enter to return to main menu...")
    cl.clear_screen()