import sys
from pygame import mixer
from audio import play_morse
from morse_utils import encode_to_morse
from practice import practice_mode
from practice1 import practice_mode as practice1_mode  # Add this import

TONE_FREQ_HZ = 528
WPM = 20
VOLUME = 0.5
SAMPLE_RATE = 44100
EXIT_COMMAND = "/quit"
TEXT_PROMPT = "Enter text (or /quit): "

def seconds_per_unit(wpm):
    return 1.2 / float(wpm)

def main():
    import pygame
    pygame.init()
    mixer.init(frequency=SAMPLE_RATE, size=-16, channels=1, buffer=512)
    unit_s = seconds_per_unit(WPM)
    print(f"[Morse Out] {WPM} WPM | {TONE_FREQ_HZ} Hz | volume {VOLUME} | sample_rate {SAMPLE_RATE}")
    print(f"Type {EXIT_COMMAND} to exit.\n")

    try:
        while True:
            text = input(TEXT_PROMPT)
            if text is None:
                continue
            text = text.strip()
            if not text:
                continue
            if text.lower() == EXIT_COMMAND.lower():
                break
            if text.lower().startswith("/practice1") or text.lower().startswith("/p1"):
                parts = text.strip().split()
                if len(parts) > 1 and parts[1].isdigit():
                    num_chars = int(parts[1])
                else:
                    num_chars = 5
                practice1_mode(unit_s, num_chars)
                continue
            if text.lower().startswith("/practice"):
                parts = text.strip().split()
                if len(parts) > 1 and parts[1].isdigit():
                    num_chars = int(parts[1])
                else:
                    num_chars = 5
                practice_mode(unit_s, num_chars)
                continue

            morse = encode_to_morse(text)
            print(f"Morse: {morse}")
            play_morse(morse, unit_s)

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