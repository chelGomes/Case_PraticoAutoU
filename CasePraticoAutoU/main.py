import os
import re
import time
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

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Download recursos do NLTK
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

def call_openai_with_retry(client, messages, max_retries=3, **kwargs):
    """
    Chama a API da OpenAI com retry em caso de erros temporários
    """
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                messages=messages,
                **kwargs
            )
            return response
        except Exception as e:
            error_str = str(e)
            
            # Erro de cota excedida
            if 'insufficient_quota' in error_str or '429' in error_str:
                raise Exception(
                    "⚠️ COTA DA API OPENAI EXCEDIDA\n\n"
                    "Seu limite de uso da OpenAI foi atingido. Para resolver:\n\n"
                    "1. Acesse: https://platform.openai.com/account/billing\n"
                    "2. Adicione um método de pagamento ou compre créditos\n"
                    "3. Verifique seu uso em: https://platform.openai.com/account/usage\n\n"
                    "Enquanto isso, o sistema usará classificação local básica."
                )
            
            # Erro de rate limit (muitas requisições)
            if 'rate_limit' in error_str.lower() and attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Espera exponencial: 1s, 2s, 4s
                print(f"Rate limit atingido. Aguardando {wait_time}s antes de tentar novamente...")
                time.sleep(wait_time)
                continue
            
            # Outros erros
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            
            raise

def classify_locally(email_text):
    """
    Classificação local básica quando a API não está disponível
    """
    text_lower = email_text.lower()
    
    # Palavras-chave para emails produtivos
    productive_keywords = [
        'solicit', 'dúvida', 'problema', 'erro', 'ajuda', 'suporte',
        'urgent', 'prazo', 'preciso', 'como', 'quando', 'pergunta',
        'favor', 'possível', 'pode', 'consegue', 'atualização',
        'status', 'andamento', 'resposta', 'informação'
    ]
    
    # Palavras-chave para emails improdutivos
    unproductive_keywords = [
        'obrigad', 'agradec', 'parabéns', 'feliz', 'ótimo',
        'excelente', 'perfeito', 'sucesso', 'felicitações'
    ]
    
    productive_score = sum(1 for keyword in productive_keywords if keyword in text_lower)
    unproductive_score = sum(1 for keyword in unproductive_keywords if keyword in text_lower)
    
    if unproductive_score > productive_score:
        category = 'IMPRODUTIVO'
        response = (
            "Prezado(a),\n\n"
            "Agradecemos sinceramente pelo seu contato e pelas palavras gentis.\n\n"
            "Ficamos muito felizes com seu feedback!\n\n"
            "Atenciosamente,\n"
            "Equipe de Suporte"
        )
    else:
        category = 'PRODUTIVO'
        response = (
            "Prezado(a),\n\n"
            "Recebemos sua mensagem e ela já está sendo analisada por nossa equipe.\n\n"
            "Retornaremos em breve com uma resposta detalhada.\n\n"
            "Agradecemos pela sua paciência.\n\n"
            "Atenciosamente,\n"
            "Equipe de Suporte"
        )
    
    return {
        'category': category,
        'response': response,
        'method': 'local'
    }

def classify_and_respond(email_text):
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        result = classify_locally(email_text)
        result['response'] = '⚠️ API OpenAI não configurada. Usando classificação local.\n\n' + result['response']
        result['preprocessed'] = preprocess_text(email_text[:200])
        return result
    
    try:
        client = OpenAI(api_key=api_key)
        
        # Tentativa 1: Classificação
        classification_prompt = f"""Analise o seguinte email e classifique-o em uma das categorias:

PRODUTIVO: Emails que requerem ação ou resposta específica (solicitações de suporte, atualizações sobre casos, dúvidas técnicas, requisições).
IMPRODUTIVO: Emails que não necessitam ação imediata (felicitações, agradecimentos, mensagens pessoais).

Email: {email_text}

Responda APENAS com "PRODUTIVO" ou "IMPRODUTIVO"."""

        classification_response = call_openai_with_retry(
            client,
            messages=[
                {"role": "system", "content": "Você é um assistente especializado em classificação de emails corporativos."},
                {"role": "user", "content": classification_prompt}
            ],
            model="gpt-3.5-turbo",
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
        
        # Tentativa 2: Geração de resposta
        response_prompt = f"""Baseado neste email classificado como {category}, gere uma resposta automática adequada e profissional em português:

Email: {email_text}

{"Gere uma resposta profissional informando que a solicitação foi recebida e será analisada pela equipe." if category == 'PRODUTIVO' else 'Gere uma resposta cordial e breve agradecendo a mensagem.'}"""

        response_generation = call_openai_with_retry(
            client,
            messages=[
                {"role": "system", "content": "Você é um assistente que gera respostas automáticas profissionais para emails corporativos."},
                {"role": "user", "content": response_prompt}
            ],
            model="gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=200
        )
        
        response_content = response_generation.choices[0].message.content
        suggested_response = response_content.strip() if response_content else 'Resposta não disponível.'
        
        preprocessed = preprocess_text(email_text[:200])
        
        return {
            'category': category,
            'response': suggested_response,
            'preprocessed': preprocessed,
            'method': 'openai'
        }
        
    except Exception as e:
        error_message = str(e)
        
        # Se for erro de cota, usar classificação local
        if 'COTA DA API OPENAI EXCEDIDA' in error_message:
            result = classify_locally(email_text)
            result['response'] = f"{error_message}\n\n{'='*50}\n\nCLASSIFICAÇÃO LOCAL:\n\n{result['response']}"
            result['preprocessed'] = preprocess_text(email_text[:200])
            return result
        
        # Outros erros
        return {
            'category': 'Erro',
            'response': f'Erro ao processar com a API: {error_message}',
            'preprocessed': preprocess_text(email_text[:200]),
            'method': 'error'
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
            'preprocessed_text': result['preprocessed'],
            'classification_method': result.get('method', 'unknown')
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Erro ao processar: {str(e)}'
        }), 500

@app.route('/health')
def health():
    api_key = os.getenv('OPENAI_API_KEY')
    return jsonify({
        'status': 'ok',
        'message': 'API funcionando',
        'openai_configured': bool(api_key),
        'fallback_available': True
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
