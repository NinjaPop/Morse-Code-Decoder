# 🔊 Morse Code Decoder

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

**If you have Dark Reader browser extension make sure to disable it for this app as it will cause some issues**

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

    cd morse-code-decoder

run the app.py via cmd:

    streamlit run app.py

or open the ```run_morse_code_decoder.py via VS-Code or any python IDE``` and run it.

The app will open in your default web browser. If not, go to the URL shown in your terminal ```(usually http://localhost:8501)```

# 🧭 How to Use the App
## Before proceeding with Option A, try and do this step for an easier time, if on a PC or laptop:

- on Windows 11 go to sound settings
  
- scroll download to Advanced section
  
- click on All sound devices
  
- scroll down on input devices and click on Stereo Mix
  
- allow the audio
  
- go back to sound settings main page
  
- in input, select Stereo Mix as microphone input

Now when you play an audio on your desktop it will loopback as microphone input to the app and you wont have to upload or record an audio through a microphone,
you just play the audio on your browser or if its a game in-game and click on record button on the app to start hearing that audio

Troubleshoot: if you cannot hear the Stereo Mix when playing an audio, make sure to select Speakers (Realtek(R) Audio) and do a test by clicking on the Stereo Mix in sound setting and testing.

## Option A: 📁 Upload a .wav file

- Open (https://morse-code-decoder.streamlit.app/) in your phone browser or on your desktop browser

- Tap 🎙 Switch to Microphone Mode

- Tap 🎙 Start Microphone Input

- Allow browser access to your microphone if prompted

- Play the Morse audio from the game or recording if you have that and put your microphone or phone near the speaker

- Once done, stop recording. The app will analyze the audio automatically.

- You can re-play the recorded audio to listen back to how it sounds (test out to see if your phone has silenced or distorted the sounds of the Morse code)

- you can download the recorded-audio if you want as well

- after analyzing the recorded sound, the app will show you:

    - The resulting spectrogram of the recording
    - the estimated Morse frequency (the app is smart enough to notice the Morse code pattern within the spectrogram and pre-select the band frequency)
    - The decoded Morse string (this is editable, so if you want you can manually edit this to change the output or look at the spectrogram and edit this yourself)
    - The decoded Morse in text
    - An AI guessor

```Note: some phones do have high noise cancellation so it might reduce the sound of the Morse code or make it silent, in such cases, try bringing the phone closer to the speaker or in some cases reduce the volume of the speaker so that it does not cancel it as much.```

**If none of the above works, record the audio from the speakers using your phone's voice recorder (every phone has this app) or download a voice recording app from apple store or google play store, make sure it saves the recording as .wav though and follow Option 2 below**

### 🎧 Tips for best results:

- Get close to the sound source

- Keep background noise low

- You can also use the “🎙 Enhance for Microphone Recording” to boost weak signals (although if your phone is already silencing the morse code's audio this might make it worse)

### 🧪 Optional Tweaks:

Use the bandpass filter slider to zero in on the Morse frequency (~800 to 850 Hz), every audio uploaded to this app will generate a spectogram and you most likely will be able to see the dot and dashes in a straight horizontal line, just try and move the slider so it focuses perfectly within the height of those bands (For all the morse code tests I have done on BF1, it almost always has the Morse code from around 750 to 830 Hz). 

## Option B: 🎙 Use Microphone Mode

- Open (https://morse-code-decoder.streamlit.app/) in your browser (desktop or mobile)

- Use the default File Upload Mode

- Upload your .wav file (you can record the sound of the Morse code via a voice recording app on your phone or record from your desktop microphone)

- The app will immediately process the signal and show:

    - The spectrogram
    - The estimated Morse frequency
    - The decoded Morse string (this is editable, so if you want you can manually edit this to change the output or look at the spectrogram and edit this yourself)
    - The decoded Morse in text
    - An AI guessor

### 🧪 You can improve the results by:

- Adjusting the frequency filter slider

- **Trying different Detection Modes:**

    - Standard (Merged) – balanced and fast
    - Short Gap Merge (<10ms) – fixes slight signal breaks, if the gaps between the nodes are tiny use this
    - High Precision (No Merge) – clean for clearly spaced taps

You can also edit the morse code string directly, just look at the spectrogram and edit the morse code according to it and it will update the text with your changes (at the top you can toggle the show decoded spectrogram and it will filter the spectrogram so that you can see the Morse code better).

**Remember! - not every Morse code will be decoded perfectly using this, but this will help you decode most of battlefield 1's morse codes easily, all you need is some clue as to what the morse code might be and search for that text or sentence in (https://wiki.bfee.co/BF1) battlefield 1 wiki and you will almost always find your decoded text.** 

## 🧪 Audio Format Guidelines

- Only .wav files are supported

- Use 44.1kHz mono audio for best accuracy

- Compressed formats like .mp3 are not supported


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
