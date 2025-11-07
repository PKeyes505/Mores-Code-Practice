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
