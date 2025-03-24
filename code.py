import random
from datetime import datetime

# Load word bank
with open("words.txt", "r") as f:
    valid_words = [word.strip().lower() for word in f.readlines()]
    target_words = [word for word in valid_words if len(word) == 5]

# Seed based on today's date for a daily word
random.seed(datetime.now().strftime("%Y%m%d"))
target = random.choice(target_words)

def validate_guess(guess):
    """Check if the guess is a valid 5-letter word."""
    return len(guess) == 5

def generate_feedback(guess, target):
    """Generate 🟩🟨⬜ feedback."""
    feedback = []
    target_counts = {}
    guess_counts = {}

    # First pass: Check for correct letters in correct positions (green)
    for g, t in zip(guess, target):
        if g == t:
            feedback.append("🟩")
        else:
            feedback.append("")
            target_counts[t] = target_counts.get(t, 0) + 1
            guess_counts[g] = guess_counts.get(g, 0) + 1

    # Second pass: Check for correct letters in wrong positions (yellow)
    for i, (g, t) in enumerate(zip(guess, target)):
        if feedback[i] == "":
            if g in target_counts and target_counts[g] > 0:
                feedback[i] = "🟨"
                target_counts[g] -= 1
            else:
                feedback[i] = "⬜"

    return "".join(feedback)

def generate_shareable_result(attempts_taken, feedback_grid):
    """Create a shareable emoji grid."""
    result = f"PyWordle {datetime.now().strftime('%Y-%m-%d')} {attempts_taken}/6\n"
    max_row = attempts_taken if isinstance(attempts_taken, int) else 6
    for i in range(max_row):
        result += feedback_grid[i] + "\n"
    return result

def play_wordle():
    max_attempts = 6
    feedback_grid = ["⬜⬜⬜⬜⬜"] * max_attempts  # Initialize 6x5 gray grid
    attempts_taken = 0

    print("Welcome to PyWordle! Guess the 5-letter word in 6 tries.\n")
    print("How to play:")
    print("🟩 - Correct letter in the right position")
    print("🟨 - Correct letter in the wrong position")
    print("⬜ - Letter not in the word\n")
    print("Initial Grid:")
    print("\n".join(feedback_grid))
    print()

    for attempt in range(1, max_attempts + 1):
        # Get guess
        while True:
            guess = input(f"Attempt {attempt}/6: ").lower()
            if validate_guess(guess):
                break
            print("Invalid word. Please enter a 5-letter word.")

        attempts_taken = attempt

        # Generate feedback and update grid
        feedback = generate_feedback(guess, target)
        feedback_grid[attempt - 1] = feedback

        # Print updated grid
        print("\nUpdated Grid:")
        print("\n".join(feedback_grid))
        print()

        # Check win condition
        if guess == target:
            print(f"🎉 You won in {attempt} attempts!")
            break

    else:  # Loop completed without breaking (loss)
        attempts_taken = "X"
        print(f"💔 Game over! The word was: {target}")

    # Generate shareable result
    share_result = generate_shareable_result(attempts_taken, feedback_grid)
    print("\nShare your result:\n" + share_result)
    return share_result

if __name__ == "__main__":
    play_wordle()