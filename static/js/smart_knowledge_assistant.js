const chatBox = document.getElementById('chat-box');
let loadingInterval;

function addMessage(text, type) {
    const div = document.createElement('div');
    div.className = `message ${type}`;
    div.innerText = text;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function showLoading() {
    const div = document.createElement('div');
    div.className = 'message bot loading';
    div.innerText = '.'; 
    div.id = 'loading-message';
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;

    let dots = 1;
    loadingInterval = setInterval(() => {
        dots = (dots % 3) + 1;
        div.innerText = '.'.repeat(dots);
    }, 500); 
}

function removeLoading() {
    clearInterval(loadingInterval);  
    const loadingMsg = document.getElementById('loading-message');
    if (loadingMsg) {
        chatBox.removeChild(loadingMsg);
    }
}

async function uploadPDF() {
    const fileInput = document.getElementById('pdfFile');
    const file = fileInput.files[0];

    if (!file) {
        alert('Please select a PDF file first.');
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch('http://localhost:8000/upload_pdf', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error('Upload failed');

        const data = await response.json();
        addMessage(`✅ PDF "${file.name}" uploaded successfully.`, 'bot');
    } catch (err) {
        addMessage('❌ Failed to upload PDF.', 'bot');
        console.error(err);
    }
}

async function sendQuery() {
    const input = document.getElementById('query');
    const question = input.value.trim();
    if (!question) return;

    addMessage(question, 'user');
    input.value = '';

    showLoading();

    try {
        const response = await fetch('http://localhost:8000/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question })
        });

        const data = await response.json();
        
        removeLoading();
        addMessage(data.answer, 'bot');
    } catch (err) {
        removeLoading();
        addMessage('❌ Error connecting to backend.', 'bot');
        console.error(err);
    }
}
