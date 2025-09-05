import morse3

def normalize_morse(s):
    s = s.strip()
    s = s.replace(" / ", " / ").replace(" /", " / ").replace("/ ", " / ").replace("/", " / ")
    s = " ".join(s.split())
    return s

def encode_to_morse(s):
    words = [w for w in s.split() if w]
    encoded_words = []
    for w in words:
        code = morse3.Morse(w).stringToMorse()
        code = " ".join(code.split())
        encoded_words.append(code)
    return " / ".join(encoded_words)