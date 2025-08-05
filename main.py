
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import time
import werkzeug

# Import the analysis engine we created earlier
from vocalysis_analyzer import run_full_analysis

# Initialize the Flask app
app = Flask(__name__, template_folder='templates')

# Enable CORS (Cross-Origin Resource Sharing) to allow our frontend
# to communicate with this server.
CORS(app)

# --- Configuration ---
# Define a folder to temporarily store uploaded files for analysis
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# --- API Endpoint for Analysis ---
@app.route('/analyze', methods=['POST'])
def analyze_audio():
    """
    This function is called when a file is sent to the /analyze endpoint.
    """
    # Check if a file was sent in the request
    if 'audio_file' not in request.files:
        return jsonify({"error": "No audio file part in the request"}), 400

    file = request.files['audio_file']

    # Check if a file was actually selected
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        # Secure the filename to prevent directory traversal issues
        filename = werkzeug.utils.secure_filename(file.filename)
        
        # Save the file to our temporary upload folder
        temp_audio_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(temp_audio_path)

        # --- Run the Core Analysis ---
        try:
            analysis_results = run_full_analysis(temp_audio_path)
        except Exception as e:
            # Handle potential errors during analysis
            # This is a fallback for unexpected errors in the analyzer.
            return jsonify({"error": f"Analysis failed unexpectedly: {str(e)}"}), 500
        finally:
            # --- Clean Up ---
            # Robustly remove the temporary file after analysis.
            # Add a small delay to ensure the file lock is released.
            time.sleep(0.1) # Wait 100ms
            if os.path.exists(temp_audio_path):
                try:
                    os.remove(temp_audio_path)
                except OSError as e:
                    # Log if the file couldn't be removed, but don't crash.
                    print(f"Error removing file {temp_audio_path}: {e}")


        # Check if the analysis itself returned an error (like a loading issue)
        if "error" in analysis_results:
             return jsonify(analysis_results), 500

        # --- Success ---
        # Return the results as a JSON object
        return jsonify(analysis_results)

    return jsonify({"error": "An unknown error occurred"}), 500


# --- Route to Serve the Frontend ---
@app.route('/')
def home():
    """
    This function serves the main index.html page.
    """
    return render_template('index.html')


# --- Main Execution ---
if __name__ == '__main__':
    # Run the Flask app. `debug=True` allows for auto-reloading when you save changes.
    # The host '0.0.0.0' makes it accessible on your local network.
    app.run(host='0.0.0.0', port=5000, debug=True)
