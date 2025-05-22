# combat.py

import time
import random
import os
import sys 

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

# --- Utility Function ---
def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

# --- Math Problem Generation ---
def generate_math_problem(effective_difficulty):
    """
    Generates a single-operation math problem based on the effective difficulty level.
    """
    operators = ["+"] # Addition is always available

    if effective_difficulty >= 1:
        operators.append("-") 
        operators.append("*") 

    if effective_difficulty >= 3:
        operators.append("/") 

    operator = random.choice(operators)
    
    num1, num2, correct_answer = 0, 0, 0

    if operator == "+":
        num1_max = 10 + effective_difficulty * 5
        num2_max = 10 + effective_difficulty * 5
        num1 = random.randint(1, num1_max)
        num2 = random.randint(1, num2_max)
        correct_answer = num1 + num2
    
    elif operator == "-":
        num1_max = 20 + effective_difficulty * 5
        num2_max = 10 + effective_difficulty * 3
        temp_num1 = random.randint(1, num1_max)
        temp_num2 = random.randint(1, num2_max)
        num1 = max(temp_num1, temp_num2) 
        num2 = min(temp_num1, temp_num2) 
        correct_answer = num1 - num2

    elif operator == "*":
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

        correct_answer = num1 * num2

    elif operator == "/":
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
        
        correct_answer = int(num1 / num2) 

    problem_string = f"What is {num1} {operator} {num2}? "
    
    return problem_string, correct_answer

# Boss Question Generation
def generate_boss_problem(effective_difficulty):
    """
    Generates a multi-operation math problem for boss fights.
    Uses +, -, * and sometimes / (ensuring integer results).
    """
    operators_pool = ["+", "-", "*"]
    
    # Introduce division more carefully in mixed problems
    if effective_difficulty >= 5: # Division for mixed problems at higher boss difficulties
        operators_pool.append("/")

    num_ops = 2 # Start with two operations (e.g., A op B op C)
    if effective_difficulty >= 7:
        num_ops = 3 # More complex: A op B op C op D

    parts = []
    
    # Generate the first number
    first_num_max = 50 + effective_difficulty * 10
    parts.append(str(random.randint(10, first_num_max)))

    for i in range(num_ops):
        operator = random.choice(operators_pool)
        next_num_max = 20 + effective_difficulty * 3
        
        # If division is chosen, ensure previous part is divisible for guaranteed integer result
        # This requires more complex expression building. For now, we use a simple approach
        # and rely on 'eval' for calculation, ensuring integer inputs to avoid floats.
        if operator == "/":
            # To ensure integer division, we'll generate the divisor and then the dividend.
            # This makes the problem less "random" but guarantees integer results.
            temp_divisor = random.randint(2, min(10 + effective_difficulty, 20))
            # Ensure the dividend is a multiple of the divisor
            temp_quotient = random.randint(1, min(15 + effective_difficulty, 30))
            next_num = temp_divisor
            # The previous result becomes the dividend. This is tricky with eval.
            # For simplicity, we'll ensure the *overall* expression evaluates to an integer,
            # and rely on the number ranges to make accidental floats less likely with / only as final op.
            # For robust mixed division, it's best to pre-calculate and simplify sub-expressions.
            
            # For current implementation, let's keep it robust for +, -, * only in multi-op for now.
            # If division is included in operators_pool, it's assumed it's handled by eval's float math,
            # but we explicitly cast to int for answer.
            pass # Keep logic simple for mixed expressions, rely on eval.

        next_num = random.randint(1, next_num_max) # Standard number generation

        parts.append(operator)
        parts.append(str(next_num))
    
    problem_string = " ".join(parts)
    
    try:
        correct_answer = eval(problem_string)
        # Ensure the final answer is an integer. If division is allowed and results in float, it will be truncated.
        correct_answer = int(correct_answer) 
    except Exception as e:
        print(f"Error evaluating boss problem '{problem_string}': {e}. Retrying problem generation.")
        return generate_boss_problem(effective_difficulty) 

    return problem_string + "? ", correct_answer

def get_player_input_answer_timed(problem_string):
    """
    Prompts the player for an answer and measures the time taken.
    Returns (player_answer, time_taken).
    """
    start_time = time.time()
    while True:
        try:
            player_input = input(problem_string)
            end_time = time.time()
            if player_input.lower() == "surrender":
                return "SURRENDER", 0
            
            player_answer = int(player_input)
            time_taken = end_time - start_time
            return player_answer, time_taken
        except ValueError:
            print("Invalid input. Please enter a whole number or 'surrender'.")
            start_time = time.time() 

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
        self.shield_hp = 0 

    def display_status(self):
        status_string = f"{self.name}: HP {self.hp}/{self.max_hp}"
        if self.shield_hp > 0:
            status_string += f" | Shield: {self.shield_hp}" 
        print(status_string)

# NEW: Boss Character Class (MODIFIED!)
class Boss(Character):
    def __init__(self, name, effective_difficulty=0, scaling_factor=1): # Added scaling_factor
        # Boss HP and Shield now scale by scaling_factor
        scaled_hp = int(BOSS_BASE_HEALTH * scaling_factor)
        scaled_shield = int(BOSS_BASE_SHIELD * scaling_factor)
        
        super().__init__(name, scaled_hp) 
        self.shield_hp = scaled_shield 

    def display_status(self):
        status_string = f"!!! BOSS {self.name} !!! HP {self.hp}/{self.max_hp}"
        if self.shield_hp > 0:
            status_string += f" | Shield: {self.shield_hp}"
        print(status_string)

# --- Game Countdown ---
def game_ready_start_countdown():
    clear_screen()
    print("\n" * 5)
    print("           READY...".center(40))
    time.sleep(1)
    clear_screen()
    print("\n" * 5)
    print("           SET...".center(40))
    time.sleep(1)
    clear_screen()
    print("\n" * 5)
    print("           FIGHT!".center(40))
    time.sleep(1)
    clear_screen()

# --- Function to handle a single bot fight ---
def run_single_bot_fight(player, target, effective_difficulty, player_damage_multiplier, current_time_limit):
    """
    Manages the combat loop for a single player vs. target (bot or boss) fight.
    """
    round_num = 1
    surrendered_in_fight = False
    
    is_boss_fight = isinstance(target, Boss) 

    while not player.is_defeated() and not target.is_defeated(): 
        clear_screen()
        print(f"\n--- Round {round_num} vs {target.name} ---") 
        player.display_status()
        target.display_status() 
        print("-" * 20)

        # Player's Turn
        print("\nYour Turn!")
        if is_boss_fight: 
            problem, correct_answer = generate_boss_problem(effective_difficulty)
            print("--- BOSS PROBLEM ---") 
        else:
            problem, correct_answer = generate_math_problem(effective_difficulty)

        print(f"{problem}") 
        print(f"(Time Limit: {current_time_limit:.0f} seconds)") 

        player_guess, time_taken = get_player_input_answer_timed("")

        if player_guess == "SURRENDER":
            confirm = input("Are you sure you want to surrender? (yes/no): ").lower()
            if confirm == "yes":
                surrendered_in_fight = True
                player.hp = 0
                print("You have surrendered.")
                time.sleep(1)
                break
            else:
                print("Surrender cancelled. Continue fighting!")
                time.sleep(1)
                continue

        print(f"You answered in {time_taken:.2f} seconds.")

        if check_answer(player_guess, correct_answer):
            calculated_damage = calculate_damage(time_taken, player_damage_multiplier, current_time_limit)
            target.take_damage(calculated_damage) 
            print(f"Correct! You dealt {calculated_damage} damage to {target.name}!")
            
            if SHIELD_MIN_TIME < time_taken <= SHIELD_MAX_TIME: 
                player.shield_hp += SHIELD_BONUS_AMOUNT
                print(f"Quick reflexes! {player.name} gained {SHIELD_BONUS_AMOUNT} Shield HP! Current Shield: {player.shield_hp}")
        else:
            damage_taken = random.randint(10, 15)
            player.take_damage(damage_taken) 
            print(f"Incorrect! The answer was {correct_answer}. {player.name} took {damage_taken} damage!")
        
        if target.is_defeated(): 
            break

        time.sleep(1.5) 

        # Bot's/Boss's Turn (only if player is not defeated and not surrendered)
        if not player.is_defeated() and not surrendered_in_fight:
            print(f"\n{target.name}'s Turn!") 
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
                print(f"{target.name} got it right! {player.name} took {bot_damage} damage!") 
            else:
                print(f"{target.name} got it wrong! They stumbled!") 

            if player.is_defeated():
                break
            
            time.sleep(2)
        round_num += 1

    return player.is_defeated(), target.is_defeated(), surrendered_in_fight