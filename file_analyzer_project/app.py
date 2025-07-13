import os
import pandas as pd
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Конфігурація папки для завантажень
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Створення папки для завантажень, якщо її не існує
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Перевіряє, чи має файл дозволене розширення."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'Файл не знайдено'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'success': False, 'message': 'Файл не вибрано'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        response = {
            'success': True,
            'message': f'Файл {filename} успішно завантажено',
            'filename': filename
        }
        return jsonify(response)
    
    return jsonify({'success': False, 'message': 'Дозволено лише файли формату .csv'}), 400

@app.route('/analyze', methods=['POST'])
def analyze_file():
    data = request.get_json()
    filename = data.get('filename')

    if not filename:
        return jsonify({'success': False, 'message': 'Ім\'я файлу не передано'}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if not os.path.exists(filepath):
        return jsonify({'success': False, 'message': 'Файл не знайдено на сервері'}), 404

    try:
        # Аналіз CSV файлу з Goodreads
        df = pd.read_csv(filepath)

        # Перевіряємо наявність необхідної колонки
        if 'Date Read' not in df.columns:
            return jsonify({'success': False, 'message': 'У файлі відсутня колонка "Date Read"'}), 400

        # Видаляємо книги без дати прочитання та конвертуємо колонку в datetime
        df.dropna(subset=['Date Read'], inplace=True)
        df['Date Read'] = pd.to_datetime(df['Date Read'], errors='coerce')
        df.dropna(subset=['Date Read'], inplace=True)

        # Рахуємо книги за роками
        df['Year Read'] = df['Date Read'].dt.year
        books_per_year = df['Year Read'].value_counts().sort_index().to_dict()

        analysis = {
            'Книг прочитано за роками': books_per_year
        }
        
        return jsonify({'success': True, 'analysis': analysis})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Помилка аналізу: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
