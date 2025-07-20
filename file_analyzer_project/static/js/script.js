document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('fileInput');
    const statusMessage = document.getElementById('statusMessage');
    const analyzeButton = document.getElementById('analyzeButton');
    const analysisResults = document.getElementById('analysis-results');
    const yearPlotDiv = document.getElementById('year-plot');
    const monthPlotDiv = document.getElementById('month-plot');
    const weekdayPlotDiv = document.getElementById('weekday-plot');
    const uploadContainer = document.getElementById('uploadContainer');
    const plotsContainer = document.querySelector('.plots-container');

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
                // Ховаємо кнопку та прибираємо клас 'show' з повідомлення
                analyzeButton.style.display = 'none';
                statusMessage.classList.remove('show');

                const analysis = data.analysis;

                // Відображаємо графік за роками
                if (analysis.year_graph) {
                    const yearGraphData = JSON.parse(analysis.year_graph);
                    Plotly.newPlot('year-plot', yearGraphData.data, yearGraphData.layout);
                }
                
                // Відображаємо графік за місяцями
                if (analysis.month_graph) {
                    const monthGraphData = JSON.parse(analysis.month_graph);
                    Plotly.newPlot('month-plot', monthGraphData.data, monthGraphData.layout);
                }
                
                // Відображаємо графік кількості книг за днями тижня
                if (analysis.weekday_graph) {
                    const weekdayGraphData = JSON.parse(analysis.weekday_graph);
                    Plotly.newPlot('weekday-plot', weekdayGraphData.data, weekdayGraphData.layout);
                }
                
                // Відображаємо графік середніх оцінок та кількості сторінок
                if (analysis.ratings_pages_graph) {
                    const ratingsPagesGraphData = JSON.parse(analysis.ratings_pages_graph);
                    Plotly.newPlot('ratings-pages-plot', ratingsPagesGraphData.data, ratingsPagesGraphData.layout);
                }
                
                // Показуємо контейнер з результатами
                analysisResults.classList.remove('hidden');
                plotsContainer.style.display = 'flex';
            } else {
                alert(`Помилка аналізу: ${data.message}`);
            }
        } catch (error) {
            console.error('Помилка аналізу:', error);
            alert('Сталася помилка під час аналізу файлу.');
        }
    });
});