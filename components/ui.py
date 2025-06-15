# Licensed under the GNU General Public License v3.0
# See LICENSE file or https://www.gnu.org/licenses/gpl-3.0.html for details.

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.signal import spectrogram

from utils.audio import load_audio_from_file, load_audio_from_bytes, bandpass, estimate_morse_tone_frequency
from utils.morse import detect_morse, decode_morse, ai_guess_words

def render_main_ui():
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        st.title("🔊 Morse Code Decoder")
    with col2:
        st.markdown(
            "<div style='font-size:20px; text-align: right; color: gray;'>By MR</div>",
            unsafe_allow_html=True
        )

    if "use_live_input" not in st.session_state:
        st.session_state["use_live_input"] = False

    if not st.session_state["use_live_input"]:
        if st.button("🎙️ Switch to Microphone Mode"):
            st.session_state["use_live_input"] = True
            st.rerun()
    else:
        if st.button("📁 Switch to File Upload Mode"):
            st.session_state["use_live_input"] = False
            st.rerun()

    use_live_input = st.session_state["use_live_input"]

    uploaded_file = None
    audio_bytes = None

    if not use_live_input:
        uploaded_file = st.file_uploader("Upload a `.wav` file", type=["wav"])

    if use_live_input:
        if "mic_mode" not in st.session_state:
            st.session_state["mic_mode"] = "idle"
            st.session_state["mic_audio"] = None

        if st.session_state["mic_mode"] == "idle":
            if st.button("🎙️ Start Microphone Input"):
                st.session_state["mic_mode"] = "listening"
                st.rerun()

        elif st.session_state["mic_mode"] == "listening":
            st.info("🎤 Click on the microphone icon to start recording...")
            audio_data = st.audio_input("Record your Morse Code (press Stop when done)")
            if audio_data:
                st.session_state["mic_audio"] = audio_data
                st.session_state["mic_mode"] = "complete"
                st.rerun()

        elif st.session_state["mic_mode"] == "complete":
            st.success("✅ Audio captured successfully.")
            if st.button("🔄 Record Again"):
                st.session_state["mic_mode"] = "idle"
                st.session_state["mic_audio"] = None
                st.rerun()


    # === Unified Audio Processing ===
    if (not use_live_input and uploaded_file) or (use_live_input and st.session_state.get("mic_audio")):
        # Get audio from either source
        if use_live_input:
            audio_bytes = st.session_state["mic_audio"]
            y, sr = load_audio_from_bytes(audio_bytes)
            st.audio(audio_bytes, format="audio/wav")
            st.download_button(
                label="💾 Download Recording (.wav)",
                data=audio_bytes.getvalue(),
                file_name="recorded_audio.wav",
                mime="audio/wav"
            )
        else:
            y, sr = load_audio_from_file(uploaded_file)

        enhance_mic = st.checkbox(
            "🎙 Enhance the audio and narrow the threshold (focuses more on the band, removes static noises - May result in worse audio decoding when recorded from a poor microphone!!!)",
            value=False
        )

        show_changed_spectogram = st.checkbox(
            "🎙Show decoded spectogram? - Useful if you want to use the morse code manually",
            value=False
        )

        dominant_freq = estimate_morse_tone_frequency(y, sr)
        default_band = (int(dominant_freq - 40), int(dominant_freq + 40))

        st.subheader("🎚 Bandpass Filter")
        band_range = st.slider("Select Frequency Range (Hz)", 300, 2000, default_band, step=10)
        lowcut, highcut = band_range
        st.caption(f"Estimated Morse frequency: **~{int(dominant_freq)} Hz**")

        if show_changed_spectogram:
            # Apply bandpass filter BEFORE computing spectrogram
            if enhance_mic:
                center = (lowcut + highcut) // 2
                y_filtered = bandpass(y, center - 30, center + 30, sr)
            else:
                y_filtered = bandpass(y, lowcut, highcut, sr)

            # Now generate spectrogram using filtered signal
            f, t, Sxx = spectrogram(y_filtered, sr, nperseg=1024, noverlap=512)
        else:
            f, t, Sxx = spectrogram(y, sr, nperseg=1024, noverlap=512)

        S_db = 10 * np.log10(Sxx + 1e-10)
        fig = go.Figure(data=go.Heatmap(
            z=S_db,
            x=t, y=f,
            colorscale='Magma',
            zmin=np.min(S_db), zmax=np.max(S_db),
            hovertemplate='Time: %{x:.2f}s<br>Freq: %{y:.0f} Hz<br>Power: %{z:.1f} dB<extra></extra>'
        ))

        fig.add_shape(
            type="rect",
            x0=t[0], x1=t[-1],
            y0=lowcut, y1=highcut,
            line=dict(color="lime", width=2, dash="dot"),
            fillcolor="rgba(0,255,0,0.1)",
            layer="below"
        )

        fig.update_layout(
            title="📊 Spectrogram (Interactive)",
            xaxis_title="Time (s)",
            yaxis_title="Frequency (Hz)",
            height=450,
            hovermode="closest",
            dragmode="pan",
            margin=dict(l=20, r=20, t=30, b=30),
            yaxis=dict(range=[0, 2000]), # Only show up to 2kHz
        )

        st.plotly_chart(fig, use_container_width=True, config={
            "scrollZoom": True,
            "displayModeBar": True,
            "displaylogo": False
        })
        st.caption("⚠️ Hover tooltips may not work properly in Microsoft Edge. For full interactivity, use Chrome or Firefox.")

        if lowcut >= highcut:
            st.error("⚠️ Invalid frequency range: Lowcut must be less than Highcut.")
            st.stop()
        else:
            if enhance_mic:
                # Tighten the band to ±30 Hz
                center = (lowcut + highcut) // 2
                y_filtered = bandpass(y, center - 30, center + 30, sr)
            else:
                y_filtered = bandpass(y, lowcut, highcut, sr)

        # Select decoding mode
        mode = st.selectbox("Detection Mode", [
            "Standard (Merged)",
            "Short Gap Merge (<10ms)",
            "High Precision (No Merge)"
        ])

        morse_string, y_filtered, sr = detect_morse(y_filtered, sr, mode=mode, enhance=enhance_mic)
        decoded_text = decode_morse(morse_string)

        # Detect new file upload or mode change and reset session state accordingly
        current_file = uploaded_file.name if not use_live_input else "LIVE_MIC"
        current_mode = mode
        previous_file = st.session_state.get("last_uploaded_filename")
        previous_mode = st.session_state.get("last_mode_used")

        # Reset if new file or mode changed
        if current_file != previous_file or current_mode != previous_mode:
            st.session_state["morse_original"] = morse_string
            st.session_state["morse_edit"] = morse_string
            st.session_state["last_uploaded_filename"] = current_file
            st.session_state["last_mode_used"] = current_mode

        st.subheader("📡 Detected Morse (Editable Input)")

        # Render editable input field
        st.markdown("""
                <style>
                textarea {
                    font-size: 16px !important;
                    font-family: monospace !important;
                }
                </style>
            """, unsafe_allow_html=True)

        morse_input = st.text_area(
            label="Edit Morse Code Here (use . for dot, - for dash, space between letters, / between words):",
            value=st.session_state["morse_edit"],
            key="morse_text_input_box",
            height=120
        )

        # Update session state with the new value
        st.session_state["morse_edit"] = morse_input

        # Decode the user-provided Morse
        decoded_text = decode_morse(morse_input)

        # Show decoded result
        st.subheader("🧾 Decoded Text")
        st.markdown(
            f"<div style='font-size: 22px; font-weight: bold; color: #28a745;'>{decoded_text}</div>",
            unsafe_allow_html=True
        )

        #guessed = ai_guess_words(decoded_text)
        #if guessed != decoded_text:
        #    st.markdown(
        #        f"<div style='font-size: 22px; color: orange;'>🤖 AI Guess: <b>{guessed}</b></div>",
        #        unsafe_allow_html=True
        #    )

        if st.button("🔄 Reset to Detected Morse"):
            st.session_state["morse_edit"] = st.session_state["morse_original"]
            st.rerun()

        with st.expander("About this tool"):
            st.markdown("""
            This tool was created as a fun project to tackle the Battlefield 1 Peacekeeper Easter egg, and it's now open source!  
            You can view or contribute to the code on <a href="https://github.com/NinjaPop/Morse-Code-Decoder" target="_blank">GitHub</a>.

            *Measure. Uncover. Signal Alignment.*
            """, unsafe_allow_html=True)

        st.markdown("""
            <div style='text-align: center; font-size: 16px; margin-top: 40px;'>
                Was the app helpful? <a href="https://github.com/NinjaPop/Morse-Code-Decoder" target="_blank">Give it a ⭐ on GitHub</a>!
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <hr style='border-top: 1px solid #bbb; margin-top: 30px;'>
        <div style='text-align: center; font-size: 14px; color: gray;'>
            Measure. Uncover. Signal Alignment.
        </div>
        """, unsafe_allow_html=True)

    else:
        st.info("Please upload a `.wav` file to begin decoding.")
