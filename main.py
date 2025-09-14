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