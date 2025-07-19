document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('fileInput');
    const statusMessage = document.getElementById('statusMessage');
    const analyzeButton = document.getElementById('analyzeButton');
    const analysisResults = document.getElementById('analysis-results');
    const plotDiv = document.getElementById('plot');
    const uploadContainer = document.getElementById('uploadContainer');

    let uploadedFilename = '';

    fileInput.addEventListener('change', async () => {
        const file = fileInput.files[0];
        if (!file) return;
        
        // Логуємо у консоль для налагодження
        console.log('Початок завантаження файлу...');
        
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                uploadedFilename = data.filename;
                // Ховаємо контейнер завантаження
                uploadContainer.style.display = 'none';
                // Показуємо повідомлення про успішне завантаження
                statusMessage.textContent = 'Файл успішно завантажено';
                statusMessage.classList.remove('error');
                statusMessage.classList.add('show');
                // Показуємо кнопку аналізу
                analyzeButton.style.display = 'inline-block';
            } else {
                statusMessage.textContent = `Помилка: ${data.message}`;
                statusMessage.classList.remove('show');
                statusMessage.classList.add('error', 'show');
            }
        } catch (error) {
            console.error('Помилка завантаження:', error);
            alert('Сталася помилка під час завантаження файлу.');
        }
    });

    analyzeButton.addEventListener('click', async () => {
        if (!uploadedFilename) return;

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ filename: uploadedFilename })
            });

            const data = await response.json();

            if (data.success) {
                // Ховаємо кнопку та повідомлення
                analyzeButton.style.display = 'none';
                statusMessage.style.display = 'none';

                const analysis = data.analysis;

                // Якщо є дані для графіка, відображаємо його
                if (analysis.graph) {
                    const graphData = JSON.parse(analysis.graph);
                    // Відображаємо графік
                    Plotly.newPlot('plot', graphData.data, graphData.layout);
                    
                    // Показуємо контейнер з результатами
                    analysisResults.classList.remove('hidden');
                }
            } else {
                alert(`Помилка аналізу: ${data.message}`);
            }
        } catch (error) {
            console.error('Помилка аналізу:', error);
            alert('Сталася помилка під час аналізу файлу.');
        }
    });
});