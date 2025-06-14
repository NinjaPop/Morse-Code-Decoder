# 🔊 Morse Code Decoder (Streamlit App)

A modern, interactive web app for decoding Morse code audio signals — either from uploaded .wav files or real-time microphone input. Powered by signal processing, clustering, and dynamic UI features built with Streamlit.

# 🎯 Features

- **Live microphone input** or 📁 **.wav file upload**
- **Interactive spectrogram viewer** using Plotly
- **Bandpass filter slider** with auto-detected Morse tone frequency
- **Dot/dash detection** via KMeans clustering
- **Editable Morse code string** with real-time decoding
- **AI-assisted word correction** using fuzzy matching
- **Recording export** (for mic input)
- Multiple detection modes (Standard, Gap Merge, High Precision)
- Optimized for decoding noisy or clean signals with option to enhance even further using the “Enhance” option


# 🚀 Getting Started

## 🔧 Requirements

Install the dependencies using pip:

```pip install -r requirements.txt```

requirements.txt includes:

streamlit

numpy

scipy

soundfile

sounddevice

scikit-learn

plotly


## 📦 Clone & Run Locally

    git clone https://github.com/NinjaPop/Morse-Code-Decoder.git

    cd morse--code-decoder

run the app.py via cmd:

    streamlit run app.py

or open the ```run_morse_code_decoder.py via VS-Code or any python IDE``` and run it.

The app will open in your default web browser. If not, go to the URL shown in your terminal ```(usually http://localhost:8501)```

# 🧭 How to Use the App
## Option A: 📁 Upload a .wav file

- Click “Upload a .wav file”

- Adjust the Bandpass Filter slider, ideally move it to where you see the morse pattern in the spectogram (can also auto-detect Morse tone)

- Toggle Enhance for Microphone Recording if needed

- View the interactive spectrogram (zoom in or out)

- Review the detected Morse code

- (Optional) Edit the Morse string manually (if un-clear, look at the spectogram and edit the morse code manually)

- See the decoded message and the AI-corrected guess

- Use “Reset to Detected Morse” if you need to undo your edits

## Option B: 🎙 Use Microphone Mode

- Click “🎙️ Switch to Microphone Mode”

- Click Start Microphone Input

- Press Record (allow browser permission)

- After recording, audio is auto-processed

- You can download the .wav, view the spectrogram, and continue as above

## 🧪 Audio Format Guidelines

- Only .wav files are supported

- Use 44.1kHz mono audio for best accuracy

- Compressed formats like .mp3 are not supported

## 🧪 Detection Modes
Choose between the different modes to see if the decoded text becomes clearer

- Standard (Merged) – Smooth balance between speed and accuracy
- Short Gap Merge (<10ms) – Fixes broken signals from noisy inputs (if the gap between the nodes are about 10ms use this)
- High Precision (No Merge) – Great for tightly spaced signals (use this option if the gap between the nodes are super tiny)

## 👩‍💻 For Developers

You can directly use modules like detect_morse(), decode_morse(), or ai_guess_words() from utils/morse.py in your own tools.

Modular, testable structure with:

```Isolated audio logic (utils/audio.py)```

```Clean UI (components/ui.py)```

```Editable Morse dictionary (utils/constants.py)```

**PRs, issues, and feature suggestions are welcome.**

## 📜 License & Terms of Use

This project is licensed under the GNU General Public License v3.0.
You are free to use, modify, and share this project — as long as:

- Derivative works remain open source

- You include proper attribution

- You do not use it commercially unless GPL-compatible

[Read the full license here »](https://www.gnu.org/licenses/gpl-3.0.html)

## 🙌 Acknowledgements

Morse timing and decoding principles based on ITU standard

Audio handling via streamlit's builtin st.audio_input and soundfile

Spectrograms via scipy.signal and plotly

Fuzzy matching via difflib
