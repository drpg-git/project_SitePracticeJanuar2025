from flask import Flask, request, send_from_directory, jsonify, send_file
import os
import time
import json
import io
import sys
import random
import threading
import webbrowser
from flask import jsonify
from werkzeug.utils import secure_filename


# =========================
# PyInstaller helper
# =========================
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# =========================
# Flask app
# =========================
app = Flask(
    __name__,
    static_folder=resource_path('.'),
    template_folder=resource_path('.')
)


# =========================
# Paths
# =========================
UPLOAD_FOLDER = resource_path('avatars')
STATUS_FILE = resource_path('status.json')
PROFILE_FILE = resource_path('profile.json')
PRESENTS_DIR = resource_path('presents')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =========================
# Init files
# =========================
def init_files():
    if not os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'w', encoding='utf-8') as f:
            json.dump(
                {"text": "В предвкушении праздника", "emoji": "🎄"},
                f,
                ensure_ascii=False
            )

    if not os.path.exists(PROFILE_FILE):
        default_profile = {
            "name": "Ципринский Илья",
            "group": "П24-2г · Политех",
            "birth": "2008",
            "field": "ИТ",
            "form": "Очная",
            "skin": "Белый",
            "orientation": "Гетеро",
            "interests": "Web, JS, UI",
            "about": "Программист и исследователь. Люблю создавать красивые вещи.",
            "skills": "HTML5, CSS3, JavaScript, Python",
            "projects": "Project Alpha, Winter Portfolio",
            "contacts": "ilya.dev@newyear.ru"
        }
        with open(PROFILE_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_profile, f, ensure_ascii=False, indent=4)


init_files()


# =========================
# Routes
# =========================
@app.route('/')
def index():
    return send_from_directory(resource_path('.'), 'index.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('avatar')
    if not file:
        return jsonify({'error': 'no file'}), 400

    filename = f"{int(time.time())}_{secure_filename(file.filename)}"
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    return jsonify({'path': f'/avatars/{filename}'})


@app.route('/latest-avatar')
def latest_avatar():
    files = [
        f for f in os.listdir(UPLOAD_FOLDER)
        if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))
    ]
    if not files:
        return jsonify({'path': None})

    files.sort(key=lambda x: os.path.getmtime(os.path.join(UPLOAD_FOLDER, x)))
    return jsonify({'path': f'/avatars/{files[-1]}'})


@app.route('/avatars-list')
def avatars_list():
    files = [
        f for f in os.listdir(UPLOAD_FOLDER)
        if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))
    ]
    files.sort(
        key=lambda x: os.path.getmtime(os.path.join(UPLOAD_FOLDER, x)),
        reverse=True
    )
    return jsonify({'avatars': [f'/avatars/{f}' for f in files]})


@app.route('/get-status')
def get_status():
    with open(STATUS_FILE, 'r', encoding='utf-8') as f:
        return jsonify(json.load(f))


@app.route('/set-status', methods=['POST'])
def set_status():
    with open(STATUS_FILE, 'w', encoding='utf-8') as f:
        json.dump(request.json, f, ensure_ascii=False)
    return jsonify({"status": "ok"})


@app.route('/get-profile')
def get_profile():
    with open(PROFILE_FILE, 'r', encoding='utf-8') as f:
        return jsonify(json.load(f))


@app.route('/set-profile', methods=['POST'])
def set_profile():
    with open(PROFILE_FILE, 'w', encoding='utf-8') as f:
        json.dump(request.json, f, ensure_ascii=False, indent=4)
    return jsonify({"status": "ok"})


@app.route('/avatars/<name>')
def avatar(name):
    return send_from_directory(UPLOAD_FOLDER, name)


# =========================
# Games
# =========================
@app.route('/game/puzzles')
def puzzles_game():
    return send_from_directory(resource_path('.'), 'game/puzzles.html')


@app.route('/game/grinch')
def grinch_game():
    return send_from_directory(resource_path('.'), 'game/game.html')


@app.route('/game/ratatype')
def ratatype_game():
    return send_from_directory(resource_path('.'), 'game/ratatype.html')


@app.route('/game/gd')
def gd_game():
    return send_from_directory(resource_path('.'), 'game/gd.html')


@app.route('/game/photo')
def photo_game():
    return send_from_directory(resource_path('.'), 'game/photo.html')


@app.route('/game/dino')
def dino_game():
    return send_from_directory(resource_path('.'), 'game/dino.html')


@app.route('/game/ilya')
def ilya_game():
    return send_from_directory(resource_path('.'), 'ilya.html')


@app.route('/game/clicker')
def clicker_game():
    return send_from_directory(resource_path('.'), 'game/clicker.html')


# =========================
# Practice
# =========================
@app.route('/practice/first')
def practic_first():
    return send_from_directory(resource_path('.'), 'practice/first.html')


@app.route('/practice/second')
def practic_second():
    return send_from_directory(resource_path('.'), 'practice/second.html')


@app.route('/practice/third')
def practic_third():
    return send_from_directory(resource_path('.'), 'practice/third.html')


@app.route('/practice/first_exchanged')
def practic_first_exchanged():
    return send_from_directory(resource_path('.'), 'practice/first_exchanged.html')


@app.route('/practice/second_exchanged')
def practic_second_exchanged():
    return send_from_directory(resource_path('.'), 'practice/second_exchanged.html')


@app.route('/practice/third_exchanged')
def practic_third_exchanged():
    return send_from_directory(resource_path('.'), 'practice/third_exchanged.html')


@app.route('/practice/menu')
def practic_menu():
    return send_from_directory(resource_path('.'), 'practice/menu.html')


@app.route('/portfolio')
def portfolio():
    return send_from_directory(resource_path('.'), 'index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(resource_path('.'), filename)


# =========================
# Presents
# =========================
@app.route('/get-random-present')
def get_random_present():
    try:
        if not os.path.exists(PRESENTS_DIR):
            return jsonify({'path': None, 'error': 'Directory not found'}), 404

        files = [
            f for f in os.listdir(PRESENTS_DIR)
            if os.path.isfile(os.path.join(PRESENTS_DIR, f))
        ]

        if not files:
            return jsonify({'path': None, 'error': 'No files in directory'}), 404

        random_file = random.choice(files)
        return jsonify({'path': f'/presents/{random_file}'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/presents/<name>')
def serve_present(name):
    return send_from_directory(PRESENTS_DIR, name)


# =========================
# Remove background (AI) — ленивый импорт
# =========================
@app.route('/remove-bg', methods=['POST'])
def remove_bg_api():
    from rembg import remove
    from PIL import Image

    if 'image' not in request.files:
        return jsonify({'error': 'No file'}), 400

    file = request.files['image']
    input_image = Image.open(file.stream)

    output_image = remove(input_image)

    img_io = io.BytesIO()
    output_image.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')


# =========================
# Shutdown route
# =========================
@app.route('/shutdown', methods=['POST'])
def shutdown():
    def terminate():
        time.sleep(1) 
        os._exit(0)
    
    threading.Thread(target=terminate).start()
    return jsonify({"success": True, "message": "Server is shutting down..."})


# =========================
# Run
# =========================
def open_browser():
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == '__main__':
    threading.Timer(1.5, open_browser).start()
    app.run(debug=False, port=5000)
