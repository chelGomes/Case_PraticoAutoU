document.addEventListener('DOMContentLoaded', function() {
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');
    const textForm = document.getElementById('text-form');
    const fileForm = document.getElementById('file-form');
    const fileInput = document.getElementById('file-input');
    const dropZone = document.getElementById('drop-zone');
    const selectedFileDisplay = document.getElementById('selected-file');
    const fileSubmitBtn = document.getElementById('file-submit');
    const loader = document.getElementById('loader');
    const results = document.getElementById('results');
    const errorDiv = document.getElementById('error');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.dataset.tab;
            
            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(tc => tc.classList.remove('active'));
            
            tab.classList.add('active');
            document.getElementById(`${targetTab}-content`).classList.add('active');
        });
    });

    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            displaySelectedFile(file);
        }
    });

    dropZone.addEventListener('click', () => {
        fileInput.click();
    });

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        
        const file = e.dataTransfer.files[0];
        if (file) {
            const allowedTypes = ['text/plain', 'application/pdf'];
            if (allowedTypes.includes(file.type)) {
                fileInput.files = e.dataTransfer.files;
                displaySelectedFile(file);
            } else {
                showError('Por favor, selecione um arquivo .txt ou .pdf');
            }
        }
    });

    function displaySelectedFile(file) {
        const fileSize = (file.size / 1024 / 1024).toFixed(2);
        selectedFileDisplay.textContent = `📄 ${file.name} (${fileSize} MB)`;
        fileSubmitBtn.disabled = false;
    }

    textForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const emailText = document.getElementById('email-text').value.trim();
        
        if (!emailText || emailText.length < 10) {
            showError('Por favor, digite um email válido com pelo menos 10 caracteres.');
            return;
        }

        const formData = new FormData();
        formData.append('email_text', emailText);
        
        await classifyEmail(formData);
    });

    fileForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const file = fileInput.files[0];
        if (!file) {
            showError('Por favor, selecione um arquivo.');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);
        
        await classifyEmail(formData);
    });

    async function classifyEmail(formData) {
        hideError();
        results.style.display = 'none';
        loader.style.display = 'block';

        try {
            const response = await fetch('/classify', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Erro ao processar o email');
            }

            displayResults(data);
        } catch (error) {
            showError(error.message);
        } finally {
            loader.style.display = 'none';
        }
    }

    function displayResults(data) {
        const categoryBadge = document.getElementById('category-badge');
        const categoryResult = document.getElementById('category-result');
        const responseResult = document.getElementById('response-result');
        const originalText = document.getElementById('original-text');
        const preprocessedText = document.getElementById('preprocessed-text');

        categoryResult.textContent = data.category;
        
        if (data.category === 'PRODUTIVO') {
            categoryBadge.textContent = '✓ Produtivo';
            categoryBadge.className = 'category-badge productive';
        } else if (data.category === 'IMPRODUTIVO') {
            categoryBadge.textContent = 'ⓘ Improdutivo';
            categoryBadge.className = 'category-badge unproductive';
        } else {
            categoryBadge.textContent = '⚠ ' + data.category;
            categoryBadge.className = 'category-badge';
            categoryBadge.style.background = '#ed8936';
            categoryBadge.style.color = 'white';
        }

        responseResult.textContent = data.suggested_response;
        originalText.textContent = data.original_text + (data.original_text.length >= 500 ? '...' : '');
        preprocessedText.textContent = data.preprocessed_text || 'N/A';

        results.style.display = 'block';
        results.scrollIntoView({ behavior: 'smooth' });
    }

    function showError(message) {
        const errorMessage = document.getElementById('error-message');
        errorMessage.textContent = message;
        errorDiv.style.display = 'flex';
        errorDiv.scrollIntoView({ behavior: 'smooth' });
    }

    function hideError() {
        errorDiv.style.display = 'none';
    }
});

function resetForm() {
    document.getElementById('text-form').reset();
    document.getElementById('file-form').reset();
    document.getElementById('selected-file').textContent = '';
    document.getElementById('file-submit').disabled = true;
    document.getElementById('results').style.display = 'none';
    document.getElementById('error').style.display = 'none';
    
    document.querySelector('.tab[data-tab="text"]').click();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function toggleDetails() {
    const detailsContent = document.getElementById('details-content');
    const arrowIcon = document.getElementById('arrow-icon');
    
    detailsContent.classList.toggle('open');
    
    if (detailsContent.classList.contains('open')) {
        arrowIcon.setAttribute('d', 'M7 14l3-3 3 3');
    } else {
        arrowIcon.setAttribute('d', 'M7 10l3 3 3-3');
    }
}

function copyResponse() {
    const responseText = document.getElementById('response-result').textContent;
    
    navigator.clipboard.writeText(responseText).then(() => {
        const copyBtn = document.querySelector('.btn-copy');
        const originalText = copyBtn.innerHTML;
        copyBtn.innerHTML = '✓ Copiado!';
        copyBtn.style.background = '#48bb78';
        copyBtn.style.color = 'white';
        
        setTimeout(() => {
            copyBtn.innerHTML = originalText;
            copyBtn.style.background = '';
            copyBtn.style.color = '';
        }, 2000);
    }).catch(err => {
        console.error('Erro ao copiar:', err);
    });
}
