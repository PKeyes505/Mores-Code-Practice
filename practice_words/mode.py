
import csv
import random
from morse_utils import encode_to_morse
from audio_pygame import play_morse

EXIT_COMMAND = "/quit"

def seconds_per_unit(wpm):
    return 1.2 / float(wpm)

def load_words(csv_path):
    """
    Load rows of (word, definition) from a CSV file.
    Accepts a header with names like 'word' and 'definition' or positional columns.
    Skips blank or malformed rows.
    """
    rows = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        # Peek first row to decide if it's a header
        first = next(reader, None)
        if first is None:
            return rows
        # Determine header
        header_lower = [c.strip().lower() for c in first]
        if any(h in ("word", "definition", "def", "meaning") for h in header_lower):
            # Treat as headered file
            idx_word = None
            idx_def = None
            for i, h in enumerate(header_lower):
                if idx_word is None and h in ("word", "term", "text"):
                    idx_word = i
                if idx_def is None and h in ("definition", "def", "meaning", "hint"):
                    idx_def = i
            if idx_word is None:
                # fallback to first column
                idx_word = 0
            if idx_def is None:
                # fallback to second if exists
                idx_def = 1 if len(first) > 1 else None

            for row in reader:
                if not row:
                    continue
                w = row[idx_word].strip() if idx_word < len(row) else ""
                d = row[idx_def].strip() if (idx_def is not None and idx_def < len(row)) else ""
                if w:
                    rows.append((w, d))
        else:
            # Treat as data row
            if first and first[0].strip():
                rows.append((first[0].strip(), first[1].strip() if len(first) > 1 else ""))
            for row in reader:
                if not row:
                    continue
                w = row[0].strip()
                d = row[1].strip() if len(row) > 1 else ""
                if w:
                    rows.append((w, d))
    return rows

def _strip_non_alnum(s: str) -> str:
    # Keep letters and digits; collapse spaces/hyphens/underscores for practice
    return "".join(ch for ch in s if ch.isalnum())

def practice_mode(unit_s, csv_path, limit=None):
    """
    Progressive per-character practice for WORDS from a CSV.

    Flow for each round:
      1) Pick a random word W.
      2) Play Morse for the first character of W.
      3) User guesses the character:
         - If correct, play Morse for W[:2] and guess the 2nd char,
           then W[:3] and guess the 3rd char, etc. until the word is complete.
         - If incorrect, tell them and replay the current prefix.
      4) Reveal with /n, repeat with /r, change speed with /s <wpm>, or /quit to exit.
      5) You may also type the entire word at any time to finish the round.
    """
    try:
        rows = load_words(csv_path)
    except FileNotFoundError:
        print(f"CSV not found: {csv_path}")
        return
    except Exception as e:
        print(f"Failed to load CSV: {e}")
        return

    if not rows:
        print("No words found in CSV. Ensure it has at least one column with words, and optional definition.")
        return

    print(f"\nPractice Words Mode (progressive): Using {csv_path} with {len(rows)} entries.")
    print("Guess one character at a time. After each correct guess, the sequence grows and is replayed.")
    print("Commands: /r to repeat, /n to reveal+next, /s <wpm> to change speed, /quit to exit.\n")

    rounds = 0
    while True:
        if limit is not None and rounds >= limit:
            print("Reached round limit. Exiting practice words mode.")
            break

        word, definition = random.choice(rows)
        # canonical version for matching
        canonical = _strip_non_alnum(word).upper()
        if not canonical:
            # skip weird rows
            continue

        # progressive index (0-based char we want the user to identify next)
        idx = 0
        # Always start by playing the first char
        prefix = canonical[: idx + 1]
        morse_prefix = encode_to_morse(prefix)
        play_morse(morse_prefix, unit_s)

        while True:
            prompt = f"Guess char #{idx+1} (or type the whole word): "
            answer = input(prompt).strip()
            if not answer:
                # empty input == repeat
                play_morse(morse_prefix, unit_s)
                continue

            # Commands (case-insensitive)
            upper = answer.upper()
            if upper == EXIT_COMMAND.upper():
                return
            elif upper == "/R":
                play_morse(morse_prefix, unit_s)
                continue
            elif upper == "/N":
                print(f"Reveal → Word: {word}")
                if definition:
                    print(f"Definition: {definition}")
                print()
                rounds += 1
                break
            elif upper.startswith("/S "):
                try:
                    wpm = int(upper.split()[1])
                    unit_s = seconds_per_unit(wpm)
                    print(f"Speed changed to {wpm} WPM.")
                    play_morse(morse_prefix, unit_s)
                except Exception:
                    print("Invalid speed. Usage: /s <wpm>")
                continue

            # If they typed multiple characters, allow a full-word solve
            if len(answer) > 1:
                if _strip_non_alnum(answer).upper() == canonical:
                    print(f"Correct! The word was: {word}\n")
                    rounds += 1
                    break
                else:
                    print("Not quite. Keep going—listen again.")
                    play_morse(morse_prefix, unit_s)
                    continue

            # Single-character guess path
            guess = upper[0]
            correct = canonical[idx]
            if guess == correct:
                idx += 1
                if idx == len(canonical):
                    print(f"Great! Completed: {word}")
                    if definition:
                        print(f"Definition: {definition}")
                    print()
                    rounds += 1
                    break
                else:
                    # Grow the sequence by one and replay
                    prefix = canonical[: idx + 1]
                    morse_prefix = encode_to_morse(prefix)
                    play_morse(morse_prefix, unit_s)
            else:
                print(f"Incorrect for position {idx+1}. Try again. (Hint: target length {len(canonical)})")
                play_morse(morse_prefix, unit_s)
