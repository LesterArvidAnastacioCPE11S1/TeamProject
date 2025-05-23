# game_modes.py

import combat
import display_manager as dm
import time
import random

def get_difficulty_values(difficulty_setting):
    """
    Returns HP, player_damage_multiplier, and time_limit based on difficulty.
    """
    if difficulty_setting == "Easy":
        return 100, 1.2, 8 # base_hp, player_dmg_mult, time_limit
    elif difficulty_setting == "Medium":
        return 80, 1.0, 6
    elif difficulty_setting == "Hard":
        return 60, 0.8, 4
    return 80, 1.0, 6 # Default to Medium if setting is unrecognized


def run_pvb_mode(mode, difficulty_setting): # ADD difficulty_setting parameter
    """
    Manages the Player vs Bot (PvB) game mode.
    Args:
        mode (str): "normal" or "endless".
        difficulty_setting (str): "Easy", "Medium", or "Hard".
    """
    # Use the passed difficulty_setting
    base_hp, player_damage_multiplier, time_limit = get_difficulty_values(difficulty_setting)

    # Initialize player character
    player = combat.Character("Hero", base_hp)

    dm.clear_screen()
    dm.display_header(f"GAME MODE: {mode.upper()}", width=70)
    dm.display_message_box(f"Prepare for battle in {difficulty_setting} mode!", title="STARTING GAME", width=50)
    time.sleep(2)

    bot_number = 1
    total_bots = 10 if mode == "normal" else float('inf') # Endless mode

    player_wins = 0
    while player.hp > 0 and bot_number <= total_bots:
        dm.clear_screen()
        bot_name = f"Math-Bot {bot_number}"
        
        # Difficulty scaling for bots
        effective_difficulty = int((bot_number - 1) / 2) # Difficulty increases every 2 bots

        # Bot HP scales with effective difficulty
        bot_hp_scale = 1 + (effective_difficulty * 0.1) 
        bot_base_hp = 50
        bot = combat.Character(bot_name, int(bot_base_hp * bot_hp_scale))

        # Decide player HP reset logic here:
        # Option 1: Player fully heals before each bot fight (as currently implemented)
        player.reset_hp() 
        # Option 2: Player HP persists, only heal if needed (e.g., via potions or specific events)
        # if player.hp < player.max_hp: # Example: only reset if not full, or implement potions
        #    player.hp = player.max_hp

        dm.display_message_box(f"A wild {bot.name} appears!", title="NEW CHALLENGER!", width=50)
        time.sleep(1.5)

        player_defeated, bot_defeated, surrendered = combat.run_single_bot_fight(
            player, bot, effective_difficulty, player_damage_multiplier, time_limit
        )

        if surrendered:
            dm.display_message_box("You surrendered. Game over!", title="GAME OVER", width=40)
            time.sleep(1)
            break

        if player_defeated:
            dm.display_message_box(f"{player.name} has been defeated by {bot.name}!", title="GAME OVER", width=50)
            break
        elif bot_defeated:
            player_wins += 1
            dm.display_message_box(f"{bot.name} defeated! {player.name} wins!", title="VICTORY!", width=50)
            time.sleep(1.5)
            bot_number += 1
            # If it's normal mode and all bots are defeated, end the game
            if mode == "normal" and bot_number > total_bots:
                dm.display_message_box("All Math-Bots defeated! You are a Math Master!", title="CONGRATULATIONS!", width=50)
                time.sleep(2)
                break
        
    dm.clear_screen()
    if player.hp <= 0:
        dm.display_message_box(f"Game Over! You defeated {player_wins} bots.", title="GAME OVER", width=50)
    elif mode == "normal" and player_wins == total_bots:
        dm.display_message_box(f"You cleared Normal Mode, defeating {player_wins} bots!", title="GAME COMPLETE", width=50)
    else: # This path is for endless mode if the loop breaks without player defeat (e.g., external interruption)
        dm.display_message_box(f"Endless Mode ended. You defeated {player_wins} bots.", title="GAME ENDED", width=50)
    
    time.sleep(2)
    dm.clear_screen()


def run_pvp_mode():
    dm.clear_screen()
    dm.display_header("PLAYER VS PLAYER MODE", width=70)
    dm.display_message_box("Player vs Player mode is not yet fully implemented.", title="COMING SOON", width=50)
    time.sleep(2)