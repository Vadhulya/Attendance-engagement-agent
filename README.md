# Attendance-engagement-agent
Prerequisites & System Requirements
Python: Version 3.8 or above (Python 3.12 fully supported via OpenCV backend)

Hardware: Webcam and microphone enabled

OS: Windows 10/11, macOS, or Linux

Installation & Setup
Clone or navigate to the project directory:

Bash
cd attendance-engagement-agent
Install dependencies:

Bash
pip install opencv-python opencv-contrib-python pyaudio numpy pandas streamlit
(Note: On Windows, if pyaudio fails via standard pip, install via pip install pipwin followed by pipwin install pyaudio.)

Add Reference Photos:
Create the reference directory and place clear, front-facing student photos inside:

Bash
mkdir -p data/known_faces
Name each image file with the student's identifier (e.g., Alice.jpg, Bob.png).

Running the Application
Launch the Streamlit dashboard:

Bash
python -m streamlit run app.py
