# display_manager.py

import os
import sys

# --- Utility Function ---
def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def _get_terminal_width():
    """Safely gets the terminal width, defaults to 80 if not detectable."""
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80

def _get_max_width(lines):
    """Calculates the maximum width among a list of strings."""
    return max(len(line) for line in lines) if lines else 0

def get_centered_left_padding(content_width):
    """Calculates the left padding needed to center a block of content_width."""
    terminal_width = _get_terminal_width()
    return (terminal_width - content_width) // 2

def draw_box(content_lines, title="", padding_x=4, padding_y=1, fixed_width=None):
    """
    Draws a box around the given content lines with an optional title.
    Returns the actual total width of the drawn box (including borders).
    """
    if not isinstance(content_lines, list):
        content_lines = [str(content_lines)]

    max_content_width = _get_max_width(content_lines)
    
    inner_content_area_width = max_content_width + (padding_x * 2)

    if title:
        inner_content_area_width = max(inner_content_area_width, len(title) + 4)

    if fixed_width is not None:
        inner_content_area_width = max(inner_content_area_width, fixed_width - 2)

    box_total_width = inner_content_area_width + 2

    left_padding = get_centered_left_padding(box_total_width)
    
    def print_aligned_line(line):
        print(" " * left_padding + line)

    print_aligned_line("+" + "-" * (box_total_width - 2) + "+")

    if title:
        title_line = "|" + title.center(box_total_width - 2) + "|"
        print_aligned_line(title_line)
        print_aligned_line("+" + "-" * (box_total_width - 2) + "+")

    for _ in range(padding_y):
        print_aligned_line("|" + " " * (box_total_width - 2) + "|")

    for line in content_lines:
        centered_line_in_box = line.center(inner_content_area_width)
        print_aligned_line(f"|{centered_line_in_box}|")

    for _ in range(padding_y):
        print_aligned_line("|" + " " * (box_total_width - 2) + "|")

    print_aligned_line("+" + "-" * (box_total_width - 2) + "+")
    
    return box_total_width


def print_centered(text, reference_width=None):
    """
    Prints text centered. If reference_width is provided, it centers the text
    relative to that width's global horizontal position. Otherwise, it centers
    it across the whole terminal.
    """
    if reference_width is None:
        print(text.center(_get_terminal_width()))
    else:
        global_left_padding = get_centered_left_padding(reference_width)
        print(" " * global_left_padding + text.center(reference_width))

def center_text(text, target_width=None):
    """
    Centers text within a given target width or the terminal width.
    If target_width is None, it uses the detected terminal width.
    """
    if target_width is None:
        target_width = _get_terminal_width()
    return text.center(target_width)

def display_header(title, width=80):
    """Displays a large, framed header, centered on the screen."""
    top_bottom = "=" * width
    middle = f" {title.upper()} ".center(width - 2, ' ')
    
    left_padding = get_centered_left_padding(width)

    print("\n")
    print(" " * left_padding + top_bottom)
    print(" " * left_padding + middle)
    print(" " * left_padding + top_bottom)
    print("\n")

def display_message_box(message, title="", width=60, padding_y=1):
    """Displays a message within a simple box, centered on screen."""
    lines = message.split('\n') if isinstance(message, str) else message
    lines = [str(line) for line in lines]
    
    return draw_box(lines, title=title, padding_x=2, padding_y=padding_y, fixed_width=width)

def get_input_in_box(prompt_text, box_title="", box_width=None, padding_x=2, padding_y=0):
    """
    Draws a box with a prompt and places the input cursor inside it.
    Returns the user's input string. This version draws the box in parts for precise cursor control.
    """
    # Use prompt_text plus a reasonable buffer for input when calculating box width
    # This prevents the box from being too narrow for user input.
    min_input_buffer = 15 # Minimum characters for input field
    content_for_width_calc = [prompt_text + " " * min_input_buffer]
    
    max_content_width_calc = _get_max_width(content_for_width_calc)
    inner_content_area_width = max_content_width_calc + (padding_x * 2)

    if box_title:
        inner_content_area_width = max(inner_content_area_width, len(box_title) + 4)
    if box_width is not None:
        inner_content_area_width = max(inner_content_area_width, box_width - 2)
    
    actual_box_width = inner_content_area_width + 2
    left_padding_global = get_centered_left_padding(actual_box_width)

    # --- Draw the TOP part of the box ---
    print(" " * left_padding_global + "+" + "-" * (actual_box_width - 2) + "+")
    
    if box_title: # Only draw title if provided (box_title can be empty string)
        title_line = "|" + box_title.center(actual_box_width - 2) + "|"
        print(" " * left_padding_global + title_line)
        print(" " * left_padding_global + "+" + "-" * (actual_box_width - 2) + "+")

    for _ in range(padding_y):
        print(" " * left_padding_global + "|" + " " * (actual_box_width - 2) + "|")

    spaces_to_fill = inner_content_area_width - (len(prompt_text) + padding_x)
    
    # Ensure spaces_to_fill is not negative
    prompt_line_content_with_input_space = " " * padding_x + prompt_text + " " * max(0, spaces_to_fill)

    # Print the line and immediately move the cursor back to the start of the line with \r
    sys.stdout.write(" " * left_padding_global + "|" + prompt_line_content_with_input_space + "|" + "\r")
    sys.stdout.flush()

    # Move cursor to the exact input position (after prompt_text)
    # Global left padding + left border (1) + inner left padding_x + length of prompt_text
    cursor_x_pos = left_padding_global + 1 + padding_x + len(prompt_text)
    sys.stdout.write(f"\033[{cursor_x_pos}G") # Set cursor to column X
    sys.stdout.flush()

    # Get the user input without an internal prompt string from input()
    user_input = sys.stdin.readline().strip()
    
    
    sys.stdout.write("\033[1F") # Move cursor UP 1 line to the prompt line
    sys.stdout.write("\033[K")  # Clear the line from cursor position to end (erases user's typed input)
    sys.stdout.flush()

    empty_content_line_for_box_closure = " " * (actual_box_width - 2)
    print(" " * left_padding_global + "|" + empty_content_line_for_box_closure + "|")

    # Print the bottom padding and bottom border lines
    for _ in range(padding_y):
        print(" " * left_padding_global + "|" + " " * (actual_box_width - 2) + "|")

    print(" " * left_padding_global + "+" + "-" * (actual_box_width - 2) + "+")
    sys.stdout.flush() # Ensure all trailing prints are visible immediately
    
    return user_input