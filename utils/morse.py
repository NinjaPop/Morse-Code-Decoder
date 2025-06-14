import numpy as np
from sklearn.cluster import KMeans
from difflib import get_close_matches
from .constants import MORSE_DICT
from .audio import bandpass, estimate_morse_tone_frequency

def detect_morse(y, sr, mode="Standard (Merged)", enhance=False):
    y = y / np.max(np.abs(y))
    dominant_freq = estimate_morse_tone_frequency(y, sr)
    y_filtered = bandpass(y, dominant_freq - 40, dominant_freq + 40, sr)

    frame_len = int((0.06 if enhance else 0.04) * sr)
    envelope = np.sqrt(np.convolve(y_filtered**2, np.ones(frame_len) / frame_len, mode='same'))

    # For future work to make the enhance button work better for low quality microphones
    # if enhance:
    #     # Apply noise floor suppression and adaptive thresholding
    #     noise_floor = np.percentile(envelope, 10)
    #     envelope -= noise_floor
    #     envelope = np.clip(envelope, 0, None)
    #     threshold = np.percentile(envelope, 95)
    # else:
    #     threshold = 0.3 * np.max(envelope)

    threshold = (0.15 if enhance else 0.3) * np.max(envelope)
    tone_mask = envelope > threshold

    changes = np.diff(tone_mask.astype(int))
    onsets = np.where(changes == 1)[0]
    offsets = np.where(changes == -1)[0]
    if tone_mask[0]: onsets = np.insert(onsets, 0, 0)
    if tone_mask[-1]: offsets = np.append(offsets, len(tone_mask) - 1)

    # Mode 3: Treat all tone segments independently
    if mode == "High Precision (No Merge)":
        merged = list(zip(onsets, offsets))
    # Mode 2: If you still want to merge but tolerate very short gaps
    elif mode == "Short Gap Merge (<10ms)":
        merged = []
        i = 0
        while i < len(onsets):
            start = onsets[i]
            end = offsets[i]
            while i + 1 < len(onsets) and (onsets[i + 1] - offsets[i]) / sr < 0.01: # Only merge <10ms
                end = offsets[i + 1]
                i += 1
            merged.append((start, end))
            i += 1
    else:
        merged = []
        i = 0
        while i < len(onsets):
            start, end = onsets[i], offsets[i]
            while i + 1 < len(onsets) and (onsets[i + 1] - offsets[i]) / sr < 0.03:
                end = offsets[i + 1]
                i += 1
            merged.append((start, end))
            i += 1

    tone_durations = np.array([(off - on) / sr for on, off in merged]).reshape(-1, 1)
    silence_durations = np.array([
        (merged[i+1][0] - merged[i][1]) / sr for i in range(len(merged) - 1)
    ]).reshape(-1, 1)

    if len(tone_durations) < 2:
        return "[No valid Morse detected]", y_filtered, sr

    kmeans_tone = KMeans(n_clusters=2, n_init=10, random_state=0).fit(tone_durations)
    dot_label = np.argmin(kmeans_tone.cluster_centers_)

    if len(silence_durations) >= 3:
        kmeans_silence = KMeans(n_clusters=3, n_init=10, random_state=0).fit(silence_durations)
        labels = kmeans_silence.labels_
        centers = kmeans_silence.cluster_centers_.flatten()
        intra_idx = np.argmin(centers)
        inter_idx = np.argsort(centers)[1]
        word_idx = np.argmax(centers)
    else:
        labels = np.zeros(len(silence_durations), dtype=int)
        intra_idx = inter_idx = word_idx = 0

    morse = []
    for i, (on, off) in enumerate(merged):
        label = kmeans_tone.labels_[i]
        morse.append('.' if label == dot_label else '-')
        if i < len(merged) - 1:
            gap_type = labels[i]
            if gap_type == inter_idx:
                morse.append(' ')
            elif gap_type == word_idx:
                morse.append(' / ')

    return ''.join(morse).strip(), y_filtered, sr

def decode_morse(morse_string):
    words = morse_string.split(' / ')
    return ' '.join(
        ''.join(MORSE_DICT.get(char, '?') for char in word.strip().split())
        for word in words
    )

def ai_guess_words(decoded_text, vocab=None):
    if vocab is None:
        vocab = [
            "INFO", "HELP", "ALERT", "DANGER", "ATTACK", "DEFEND", "MAYDAY", "MESSAGE", "STOP", "GO",
            "INCORRECT", "ATTENTION", "TRANSMISSION", "REQUEST", "NEED", "FLANK", "INCOMING", "REINFORCEMENT", 
            "LOCATION", "ACQUIRE"
        ]
    
    words = decoded_text.upper().split()
    guesses = []
    for word in words:
        match = get_close_matches(word, vocab, n=1, cutoff=0.5)
        guesses.append(match[0] if match else word)
    return ' '.join(guesses)
