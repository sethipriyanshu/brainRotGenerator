from flask import Flask, request, jsonify, render_template, send_from_directory
from main import main
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('app.html')

@app.route('/generate', methods=['POST'])
def generate():
    print("Received request at /generate")  # Debugging statement
    data = request.get_json()
    link = data.get('link', '').strip()
    character = data.get('character', 'trump').strip().lower() or 'trump'
    print(f"Link: {link}, Character: {character}")  # Debugging statement

    if not link:
        return jsonify({'error': 'Missing Reddit link.'}), 400

    try:
        # Always treat this as a single post URL (thread mode removed for UI).
        main(link, llm=False, asset_name=character)
    except Exception as e:
        # Surface a clear error back to the client instead of a 500 stack trace
        print(f"Error during video generation: {e}")  # Debugging / logging
        return jsonify({'error': str(e)}), 500

    # Assuming the video is saved as 'subway.mp4' in the 'assets' directory
    video_filename = 'final.mp4'
    video_path = os.path.join('final', video_filename)
    if os.path.exists(video_path):
        print("Video generation successful")  # Debugging statement
        return jsonify({'video_url': f'/final/{video_filename}'})
    else:
        print("Video generation failed")  # Debugging statement
        return jsonify({'error': 'Video generation failed'}), 500

@app.route('/final/<path:filename>')
def serve_video(filename):
    return send_from_directory('final', filename)

if __name__ == "__main__":
    app.run(debug=True)