html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MedBot - AI Medicine Analyzer</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Segoe UI, sans-serif; background: #f0f4f8; min-height: 100vh; }
        .header { background: linear-gradient(135deg, #2c7be5, #1a5276); color: white; text-align: center; padding: 30px; }
        .header h1 { font-size: 2rem; }
        .header p { opacity: 0.85; margin-top: 5px; }
        .container { max-width: 850px; margin: 40px auto; padding: 0 20px; }
        .upload-card { background: white; border-radius: 16px; padding: 40px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
        .upload-area { border: 2px dashed #2c7be5; border-radius: 12px; padding: 50px 20px; text-align: center; cursor: pointer; transition: all 0.3s; background: #f8faff; }
        .upload-area:hover { background: #eef3ff; }
        .upload-area .icon { font-size: 3rem; }
        .upload-area p { color: #666; margin-top: 10px; }
        #preview { width: 100%; max-height: 300px; object-fit: contain; border-radius: 10px; display: none; margin-top: 15px; }
        .question-box { margin-top: 20px; }
        .question-box input { width: 100%; padding: 14px 18px; border: 1px solid #ddd; border-radius: 10px; font-size: 15px; outline: none; }
        .question-box input:focus { border-color: #2c7be5; }
        .analyze-btn { margin-top: 20px; width: 100%; padding: 15px; background: linear-gradient(135deg, #2c7be5, #1a5276); color: white; border: none; border-radius: 10px; font-size: 16px; font-weight: bold; cursor: pointer; }
        .analyze-btn:disabled { opacity: 0.5; cursor: not-allowed; }
        .result-card { background: white; border-radius: 16px; padding: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin-top: 30px; display: none; }
        .result-card h2 { color: #1a5276; margin-bottom: 20px; }
        .result-content { line-height: 1.8; color: #333; white-space: pre-wrap; }
        .loader { text-align: center; padding: 30px; display: none; }
        .loader .spinner { width: 45px; height: 45px; border: 4px solid #ddd; border-top: 4px solid #2c7be5; border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto; }
        @keyframes spin { to { transform: rotate(360deg); } }
        .disclaimer { background: #fff3cd; border-left: 4px solid #ffc107; padding: 12px 16px; border-radius: 6px; margin-top: 20px; font-size: 13px; color: #856404; }
    </style>
</head>
<body>
<div class="header">
    <h1>MedBot - AI Medicine Analyzer</h1>
    <p>Upload a photo of any medicine and get instant detailed information</p>
</div>
<div class="container">
    <div class="upload-card">
        <div class="upload-area" onclick="document.getElementById('imageInput').click()">
            <div class="icon">📷</div>
            <p><strong>Click to upload</strong> or drag and drop a medicine image</p>
            <p style="font-size:13px; margin-top:5px;">Supports JPG, PNG, WEBP</p>
        </div>
        <input type="file" id="imageInput" accept="image/*" style="display:none">
        <img id="preview" alt="Medicine Preview">
        <div class="question-box">
            <input type="text" id="questionInput" placeholder="Optional: Ask something e.g. Can I take this with food?">
        </div>
        <button class="analyze-btn" id="analyzeBtn" onclick="analyzeMedicine()" disabled>
            Analyze Medicine
        </button>
    </div>
    <div class="loader" id="loader">
        <div class="spinner"></div>
        <p style="margin-top:15px; color:#666;">Analyzing your medicine, please wait...</p>
    </div>
    <div class="result-card" id="resultCard">
        <h2>Medicine Analysis Result</h2>
        <div class="result-content" id="resultContent"></div>
    </div>
    <div class="disclaimer">
        <strong>Disclaimer:</strong> MedBot is for educational purposes only.
        Always consult a licensed healthcare professional before taking any medication.
    </div>
</div>
<script>
    const imageInput = document.getElementById('imageInput');
    const preview = document.getElementById('preview');
    const analyzeBtn = document.getElementById('analyzeBtn');
    imageInput.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = e => {
                preview.src = e.target.result;
                preview.style.display = 'block';
                analyzeBtn.disabled = false;
            };
            reader.readAsDataURL(file);
        }
    });
    async function analyzeMedicine() {
        const file = imageInput.files[0];
        const question = document.getElementById('questionInput').value;
        if (!file) return;
        document.getElementById('loader').style.display = 'block';
        document.getElementById('resultCard').style.display = 'none';
        analyzeBtn.disabled = true;
        analyzeBtn.textContent = 'Analyzing...';
        const formData = new FormData();
        formData.append('image', file);
        formData.append('question', question);
        try {
            const response = await fetch('/analyze/', { method: 'POST', body: formData });
            const data = await response.json();
            document.getElementById('loader').style.display = 'none';
            document.getElementById('resultCard').style.display = 'block';
            if (data.success) {
                document.getElementById('resultContent').textContent = data.analysis;
            } else {
                document.getElementById('resultContent').textContent = 'Error: ' + data.error;
            }
        } catch (err) {
            document.getElementById('loader').style.display = 'none';
            document.getElementById('resultContent').textContent = 'Something went wrong. Please try again.';
            document.getElementById('resultCard').style.display = 'block';
        }
        analyzeBtn.disabled = false;
        analyzeBtn.textContent = 'Analyze Medicine';
    }
</script>
</body>
</html>'''

with open('medicine/templates/medicine/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("SUCCESS! File written!")
print("File size:", len(html_content), "bytes")