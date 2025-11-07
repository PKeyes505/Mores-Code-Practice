import numpy as np
import audio_simpleaudio as sa
import time

TONE_FREQ_HZ = 528
VOLUME = 0.5
SAMPLE_RATE = 44100

UNIT_DOT_MULT = 1.0
UNIT_DASH_MULT = 3.0
UNIT_GAP_INTRA = 1.0      # gap between symbols within a character
UNIT_GAP_INTER = 3.0      # gap between characters
UNIT_GAP_WORD = 7.0       # gap between words

def make_tone_buffer(freq_hz, duration_sec, volume, sample_rate):
    """
    Build a sine tone as a simpleaudio WaveObject (16-bit PCM, mono).
    Includes a 5 ms fade-in/out to avoid clicks.
    """
    duration_sec = max(0.0, float(duration_sec))
    n_samples = max(1, int(duration_sec * sample_rate))

    # Time base
    t = np.arange(n_samples, dtype=np.float64) / sample_rate
    wave = np.sin(2.0 * np.pi * float(freq_hz) * t)

    # Fade-in/out (5 ms each) to prevent clicks
    fade_len = int(0.005 * sample_rate)
    if fade_len * 2 < n_samples:
        envelope = np.ones(n_samples, dtype=np.float64)
        envelope[:fade_len] = np.linspace(0.0, 1.0, fade_len, endpoint=True)
        envelope[-fade_len:] = np.linspace(1.0, 0.0, fade_len, endpoint=True)
        wave *= envelope

    # Clamp volume to [0, 1] and scale to int16
    vol = max(0.0, min(1.0, float(volume)))
    audio_i16 = np.int16(wave * vol * 32767)

    # Create a WaveObject: mono (1 channel), 2 bytes/sample, given sample rate
    return sa.WaveObject(audio_i16.tobytes(), num_channels=1, bytes_per_sample=2, sample_rate=sample_rate)

def play_silence(duration_sec):
    time.sleep(max(0.0, float(duration_sec)))

def play_tone(duration_sec):
    wave_obj = make_tone_buffer(TONE_FREQ_HZ, duration_sec, VOLUME, SAMPLE_RATE)
    play_obj = wave_obj.play()
    play_obj.wait_done()  # block until the tone finishes

def play_symbol(symbol, unit_s):
    if symbol == '.':
        play_tone(unit_s * UNIT_DOT_MULT)
    elif symbol == '-':
        play_tone(unit_s * UNIT_DASH_MULT)
    else:
        return
    # intra-character gap after every symbol
    play_silence(unit_s * UNIT_GAP_INTRA)

def play_morse(morse_text, unit_s):
    """
    morse_text: string of '.', '-', ' ' (char gap), '/' (word gap)
    unit_s: length of one Morse "unit" in seconds
    """
    unit_s = float(unit_s)
    for ch in morse_text:
        if ch in ('.', '-'):
            play_symbol(ch, unit_s)
        elif ch == ' ':
            # We've already added an intra-character gap after the last symbol,
            # so top it up to the full inter-character gap.
            play_silence(unit_s * max(0.0, (UNIT_GAP_INTER - UNIT_GAP_INTRA)))
        elif ch == '/':
            # Likewise, top up to the full word gap.
            play_silence(unit_s * max(0.0, (UNIT_GAP_WORD - UNIT_GAP_INTRA)))
