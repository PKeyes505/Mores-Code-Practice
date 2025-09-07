import random
import string
from morse_utils import encode_to_morse
from audio_pygame import play_morse

EXIT_COMMAND = "/quit"

def seconds_per_unit(wpm):
    return 1.2 / float(wpm)

def practice_mode(unit_s, num_chars=5):
    chars = string.ascii_uppercase + string.digits
    print(f"\nPractice Mode: Type back the {num_chars} characters you hear in Morse.")
    print("Type /r to repeat, /n for next (shows answer), /s <wpm> to change speed, or /quit to exit.\n")

    running = True
    while running:
        seq = ''.join(random.choice(chars) for _ in range(num_chars))
        morse = encode_to_morse(seq)
        play_morse(morse, unit_s)

        while True:
            answer = input(f"Your answer ({num_chars} chars): ").strip().upper()
            if answer == EXIT_COMMAND.upper():
                running = False
                break
            elif answer == "/R":
                play_morse(morse, unit_s)
                continue
            elif answer == "/N":
                print(f"Morse code: {morse}")
                print(f"Characters: {seq}")
                break
            elif answer.startswith("/S "):
                try:
                    wpm = int(answer.split()[1])
                    unit_s = seconds_per_unit(wpm)
                    print(f"Speed changed to {wpm} WPM.")
                    play_morse(morse, unit_s)
                except Exception:
                    print("Invalid speed. Usage: /s <wpm>")
                continue
            elif answer == seq:
                print("Correct!\n")
                break
            else:
                print("Incorrect. Try again or type /r to repeat, /n for next, /s <wpm> to change speed.")
                play_morse(morse, unit_s)

if __name__ == "__main__":
    # Example usage: practice_mode(unit_s=0.06, num_chars=5)
    # Replace 0.06 with your unit_s value or import from main
    practice_mode(unit_s=0.06, num_chars=5)