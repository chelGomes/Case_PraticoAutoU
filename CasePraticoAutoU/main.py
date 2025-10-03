import os
import re
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import RSLPStemmer
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)

try:
    nltk.data.find('stemmers/rslp')
except LookupError:
    nltk.download('rslp', quiet=True)

stemmer = RSLPStemmer()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_txt_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        return file.read()

def read_pdf_file(filepath):
    text = ""
    with open(filepath, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    
    if not text or len(text.strip()) < 10:
        raise ValueError("O PDF não contém texto extraível. Por favor, use um PDF com texto pesquisável ou digite o conteúdo manualmente.")
    
    return text

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-záàâãéèêíïóôõöúçñ\s]', '', text)
    
    tokens = word_tokenize(text, language='portuguese')
    
    stop_words = set(stopwords.words('portuguese'))
    tokens = [word for word in tokens if word not in stop_words and len(word) > 2]
    
    tokens = [stemmer.stem(word) for word in tokens]
    
    return ' '.join(tokens)

def classify_and_respond(email_text):
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        return {
            'category': 'Erro',
            'response': 'Erro: API key da OpenAI não configurada. Por favor, configure a variável de ambiente OPENAI_API_KEY.',
            'preprocessed': preprocess_text(email_text[:200])
        }
    
    try:
        client = OpenAI(api_key=api_key)
        
        classification_prompt = f"""Analise o seguinte email e classifique-o em uma das categorias:

PRODUTIVO: Emails que requerem ação ou resposta específica (solicitações de suporte, atualizações sobre casos, dúvidas técnicas, requisições).
IMPRODUTIVO: Emails que não necessitam ação imediata (felicitações, agradecimentos, mensagens pessoais).

Email: {email_text}

Responda APENAS com "PRODUTIVO" ou "IMPRODUTIVO"."""

        classification_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente especializado em classificação de emails corporativos."},
                {"role": "user", "content": classification_prompt}
            ],
            temperature=0.3,
            max_tokens=10
        )
        
        category_content = classification_response.choices[0].message.content
        category = category_content.strip().upper() if category_content else 'PRODUTIVO'
        
        if 'PRODUTIVO' in category:
            category = 'PRODUTIVO'
        elif 'IMPRODUTIVO' in category:
            category = 'IMPRODUTIVO'
        else:
            category = 'PRODUTIVO'
        
        response_prompt = f"""Baseado neste email classificado como {category}, gere uma resposta automática adequada e profissional em português:

Email: {email_text}

{"Gere uma resposta profissional informando que a solicitação foi recebida e será analisada pela equipe." if category == 'PRODUTIVO' else 'Gere uma resposta cordial e breve agradecendo a mensagem.'}"""

        response_generation = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente que gera respostas automáticas profissionais para emails corporativos."},
                {"role": "user", "content": response_prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        response_content = response_generation.choices[0].message.content
        suggested_response = response_content.strip() if response_content else 'Resposta não disponível.'
        
        preprocessed = preprocess_text(email_text[:200])
        
        return {
            'category': category,
            'response': suggested_response,
            'preprocessed': preprocessed
        }
        
    except Exception as e:
        return {
            'category': 'Erro',
            'response': f'Erro ao processar com a API: {str(e)}',
            'preprocessed': preprocess_text(email_text[:200])
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify_email():
    try:
        email_text = None
        
        if 'email_text' in request.form and request.form['email_text'].strip():
            email_text = request.form['email_text'].strip()
        
        elif 'file' in request.files:
            file = request.files['file']
            
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                try:
                    if filename.lower().endswith('.pdf'):
                        email_text = read_pdf_file(filepath)
                    else:
                        email_text = read_txt_file(filepath)
                except ValueError as ve:
                    os.remove(filepath)
                    return jsonify({
                        'error': str(ve)
                    }), 400
                
                os.remove(filepath)
        
        if not email_text or len(email_text.strip()) < 10:
            return jsonify({
                'error': 'Por favor, forneça um texto de email válido (mínimo 10 caracteres) ou faça upload de um arquivo.'
            }), 400
        
        result = classify_and_respond(email_text)
        
        return jsonify({
            'original_text': email_text[:500],
            'category': result['category'],
            'suggested_response': result['response'],
            'preprocessed_text': result['preprocessed']
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Erro ao processar: {str(e)}'
        }), 500

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'message': 'API funcionando'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
