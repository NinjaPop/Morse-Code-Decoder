# Licensed under the GNU General Public License v3.0
# See LICENSE file or https://www.gnu.org/licenses/gpl-3.0.html for details.

import numpy as np
from scipy.signal import butter, lfilter, welch
import soundfile as sf
import io

# === Audio Processing Utilities ===
def bandpass(data, lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low, high = lowcut / nyq, highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return lfilter(b, a, data)

def estimate_morse_tone_frequency(y, sr):
    y_segment = y[:min(len(y), sr * 5)]
    freqs, psd = welch(y_segment, sr, nperseg=2048)
    valid = (freqs > 300) & (freqs < 2000)
    return freqs[valid][np.argmax(psd[valid])] if np.any(valid) else 1000

def load_audio_from_file(file):
    y, sr = sf.read(io.BytesIO(file.read()))
    if y.ndim > 1:
        y = y.mean(axis=1)
    return y / np.max(np.abs(y)), sr

def load_audio_from_bytes(audio_bytes):
    y, sr = sf.read(io.BytesIO(audio_bytes.getvalue()))
    if y.ndim > 1:
        y = y.mean(axis=1)
    return y / np.max(np.abs(y)), sr
