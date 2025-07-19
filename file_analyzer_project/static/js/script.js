document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('fileInput');
    const statusMessage = document.getElementById('statusMessage');
    const analyzeButton = document.getElementById('analyzeButton');
    const analysisResult = document.getElementById('analysisResult');
    const uploadContainer = document.getElementById('uploadContainer');

    let uploadedFilename = '';

    fileInput.addEventListener('change', async () => {
        const file = fileInput.files[0];
        if (!file) return;
        
        // Показуємо повідомлення про завантаження
        statusMessage.textContent = 'Завантаження файлу...';
        statusMessage.classList.remove('hidden');
        
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
                statusMessage.classList.add('visible');
                // Показуємо кнопку аналізу
                analyzeButton.style.display = 'inline-block';
            } else {
                alert(`Помилка: ${data.message}`);
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
                analyzeButton.style.display = 'none';
                statusMessage.style.display = 'none';

                analysisResult.innerHTML = '<h3>Результати аналізу:</h3>';
                analysisResult.classList.remove('hidden');
                const booksByYear = data.analysis['Книг прочитано за роками'];
                let resultHTML = '<ul>';
                for (const [year, count] of Object.entries(booksByYear)) {
                    resultHTML += `<li><strong>${parseInt(year)} рік:</strong> ${count} книг(и)</li>`;
                }
                resultHTML += '</ul>';
                analysisResult.innerHTML += resultHTML;
            } else {
                alert(`Помилка аналізу: ${data.message}`);
            }
        } catch (error) {
            console.error('Помилка аналізу:', error);
            alert('Сталася помилка під час аналізу файлу.');
        }
    });
});