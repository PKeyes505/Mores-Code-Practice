import time
import simpleaudio as sa
from MorseCodePy import MorseCode

# Initialize MorseCode encoder/decoder (defaults to English International Morse)
morse = MorseCode()

def play_morse(text, wpm=20, freq=600):
    """Play Morse code audio from given text."""
    dot_duration = 1.2 / wpm  # duration of a dit in seconds
    dash_duration = 3 * dot_duration
    intra_char_gap = dot_duration
    letter_gap = 3 * dot_duration
    word_gap = 7 * dot_duration

    # Encode text into Morse (dots/dashes)
    morse_text = morse.encode(text.upper())
    print(f"{text} → {morse_text}")

    # Generate tones and gaps
    for idx, char in enumerate(text.upper()):
        if char == " ":
            time.sleep(word_gap)
            continue

        code = morse.encode(char)
        for i, symbol in enumerate(code):
            if symbol == ".":
                play_tone(freq, dot_duration)
            elif symbol == "-":
                play_tone(freq, dash_duration)

            # Gap between symbols of the same letter
            if i < len(code) - 1:
                time.sleep(intra_char_gap)

        # Gap between letters
        if idx < len(text) - 1 and text[idx + 1] != " ":
            time.sleep(letter_gap)


def play_tone(freq, duration):
    """Generate and play a tone at freq (Hz) for duration (seconds)."""
    sample_rate = 44100
    t = (np.arange(int(sample_rate * duration)) / sample_rate).astype(np.float32)
    wave = (0.5 * np.sin(2 * np.pi * freq * t)).astype(np.float32)

    audio = (wave * 32767).astype(np.int16).tobytes()
    play_obj = sa.play_buffer(audio, 1, 2, sample_rate)
    play_obj.wait_done()


if __name__ == "__main__":
    import numpy as np

    print("Morse Code Trainer (type 'exit' to quit)\n")
    wpm = int(input("Speed (WPM): "))
    freq = int(input("Tone Frequency (Hz): "))

    while True:
        msg = input("\nEnter text: ")
        if msg.strip().lower() in ("exit", "quit", "q"):
            print("73 and clear!")
            break
        play_morse(msg, wpm=wpm, freq=freq)
