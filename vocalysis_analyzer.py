# vocalysis_analyzer.py (Stable Version with pydub)
# This file contains all the core analysis functions.
# It uses the pydub library for robust loading of all audio formats.
#
# -----------------
# --- SETUP ---
# -----------------
# Ensure you have: pip install Flask flask_cors librosa numpy openai-whisper pydub
# And that ffmpeg is installed on your system.
# -----------------

import librosa
import numpy as np
import math
import whisper
import os
import io
import warnings

# --- Suppress the harmless "Couldn't find ffmpeg" warning from pydub ---
with warnings.catch_warnings():
    warnings.simplefilter("ignore", RuntimeWarning)
    from pydub import AudioSegment

# --- !! IMPORTANT CONFIGURATION !! ---
# Set the correct, full path to your ffmpeg.exe.
# To find the path, run `Get-Command ffmpeg.exe` in PowerShell.
# The `r` before the quote is important - DO NOT DELETE IT.
FFMPEG_PATH = r"C:\ProgramData\chocolatey\bin\ffmpeg.exe"

if os.path.exists(FFMPEG_PATH):
    AudioSegment.converter = FFMPEG_PATH
    print(f"Successfully set ffmpeg path to: {FFMPEG_PATH}")
else:
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!! WARNING: FFMPEG PATH NOT FOUND OR INCORRECT !!!")
    print(f"!!! Path set in script: '{FFMPEG_PATH}'")
    print("!!! Please update the FFMPEG_PATH variable in this file.")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


# --- HELPER FUNCTIONS ---

def normalize_score(value, min_val, max_val, reverse=False):
    """Normalizes a value to a 0-10 scale."""
    value = max(min(value, max_val), min_val)
    normalized = (value - min_val) / (max_val - min_val)
    if reverse:
        return (1 - normalized) * 10
    return normalized * 10

# --- CORE ANALYSIS FUNCTIONS ---

def analyze_clarity(y, sr):
    """Analyzes the clarity of speech based on vocal stability (jitter and shimmer)."""
    try:
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_values = [pitches[magnitudes[:, t].argmax(), t] for t in range(pitches.shape[1]) if pitches[magnitudes[:, t].argmax(), t] > 0]
        if len(pitch_values) < 2: return 0.0
        jitter = np.mean(np.abs(np.diff(pitch_values)))
        shimmer = np.mean(np.abs(np.diff(librosa.feature.rms(y=y)[0])))
        clarity_score = (normalize_score(jitter, 0, 5, reverse=True) + normalize_score(shimmer, 0, 0.1, reverse=True)) / 2
        return clarity_score
    except Exception:
        return 0.0

def analyze_confidence(y, sr, transcribed_text):
    """Analyzes confidence from volume stability and lack of filler words."""
    try:
        volume_stability_score = normalize_score(np.std(librosa.feature.rms(y=y)[0]), 0, 0.1, reverse=True)
        words = transcribed_text.lower().split()
        if not words: return volume_stability_score
        filler_count = sum(1 for word in words if word in ["um", "uh", "like", "you know", "so", "actually", "basically"])
        filler_ratio = filler_count / (len(words) / 100.0) if words else 0
        filler_word_score = normalize_score(filler_ratio, 0, 10, reverse=True)
        return (volume_stability_score + filler_word_score) / 2
    except Exception:
        return 0.0

def analyze_energy_engagement(y, sr):
    """Analyzes energy/engagement via pitch range and speech rate."""
    try:
        pitches, _ = librosa.piptrack(y=y, sr=sr)
        pitch_values = pitches[pitches > 0]
        duration = librosa.get_duration(y=y, sr=sr)
        if duration == 0: return 0.0
        pitch_range_score = normalize_score(np.ptp(pitch_values) if len(pitch_values) > 1 else 0, 50, 250)
        speech_rate_score = normalize_score(len(librosa.onset.onset_detect(y=y, sr=sr)) / duration, 2, 6)
        return (pitch_range_score + speech_rate_score) / 2
    except Exception:
        return 0.0

def placeholder_mood_analysis():
    """Placeholder for a real Speech Emotion Recognition (SER) model."""
    return {"Status": "Not Implemented"}

def placeholder_professionalism_score(clarity, confidence):
    """Placeholder for the composite professionalism score."""
    if clarity is None or confidence is None:
        return "Not Calculated"
    return (clarity + confidence) / 2

# --- Main Analysis Runner ---
print("Loading Whisper STT model...")
whisper_model = whisper.load_model("base")
print("Whisper model loaded.")


def run_full_analysis(audio_path):
    """
    A single function to run all analyses on a given audio file path.
    """
    print(f"Processing file: {audio_path}...")
    try:
        # Use pydub to robustly load any audio format from the given path
        audio_segment = AudioSegment.from_file(audio_path)
        
        # Convert to a standard format (mono, 16kHz) for consistent analysis
        audio_segment = audio_segment.set_channels(1).set_frame_rate(16000)

        # Export to an in-memory WAV format bytes buffer
        wav_buffer = io.BytesIO()
        audio_segment.export(wav_buffer, format="wav")
        wav_buffer.seek(0)

        # Load the WAV data from the in-memory buffer using librosa
        y, sr = librosa.load(wav_buffer, sr=16000)

    except Exception as e:
        return {"error": f"Could not load audio file: {e}"}

    # Handle silent audio arrays
    if np.max(np.abs(y)) < 0.001:
        return {
            "Clarity Score": 0.0,
            "Confidence Score": 0.0,
            "Energy & Engagement Score": 0.0,
            "Professionalism Score": 0.0,
            "Mood Analysis": "Not Implemented",
            "Transcription": "Audio is silent or contains no speech."
        }

    print("Transcribing audio data...")
    transcription_result = whisper_model.transcribe(y) # Transcribe from memory
    transcribed_text = transcription_result["text"]
    print(f"Transcription: '{transcribed_text}'")

    clarity_score = analyze_clarity(y, sr)
    confidence_score = analyze_confidence(y, sr, transcribed_text)
    engagement_score = analyze_energy_engagement(y, sr)
    professionalism_score = placeholder_professionalism_score(clarity_score, confidence_score)
    mood_report = placeholder_mood_analysis() # Added the missing function call

    return {
        "Clarity Score": float(clarity_score),
        "Confidence Score": float(confidence_score),
        "Energy & Engagement Score": float(engagement_score),
        "Professionalism Score": float(professionalism_score) if isinstance(professionalism_score, (int, float, np.number)) else "Not Calculated",
        "Mood Analysis": mood_report["Status"],
        "Transcription": transcribed_text
    }
