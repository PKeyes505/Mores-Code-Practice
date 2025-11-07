<<<<<<< HEAD
import winsound  # Windows only
import time

# Morse Code dictionary
MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.'
}

def play_morse(text, wpm=20, freq=600):
    """Play text in Morse code with proper spacing."""
    dot_duration = 1.2 / wpm  # dit length (sec)
    dash_duration = 3 * dot_duration
    intra_char_gap = dot_duration
    letter_gap = 3 * dot_duration
    word_gap = 7 * dot_duration

    text = text.upper()

    # Print converted Morse for reference
    morse_text = " ".join(MORSE_CODE.get(ch, "") for ch in text if ch != " ")
    print(f"[{text}] -> {morse_text}")

    for idx, char in enumerate(text):
        if char == " ":
            time.sleep(word_gap)
            continue

        morse = MORSE_CODE.get(char, "")
        for i, symbol in enumerate(morse):
            if symbol == ".":
                winsound.Beep(freq, int(dot_duration * 1000))
            elif symbol == "-":
                winsound.Beep(freq, int(dash_duration * 1000))

            # Gap between symbols of same letter (except after last one)
            if i < len(morse) - 1:
                time.sleep(intra_char_gap)

        # Gap between letters (except if next char is space or end of text)
        if idx < len(text) - 1 and text[idx + 1] != " ":
            time.sleep(letter_gap)

if __name__ == "__main__":
    print("Morse Code Trainer (type 'exit' to quit)\n")
    wpm = int(input("Set speed (WPM): "))
    freq = int(input("Set tone frequency (Hz): "))

    while True:
        msg = input("\nEnter text: ")
        if msg.strip().lower() in ("exit", "quit", "q"):
            print("Exiting...")
            break
        play_morse(msg, wpm=wpm, freq=freq)
=======
import sys
from pygame import mixer
from audio_pygame import play_morse
from morse_utils import encode_to_morse
from practice import practice_mode
from practice1 import practice_mode as practice1_mode
from practice_words.mode import practice_mode as practice_words_mode

# Configuration
TONE_FREQ_HZ = 528
WPM = 20
VOLUME = 0.5
SAMPLE_RATE = 44100
EXIT_COMMAND = "/quit"
TEXT_PROMPT = "Enter text (or /quit): "

def seconds_per_unit(wpm):
    return 1.2 / float(wpm)

def handle_speed_command(parts):
    global WPM
    if len(parts) > 1 and parts[1].isdigit():
        WPM = int(parts[1])
        print(f"Speed changed to {WPM} WPM.")
        return seconds_per_unit(WPM)
    else:
        print("Usage: /s <wpm>")
        return seconds_per_unit(WPM)

def handle_practice_command(parts, unit_s):
    num_chars = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 5
    practice_mode(unit_s, num_chars)

def handle_practice1_command(parts, unit_s):
    num_chars = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 5
    print(f"Starting practice1 mode with {num_chars} characters.")
    practice1_mode(unit_s, num_chars)
    
def handle_practice_words_command(parts, unit_s):
    """
    Usage:
      /practice_words <csv_path> [rounds]
      /pw <csv_path> [rounds]
    If rounds is provided, stop after that many prompts.
    """
    if len(parts) < 2:
        csv_path = input("Enter path to CSV file: ").strip()
    else:
        csv_path = parts[1]
    limit = None
    if len(parts) > 2 and parts[2].isdigit():
        limit = int(parts[2])
    print(f"Starting practice_words mode using {csv_path} ...")
    practice_words_mode(unit_s, csv_path, limit)


def main():
    global WPM
    import pygame
    pygame.init()
    mixer.init(frequency=SAMPLE_RATE, size=-16, channels=1, buffer=512)
    unit_s = seconds_per_unit(WPM)
    print(f"[Morse Out] {WPM} WPM | {TONE_FREQ_HZ} Hz | volume {VOLUME} | sample_rate {SAMPLE_RATE}")
    print(f"Type {EXIT_COMMAND} to exit.\n")

    try:
        last_text = ""
        while True:
            text = input(TEXT_PROMPT)
            if text is None:
                continue
            text = text.strip()
            if not text:
                # Replay last text if available
                if last_text:
                    morse = encode_to_morse(last_text)
                    print(f"Replaying: {last_text}")
                    print(f"Morse: {morse}")
                    play_morse(morse, unit_s)
                continue
            if text.lower() == EXIT_COMMAND.lower():
                break

            parts = text.split()
            cmd = parts[0].lower()

            if cmd == "/s":
                unit_s = handle_speed_command(parts)
                continue
            elif cmd in ("/practice",):
                handle_practice_command(parts, unit_s)
                continue
            elif cmd in ("/practice1", "/p1"):
                handle_practice1_command(parts, unit_s)
                continue
            elif cmd in ("/practice_words", "/pw"):
                handle_practice_words_command(parts, unit_s)
                continue

            morse = encode_to_morse(text)
            print(f"Morse: {morse}")
            play_morse(morse, unit_s)
            last_text = text

    except KeyboardInterrupt:
        pass
    finally:
        try:
            mixer.quit()
        except Exception:
            pass
        try:
            pygame.quit()
        except Exception:
            pass
        print("\nBye.")

if __name__ == "__main__":
    main()
>>>>>>> 56568d9579da9d9cf0482b8b6efcab385141c7ce
