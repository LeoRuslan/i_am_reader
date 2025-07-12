from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Створюємо директорію для завантажених файлів
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    print('Upload request received')
    
    if 'file' not in request.files:
        print('No file part')
        return 'Файл не вибрано', 400
    
    file = request.files['file']
    
    if file.filename == '':
        print('No selected file')
        return 'Файл не вибрано', 400
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(f'Saving file to {filepath}')
        file.save(filepath)
        return f'Файл {filename} успішно завантажено'
    
    return 'Помилка завантаження', 500

@app.route('/analyze')
def analyze_file():
    try:
        # Знаходимо останній завантажений файл CSV
        files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.csv')]
        if not files:
            return jsonify({'error': 'No CSV files found'}), 404
            
        latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(UPLOAD_FOLDER, x)))
        filepath = os.path.join(UPLOAD_FOLDER, latest_file)
        
        # Читаємо файл та аналізуємо дані
        import pandas as pd
        df = pd.read_csv(filepath)
        
        # Отримуємо основні метрики
        total_books = len(df)
        average_rating = df['My Rating'].mean()
        
        # Знаходимо топ-5 книг за оцінкою
        top_books = df.sort_values('My Rating', ascending=False).head(5)
        top_books_data = [
            {
                'title': row['Title'],
                'rating': row['My Rating']
            }
            for _, row in top_books.iterrows()
        ]
        
        return jsonify({
            'totalBooks': total_books,
            'averageRating': round(average_rating, 2),
            'topBooks': top_books_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
