document.addEventListener('DOMContentLoaded', () => {
    const uploadButton = document.getElementById('uploadButton');
    const fileInput = document.getElementById('fileInput');
    const statusMessage = document.getElementById('statusMessage');
    const analyzeButton = document.getElementById('analyzeButton');
    const analysisResult = document.getElementById('analysisResult');

    let uploadedFilename = '';

    uploadButton.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', async () => {
        const file = fileInput.files[0];
        if (!file) return;

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
                uploadButton.style.display = 'none';
                statusMessage.textContent = data.message;
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