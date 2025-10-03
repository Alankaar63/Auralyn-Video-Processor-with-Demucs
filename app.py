import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify, session
from audio_processing import extract_audio, seperate_voice, recombine_audio_with_video
from transcribe import transcribe_whisper
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__)
app.secret_key = 'cc2f2e8035fa2eda0961fe9725770058'

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def process_video():
    if "file" not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    if file.filename == "":
        return "Empty Filename", 400

    # Save uploaded video
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(video_path)

    # Extract audio
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4()}.wav")
    extract_audio(video_path, audio_path)

    # Separate voice
    voice_path = seperate_voice(audio_output_path=audio_path, output_dir=app.config['OUTPUT_FOLDER'])

    # Transcribe
    transcription = transcribe_whisper(voice_path)
    session['transcription'] = transcription  # save for chatbot use

    # Recombine cleaned audio with video
    final_video_path = os.path.join(app.config['OUTPUT_FOLDER'], f"processed_{file.filename}")
    recombine_audio_with_video(video_path, voice_path, final_video_path)

    return render_template(
        "result.html",
        transcription=transcription,
        vocals_file=os.path.basename(voice_path),
        video_file=os.path.basename(final_video_path),
    )

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form.get('message', '')
    if not user_message:
        return jsonify({'reply': "Please enter a message."})

    transcription = session.get('transcription', '')[:200]

    # Only add transcription if message seems related to video
    if user_message.lower() in ["hi", "hello", "hey", "how are you"]:
        prompt = f"User: {user_message}\nBot:"
    else:
        prompt = f"Video transcription (short snippet): {transcription}\nUser: {user_message}\nBot:"

    model = genai.GenerativeModel("gemini-2.5-flash-preview-09-2025")
    response = model.generate_content(prompt)

    return jsonify({'reply': response.text})




@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

# For local testing
# if __name__ == "__main__":
#     app.run(debug=True)

# For Docker deployment
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=False)

