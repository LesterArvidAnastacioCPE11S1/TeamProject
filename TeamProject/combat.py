# combat.py

import time
import random
import os
import sys
import display_manager as dm

# --- Constants for Game Mechanics ---
MIN_DAMAGE_BONUS_TIME = 2.0
BASE_PLAYER_DAMAGE = 10
BONUS_DAMAGE_PER_SECOND = 5

SHIELD_BONUS_AMOUNT = 10
SHIELD_MIN_TIME = 0.5
SHIELD_MAX_TIME = 3.0

# Boss specific constants (These are BASE values now)
BOSS_BASE_HEALTH = 500
BOSS_BASE_SHIELD = 200

# --- Math Problem Generation Helper Functions ---
def _generate_addition_problem(effective_difficulty):
    """Generates an addition problem."""
    num1_max = 10 + effective_difficulty * 5
    num2_max = 10 + effective_difficulty * 5
    num1 = random.randint(1, num1_max)
    num2 = random.randint(1, num2_max)
    return f"What is {num1} + {num2}? ", num1 + num2

def _generate_subtraction_problem(effective_difficulty):
    """Generates a subtraction problem."""
    num1_max = 20 + effective_difficulty * 5
    num2_max = 10 + effective_difficulty * 3
    temp_num1 = random.randint(1, num1_max)
    temp_num2 = random.randint(1, temp_num1) # Ensure num1 >= num2 for positive result
    num1 = max(temp_num1, temp_num2)
    num2 = min(temp_num1, temp_num2)
    return f"What is {num1} - {num2}? ", num1 - num2

def _generate_multiplication_problem(effective_difficulty):
    """Generates a multiplication problem."""
    factor_max_base = 10
    factor_max_scaling = 3
    max_factor = min(factor_max_base + effective_difficulty * factor_max_scaling, 50)

    num1 = random.randint(1, max_factor)
    num2 = random.randint(1, max_factor)

    if effective_difficulty < 2:
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
    elif effective_difficulty < 4:
        num1 = random.randint(1, 15)
        num2 = random.randint(1, 15)
    return f"What is {num1} * {num2}? ", num1 * num2

def _generate_division_problem(effective_difficulty):
    """Generates a division problem ensuring integer results."""
    divisor_min = 2
    divisor_max_base = 5
    divisor_max_scaling = 1
    max_divisor = min(divisor_max_base + effective_difficulty * divisor_max_scaling, 25)

    num2 = random.randint(divisor_min, max_divisor)

    quotient_min = 1
    quotient_max_base = 10
    quotient_max_scaling = 2
    max_quotient = min(quotient_min + effective_difficulty * quotient_max_scaling, 50)

    num1 = num2 * random.randint(quotient_min, max_quotient)
    return f"What is {num1} / {num2}? ", int(num1 / num2)

def generate_math_problem(effective_difficulty):
    """
    Generates a single-operation math problem based on the effective difficulty level.
    """
    operators = ["+"]
    if effective_difficulty >= 1:
        operators.extend(["-", "*"])
    if effective_difficulty >= 3:
        operators.append("/")

    operator = random.choice(operators)

    if operator == "+":
        return _generate_addition_problem(effective_difficulty)
    elif operator == "-":
        return _generate_subtraction_problem(effective_difficulty)
    elif operator == "*":
        return _generate_multiplication_problem(effective_difficulty)
    elif operator == "/":
        return _generate_division_problem(effective_difficulty)

# --- Boss Question Generation ---
def generate_boss_problem(effective_difficulty):
    """
    Generates a multi-operation math problem for boss fights.
    Uses +, -, * and sometimes / (ensuring integer results).
    """
    operators_pool = ["+", "-", "*"]
    if effective_difficulty >= 5:
        operators_pool.append("/")

    num_ops = 2
    if effective_difficulty >= 7:
        num_ops = 3

    parts = []
    first_num_max = 50 + effective_difficulty * 10
    parts.append(str(random.randint(10, first_num_max)))

    for i in range(num_ops):
        operator = random.choice(operators_pool)
        next_num_max = 20 + effective_difficulty * 3
        next_num = random.randint(1, next_num_max)
        parts.append(operator)
        parts.append(str(next_num))

    problem_string = " ".join(parts)

    try:
        correct_answer = eval(problem_string)
        correct_answer = int(correct_answer)
    except Exception as e:
        print(f"Error evaluating boss problem '{problem_string}': {e}. Retrying problem generation.")
        return generate_boss_problem(effective_difficulty)

    return problem_string + "? ", correct_answer

def get_player_input_answer_timed(prompt_text, input_box_width, allow_string_input=False):
    """
    Prompts the player for an answer and measures the time taken.
    The prompt is displayed inside a box, and the input cursor is placed inside it.
    Returns (player_answer_or_command_string, time_taken).
    """
    start_time = time.time()
    
    while True:
        # Call get_input_in_box with an empty box_title for a single-line prompt
        player_input = dm.get_input_in_box(prompt_text, box_title="", box_width=input_box_width, padding_x=2, padding_y=0)

        end_time = time.time()
        time_taken = end_time - start_time

        if player_input.lower() == "surrender":
            return "SURRENDER", time_taken
        
        if allow_string_input:
            return player_input.lower(), time_taken
        
        # Check if input is a digit or can be converted to int (handles negative numbers)
        if player_input.lstrip('-').isdigit():
            player_answer = int(player_input)
            return player_answer, time_taken
        else:
            dm.display_message_box("Invalid input. Please enter a whole number or 'surrender'.", title="INPUT ERROR", width=input_box_width)
            time.sleep(1.5)
            dm.clear_screen()
            # Note: The original start_time is maintained to reflect the total time spent trying to input.


def calculate_damage(time_taken, player_damage_multiplier, current_time_limit):
    """
    Calculates damage based on time taken to answer, a damage multiplier,
    and the specific time limit for the current difficulty.
    """
    effective_time = min(time_taken, current_time_limit)

    time_bonus_factor = max(0, (current_time_limit - effective_time) / (current_time_limit - MIN_DAMAGE_BONUS_TIME))
    time_bonus_factor = max(0, min(1, time_bonus_factor))

    bonus_damage = int(time_bonus_factor * (BONUS_DAMAGE_PER_SECOND * (current_time_limit - MIN_DAMAGE_BONUS_TIME)))

    total_damage = (BASE_PLAYER_DAMAGE + bonus_damage) * player_damage_multiplier
    return int(total_damage)

def check_answer(player_answer, correct_answer):
    """Checks if the player's answer is correct."""
    return player_answer == correct_answer

# --- Player and Bot Stats ---
class Character:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.shield_hp = 0

    def take_damage(self, damage):
        if self.shield_hp > 0:
            if damage <= self.shield_hp:
                self.shield_hp -= damage
                damage = 0
            else:
                damage -= self.shield_hp
                self.shield_hp = 0

        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def is_defeated(self):
        return self.hp <= 0

    def reset_hp(self):
        self.hp = self.max_hp
        self.shield_hp = 0 # Reset shield on full HP reset

    def display_status(self):
        status_lines = [
            f"HP: {self.hp}/{self.max_hp}",
        ]
        if self.shield_hp > 0:
            status_lines.append(f"Shield: {self.shield_hp}")
        
        title = f"{self.name.upper()} STATUS"
        if "Math-Bot" in self.name:
            title = f"BOT STATUS ({self.name.split(' ')[-1]})"
        elif "OMEGA BOT" in self.name or "VOID LORD" in self.name:
            title = f"BOSS STATUS ({self.name})"
        elif self.name == "Hero":
            title = "PLAYER STATUS"

        # Fixed width for status boxes for consistent alignment
        dm.draw_box(status_lines, title=title, padding_x=4, padding_y=0, fixed_width=30)


class Boss(Character):
    def __init__(self, name, effective_difficulty=0, scaling_factor=1):
        scaled_hp = int(BOSS_BASE_HEALTH * scaling_factor)
        scaled_shield = int(BOSS_BASE_SHIELD * scaling_factor)

        super().__init__(name, scaled_hp)
        self.shield_hp = scaled_shield

    def display_status(self):
        super().display_status()


# --- Game Countdown ---
def game_ready_start_countdown():
    dm.clear_screen()
    width = 30 # Consistent width for the countdown boxes

    messages = ["READY...", "SET...", "FIGHT!"]
    for msg in messages:
        dm.clear_screen()
        print("\n" * 3) # More vertical spacing before the box
        dm.draw_box([msg], padding_x=6, padding_y=1, title="GET READY!", fixed_width=40)
        time.sleep(1)
    dm.clear_screen()

# --- Functions for a single bot fight ---
def _handle_player_turn(player, target, effective_difficulty, player_damage_multiplier, current_time_limit, is_boss_fight):
    """Handles the player's turn in combat."""
    
    # Draw "Your Turn!" inside a box
    dm.draw_box(["Your Turn!"], title="PLAYER TURN", padding_x=6, padding_y=0, fixed_width=30)
    time.sleep(0.5)

    if is_boss_fight:
        problem, correct_answer = generate_boss_problem(effective_difficulty)
        problem_title = "BOSS MATH PROBLEM"
    else:
        problem, correct_answer = generate_math_problem(effective_difficulty)
        problem_title = "MATH PROBLEM"

    problem_lines = [
        problem,
        f"(Time Limit: {current_time_limit:.0f} seconds)"
    ]
    # Get the total width of the problem box. We'll use this for the input box below.
    problem_box_total_width = dm.draw_box(problem_lines, title=problem_title, padding_x=4, padding_y=1, fixed_width=60)

    # Use the new dm.get_input_in_box, passing empty string for box_title
    player_guess, time_taken = get_player_input_answer_timed("Your Answer: ", problem_box_total_width, allow_string_input=False)

    # Handle surrender first as it's a direct exit
    if player_guess == "SURRENDER":
        confirm_lines = [
            "Are you sure you want to surrender?",
            "(Type 'yes' to confirm or anything else to cancel)"
        ]
        # Pass an empty string for box_title here
        confirm_box_total_width = dm.draw_box(confirm_lines, title="SURRENDER?", padding_x=4, padding_y=1, fixed_width=50)
        
        # Pass an empty string for box_title here
        player_confirm, _ = get_player_input_answer_timed("Confirm: ", confirm_box_total_width, allow_string_input=True) 

        if player_confirm == "yes":
            player.hp = 0 # Mark player as defeated for surrender
            dm.display_message_box("You have surrendered.", title="SURRENDERED", width=40)
            time.sleep(1)
            return True, True # Surrendered, fight ends
        else:
            dm.display_message_box("Surrender cancelled. Continue fighting!", title="FIGHT ON!", width=40)
            time.sleep(1)
            return False, False # Not surrendered, continue fight

    # --- Check for Time Limit Exceeded ---
    if time_taken > current_time_limit:
        timeout_box_width = dm.display_message_box([
            f"Time's up! You took {time_taken:.2f} seconds (limit: {current_time_limit:.0f}s).",
            f"The correct answer was {correct_answer}."
        ], title="TIME OUT!", width=60)
        damage_taken = 5  # Fixed damage for timeout
        player.take_damage(damage_taken)
        dm.print_centered(f"{player.name} took {damage_taken} damage for exceeding the time limit!", reference_width=timeout_box_width)
        time.sleep(1.5)
        return False, False # Not surrendered, but this turn was a failure

    # Align "You answered in X seconds." message
    dm.print_centered(f"You answered in {time_taken:.2f} seconds.", reference_width=problem_box_total_width) 
    time.sleep(0.5)

    if check_answer(player_guess, correct_answer):
        calculated_damage = calculate_damage(time_taken, player_damage_multiplier, current_time_limit)
        target.take_damage(calculated_damage)
        hit_box_width = dm.display_message_box(f"Correct! You dealt {calculated_damage} damage to {target.name}!", title="HIT!", width=60)

        if SHIELD_MIN_TIME < time_taken <= SHIELD_MAX_TIME:
            player.shield_hp += SHIELD_BONUS_AMOUNT
            dm.print_centered(f"Quick reflexes! {player.name} gained {SHIELD_BONUS_AMOUNT} Shield HP! Current Shield: {player.shield_hp}", reference_width=hit_box_width)
    else:
        damage_taken = random.randint(10, 15)
        player.take_damage(damage_taken)
        miss_box_width = dm.display_message_box([
            f"Incorrect! The answer was {correct_answer}.",
            f"{player.name} took {damage_taken} damage!"
        ], title="MISS!", width=60)

    time.sleep(1.5)
    return False, False

def _handle_bot_turn(player, target, effective_difficulty, is_boss_fight):
    """Handles the bot's/boss's turn in combat."""
    
    dm.draw_box([f"{target.name}'s Turn!"], title="BOT TURN", padding_x=6, padding_y=0, fixed_width=30)
    time.sleep(0.5)

    bot_accuracy_chance = 0.8 + (effective_difficulty * 0.02)
    bot_accuracy_chance = min(0.95, bot_accuracy_chance)
    bot_answer_time = random.uniform(1.0, 4.0 - (effective_difficulty * 0.2))
    bot_answer_time = max(0.5, bot_answer_time)
    bot_damage = random.randint(10, 20) + effective_difficulty * 2

    if is_boss_fight:
        bot_damage = int(bot_damage * 1.5)
        bot_answer_time = max(0.2, bot_answer_time * 0.7)

    time.sleep(bot_answer_time)

    if random.random() < bot_accuracy_chance:
        player.take_damage(bot_damage)
        dm.display_message_box(f"{target.name} got it right! {player.name} took {bot_damage} damage!", title="BOT ATTACK!", width=60)
    else:
        dm.display_message_box(f"{target.name} got it wrong! They stumbled!", title="BOT MISS!", width=60)

    time.sleep(2)

def run_single_bot_fight(player, target, effective_difficulty, player_damage_multiplier, current_time_limit):
    """
    Manages the combat loop for a single player vs. target (bot or boss) fight.
    """
    round_num = 1
    surrendered_in_fight = False
    is_boss_fight = isinstance(target, Boss)

    combat_area_width = 70 

    while not player.is_defeated() and not target.is_defeated():
        dm.clear_screen()
        dm.display_header(f"Round {round_num} vs {target.name}", width=combat_area_width) 
        
        player.display_status()
        target.display_status()
        
        left_offset = dm.get_centered_left_padding(combat_area_width)
        print(" " * left_offset + "-" * combat_area_width)

        surrendered_in_fight, fight_ended_due_to_surrender = _handle_player_turn(
            player, target, effective_difficulty, player_damage_multiplier, current_time_limit, is_boss_fight
        )

        if surrendered_in_fight or player.is_defeated() or target.is_defeated():
            break

        if not player.is_defeated() and not surrendered_in_fight:
            _handle_bot_turn(player, target, effective_difficulty, is_boss_fight)
            if player.is_defeated():
                break

        round_num += 1

    return player.is_defeated(), target.is_defeated(), surrendered_in_fight