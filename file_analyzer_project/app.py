import os
import hashlib
import json
import pandas as pd
import plotly.express as px
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
        # Зчитуємо вміст файлу
        file_content = file.read()
        # Створюємо хеш SHA-256 з вмісту файлу
        file_hash = hashlib.sha256(file_content).hexdigest()[:16]  # Беремо перші 16 символів хешу
        
        # Отримуємо розширення файлу
        file_ext = os.path.splitext(file.filename)[1]
        # Створюємо нове ім'я файлу: оригінальне_ім'я_хеш.розширення
        safe_name = secure_filename(file.filename)
        filename = f"{os.path.splitext(safe_name)[0]}_{file_hash}{file_ext}"
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Зберігаємо файл
        with open(filepath, 'wb') as f:
            f.write(file_content)
        
        response = {
            'success': True,
            'message': f'Файл {filename} успішно завантажено',
            'filename': filename
        }
        return jsonify(response)
    
    return jsonify({'success': False, 'message': 'Дозволено лише файли формату .csv'}), 400

@app.route('/analyze', methods=['POST'])
def analyze_file(start_year: int = 2018):
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

        # convert Date Read to datetime and add new columns
        df['Date Read'] = pd.to_datetime(df['Date Read'])
        df['year_read'] = df['Date Read'].dt.year
        df['month_read'] = df['Date Read'].dt.month
        df['finished_week_day'] = df['Date Read'].dt.dayofweek
        df['finished_week_day_name'] = df['Date Read'].dt.day_name()

        df_read = df[df['Exclusive Shelf'] == 'read']
        df_read.loc[:, 'Date Read'] = df_read.loc[:, 'Date Read'].fillna(df_read['Date Added'])

        df_read = df_read[df_read['year_read'] >= start_year]
        
        books_per_year = df_read['year_read'].value_counts().sort_index()

        # Переконуємось, що всі роки відображаються як категорії
        years = books_per_year.index.astype(int).astype(str).tolist()
        values = books_per_year.values.tolist()
        
        # Створюємо графік з підписами
        graph_data = {
            'data': [{
                'x': years,
                'y': values,
                'type': 'bar',
                'text': values,  # Показує значення над стовпцями
                'textposition': 'auto',  # Автоматичне розташування тексту
                'texttemplate': '%{y}',  # Формат тексту (показуємо тільки значення Y)
                'hoverinfo': 'x+text',   # Показуємо рік і кількість при наведенні
            }],
            'layout': {
                'title': 'Кількість прочитаних книг за роками',
                'xaxis': {
                    'title': 'Рік',
                    'type': 'category',  # Це змушує відображати всі роки
                    'tickmode': 'array',
                    'tickvals': years,   # Всі роки як мітки
                    'ticktext': years    # Відображаємо всі роки
                },
                'yaxis': {
                    'title': 'Кількість книг',
                    'rangemode': 'tozero'  # Починаємо вісь Y з 0
                },
                'showlegend': False  # Приховуємо легенду, вона нам не потрібна
            }
        }
        
        analysis = {
            'graph': json.dumps(graph_data)
        }
        
        return jsonify({'success': True, 'analysis': analysis})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Помилка аналізу: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
