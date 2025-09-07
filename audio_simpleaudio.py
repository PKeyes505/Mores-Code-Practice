import numpy as np
import audio_simpleaudio as sa
import time

TONE_FREQ_HZ = 528
VOLUME = 0.5
SAMPLE_RATE = 44100

UNIT_DOT_MULT = 1.0
UNIT_DASH_MULT = 3.0
UNIT_GAP_INTRA = 1.0
UNIT_GAP_INTER = 3.0
UNIT_GAP_WORD = 7.0

def make_tone_buffer(freq_hz, duration_sec, volume, sample_rate):
    n_samples = max(1, int(duration_sec * sample_rate))
    t = np.arange(n_samples) / sample_rate
    wave = np.sin(2 * np.pi * freq_hz * t)

    # Fade-in/out (5 ms each)
    fade_len = int(0.005 * sample_rate)
    envelope = np.ones(n_samples)
    if fade_len * 2 < n_samples:
        envelope[:fade_len] = np.linspace(0, 1, fade_len)
        envelope[-fade_len:] = np.linspace(1, 0, fade_len)
    wave *= envelope

    audio = (wave * (32767 * max(0.0, min(1.0, volume)))).astype(np.int16)
    return audio

def play_silence(duration_sec):
    time.sleep(max(0.0, duration_sec))

def play_tone(duration_sec):
    audio = make_tone_buffer(TONE_FREQ_HZ, duration_sec, VOLUME, SAMPLE_RATE)
    play_obj = sa.play_buffer(audio, 1, 2, SAMPLE_RATE)
    play_obj.wait_done()

def play_symbol(symbol, unit_s):
    if symbol == '.':
        play_tone(unit_s * UNIT_DOT_MULT)
    elif symbol == '-':
        play_tone(unit_s * UNIT_DASH_MULT)
    else:
        return
    play_silence(unit_s * UNIT_GAP_INTRA)

def play_morse(morse_text, unit_s):
    for ch in morse_text:
        if ch in ('.', '-'):
            play_symbol(ch, unit_s)
        elif ch == ' ':
            play_silence(unit_s * max(0.0, (UNIT_GAP_INTER - UNIT_GAP_INTRA)))
        elif ch == '/':
            play_silence(unit_s * max(0.0, (UNIT_GAP_WORD - UNIT_GAP_INTRA)))