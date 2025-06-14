# Licensed under the GNU General Public License v3.0
# See LICENSE file or https://www.gnu.org/licenses/gpl-3.0.html for details.

import subprocess
import os

# Here is the script to run through the pyinstaller: pyinstaller --onefile --add-data "streamlit_morse_decoder_app.py;." run_streamlit_morse_decoder.py 
# Option A use if you want simplicity ma boy:
script_path = os.path.join(os.path.dirname(__file__), "app.py")
subprocess.run(["streamlit", "run", script_path])

# Option B, if you want some portability:
# def run_streamlit_app():
#     # When frozen by PyInstaller, app is extracted to _MEIPASS
#     if getattr(sys, 'frozen', False):
#         base_path = sys._MEIPASS
#     else:
#         base_path = os.path.dirname(__file__)

#     app_path = os.path.join(base_path, "morse_decoder_app.py")
#     subprocess.run(["streamlit", "run", app_path])

# if __name__ == "__main__":
#     run_streamlit_app()

