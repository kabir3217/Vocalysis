# Vocalysis
A tool that aims to be more of a guide or mentor for students, helping them find direction in their study habits. This project is an innovative tool designed to help students by analyzing their handwritten notes. After a student scans their notes, the application uses AI to provide crucial feedback on three key areas: focus, clarity and content..

AI-Powered Speech Analysis Tool
Vocalysis is a web application designed to help students and professionals improve their public speaking and communication skills. By uploading an audio recording, users receive instant, AI-driven feedback on their speech, scored on a scale of 1 to 10 across several key metrics.

The application features a dynamic, interactive 3D frontend and a powerful Python backend, making speech analysis simple and engaging.

(Suggestion: Replace the URL above with a screenshot of your running application)

Key Features:
Comprehensive Analysis: Get scores for Confidence, Clarity, Ambition, Mood, Grammar, and Professionalism.

AI-Powered Transcription: Utilizes OpenAI's Whisper model for highly accurate speech-to-text conversion.

Interactive Web Interface: Features a dynamic 3D frontend built with Three.js, allowing users to drag and drop multiple audio files at once.

Data Export: Download your analysis results to a CSV file to easily track your progress over time.

Tech Stack:
Backend: Python, Flask

AI/ML: OpenAI Whisper, NLTK, language-tool-python, Librosa

Frontend: HTML, Tailwind CSS, Three.js

Installation & Setup
Follow these steps to get the Vocalysis application running on your local machine.

1. Clone the Repository:

git clone https://github.com/your-username/vocalysis.git
cd vocalysis

2. Create a Virtual Environment (Recommended):

# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies:
Make sure you have all the required Python packages by running:

pip install -r requirements.txt

(Note: You will need to create a requirements.txt file. See the section below.)

4. Install FFmpeg:
The pydub library requires FFmpeg to process different audio formats like MP3.

Windows: Download the binaries from ffmpeg.org and add the bin folder to your system's PATH.

macOS (using Homebrew): brew install ffmpeg

Linux (using apt): sudo apt update && sudo apt install ffmpeg

How to Use
1. Run the Flask Server:
Once the setup is complete, start the backend server by running:

python main.py

The terminal will indicate that the server is running, usually on http://127.0.0.1:5000.

2. Open the Web Interface:
Open your web browser and navigate to http://127.0.0.1:5000.

3. Upload Audio Files:
Drag and drop one or more audio files (WAV, MP3, M4A, FLAC) into the upload zone, or click to select them from your computer.

4. View and Export Results:
The analysis will begin automatically. Once complete, the results will appear in a table. You can then click the "Export to Excel (CSV)" button to save your report.

Creating the requirements.txt File
For easy installation, create a file named requirements.txt in your main project folder and add the following lines to it:

Flask
openai-whisper
pydub
language-tool-python
nltk
librosa
numpy

Project Structure
The project is organized into the following directories and files:

VOCAL_ANALYZER/
├── main.py              # The main Flask web server application
├── vocalysis.py         # The core analysis library and functions
├── requirements.txt     # A list of all Python dependencies
├── templates/
│   └── index.html       # The frontend HTML and JavaScript file
└── uploads/             # A temporary folder for storing uploaded audio files

