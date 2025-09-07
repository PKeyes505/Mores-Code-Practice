
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

def practice_mode(unit_s, csv_path, limit=None):
    """
    Console practice mode similar to practice1:
    - Plays a random WORD from the CSV as Morse
    - You type the word back
    Commands:
      /r         repeat the Morse
      /n         reveal the word + definition, then go to next
      /s <wpm>   change speed
      /quit      exit
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

    print(f"\nPractice Words Mode: Using {csv_path} with {len(rows)} entries.")
    print("Type the word you hear in Morse.")
    print("Commands: /r to repeat, /n to reveal+next, /s <wpm> to change speed, /quit to exit.\n")

    rounds = 0
    while True:
        if limit is not None and rounds >= limit:
            print("Reached round limit. Exiting practice words mode.")
            break
        word, definition = random.choice(rows)
        morse = encode_to_morse(word)
        play_morse(morse, unit_s)

        while True:
            answer = input("Your answer (word): ").strip()
            if not answer:
                # empty repeats
                play_morse(morse, unit_s)
                continue

            upper = answer.upper()
            if upper == EXIT_COMMAND.upper():
                return
            elif upper == "/R":
                play_morse(morse, unit_s)
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
                    play_morse(morse, unit_s)
                except Exception:
                    print("Invalid speed. Usage: /s <wpm>")
                continue
            else:
                if answer.strip().lower() == word.strip().lower():
                    print("Correct!\n")
                else:
                    print(f"Incorrect. The word was: {word}")
                    if definition:
                        print(f"Definition: {definition}")
                    print()
                rounds += 1
                break
