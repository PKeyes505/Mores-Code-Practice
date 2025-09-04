#!/usr/bin/env python3
"""
Morse Code Audio Out
- Encodes input text to Morse using morse3
- Plays tone beeps with pygame
- Loops until you type the exit command
"""

# =========================
# Variables (tweak these) :
# =========================
TONE_FREQ_HZ     = 528      # Sine tone frequency
WPM              = 15       # Words per minute (dot = 1.2/WPM seconds)
VOLUME           = 0.5      # 0.0 .. 1.0
SAMPLE_RATE      = 44100    # Audio sample rate
EXIT_COMMAND     = "/quit"  # Type this to exit
TEXT_PROMPT      = "Enter text (or /quit): "  # Prompt shown each loop

# If you want extra spacing (Farnsworth feel), bias these multipliers above defaults.
UNIT_DOT_MULT    = 1.0      # dot length = 1 unit
UNIT_DASH_MULT   = 3.0      # dash length = 3 units
UNIT_GAP_INTRA   = 1.0      # gap between symbols in a letter = 1 unit
UNIT_GAP_INTER   = 3.0      # gap between letters = 3 units
UNIT_GAP_WORD    = 7.0      # gap between words = 7 units
# =========================

import sys
import time

try:
    import numpy as np
except Exception:
    sys.exit("Missing dependency 'numpy'. Install with: pip install numpy")

try:
    import pygame
    from pygame import mixer
except Exception:
    sys.exit("Missing dependency 'pygame'. Install with: pip install pygame")

try:
    import morse3  # pip install morse3
except Exception:
    sys.exit("Missing dependency 'morse3'. Install with: pip install morse3")


def seconds_per_unit(wpm: float) -> float:
    # Standard: dot (one unit) duration in seconds = 1.2 / WPM
    return 1.2 / float(wpm)


def make_tone_buffer(freq_hz: float, duration_sec: float, volume: float, sample_rate: int) -> pygame.mixer.Sound:
    """Create a pygame Sound for a sine tone of given duration."""
    n_samples = max(1, int(duration_sec * sample_rate))
    t = np.arange(n_samples) / sample_rate
    wave = np.sin(2 * np.pi * freq_hz * t)  # sine wave
    audio = (wave * (32767 * max(0.0, min(1.0, volume)))).astype(np.int16)
    return pygame.mixer.Sound(buffer=audio.tobytes())


def play_silence(duration_sec: float):
    time.sleep(max(0.0, duration_sec))


def play_tone(duration_sec: float):
    snd = make_tone_buffer(TONE_FREQ_HZ, duration_sec, VOLUME, SAMPLE_RATE)
    ch = snd.play()
    while ch.get_busy():
        pygame.time.wait(1)


def play_symbol(symbol: str, unit_s: float):
    """Play a '.' or '-' and then the intra-character gap."""
    if symbol == '.':
        play_tone(unit_s * UNIT_DOT_MULT)
    elif symbol == '-':
        play_tone(unit_s * UNIT_DASH_MULT)
    else:
        return
    # intra-character gap (between symbols of same letter)
    play_silence(unit_s * UNIT_GAP_INTRA)


def play_morse(morse_text: str, unit_s: float):
    """
    Expects morse like: "... --- ..." with spaces between letters and '/' between words.
    We'll treat:
      ' '  -> inter-character gap (already had an intra gap after last symbol, so add 2 more units)
      '/'  -> word gap
    """
    for ch in morse_text:
        if ch == '.' or ch == '-':
            play_symbol(ch, unit_s)
        elif ch == ' ':  # between letters
            # We already slept 1 unit after the last symbol. Inter-letter total is 3 units -> add 2 more.
            play_silence(unit_s * max(0.0, (UNIT_GAP_INTER - UNIT_GAP_INTRA)))
        elif ch == '/':  # between words
            # We already slept 1 unit after the last symbol. Word gap total is 7 units -> add 6 more.
            play_silence(unit_s * max(0.0, (UNIT_GAP_WORD - UNIT_GAP_INTRA)))
        # ignore anything else


def normalize_morse(s: str) -> str:
    """
    Normalize morse output to a predictable form:
      - single spaces between letters
      - '/' between words (no surrounding spaces)
    """
    # morse3 usually uses single spaces between letters and ' / ' between words.
    s = s.strip()
    # Tighten spaces around slashes to single '/'
    s = s.replace(" / ", "/").replace(" /", "/").replace("/ ", "/")
    # Collapse any multiple spaces
    parts = s.split()
    s = " ".join(parts)
    return s


def encode_to_morse(s: str) -> str:
    """
    Use morse3 to encode text to Morse.
    morse3 API: create a Morse object with the source string, then call .stringToMorse()
    """
    m = morse3.Morse(s)
    code = m.stringToMorse()  # encode string → Morse
    return normalize_morse(code)


def main():
    # Init audio
    pygame.init()
    mixer.init(frequency=SAMPLE_RATE, size=-16, channels=1, buffer=512)

    unit_s = seconds_per_unit(WPM)
    print(f"[Morse Out] {WPM} WPM | {TONE_FREQ_HZ} Hz | volume {VOLUME} | sample_rate {SAMPLE_RATE}")
    print(f"Type {EXIT_COMMAND} to exit.\n")

    try:
        while True:
            try:
                text = input(TEXT_PROMPT)
            except EOFError:
                break
            if text is None:
                continue
            text = text.strip()
            if not text:
                continue
            if text.lower() == EXIT_COMMAND.lower():
                break

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
