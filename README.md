# Case_PraticoAutoU

Sistema web de classificação automática de emails usando inteligência artificial, desenvolvido para empresas do setor financeiro que lidam com alto volume de emails diários.

🎯 Funcionalidades
Classificação Automática: Identifica emails como "Produtivo" (requerem ação) ou "Improdutivo" (sem ação imediata)
Respostas Sugeridas: Gera respostas automáticas personalizadas usando IA
Múltiplos Formatos: Aceita entrada de texto direto ou upload de arquivos (.txt, .pdf)
Processamento NLP: Utiliza técnicas de processamento de linguagem natural em português
Interface Moderna: Design intuitivo com drag-and-drop e feedback em tempo real

🚀 Como Usar
1. Entrada de Texto
Acesse a aba "Digitar Email"
Cole ou digite o conteúdo do email
Clique em "Classificar Email"

2. Upload de Arquivo
Acesse a aba "Upload de Arquivo"
Arraste e solte um arquivo .txt ou .pdf (ou clique para selecionar)
Clique em "Classificar Email"

3. Resultados
O sistema exibirá:
Categoria: Produtivo ou Improdutivo
Resposta Sugerida: Texto pronto para uso
Detalhes do Processamento: Análise NLP aplicada

🏗️ Arquitetura Técnica

Backend
Framework: Flask (Python)
IA: OpenAI GPT-3.5 Turbo
NLP: NLTK com suporte a português brasileiro
Tokenização com punkt
Remoção de stop words
Stemming com RSLP

Frontend
Tecnologias: HTML5, CSS3, JavaScript puro
Design: Interface responsiva com gradientes modernos
UX: Tabs, drag-and-drop, validação em tempo real

Segurança
Sanitização de nomes de arquivo
Validação de tipos de arquivo (whitelist)
Limite de 16MB por upload
CORS configurado
Gerenciamento seguro de API keys

📦 Dependências
flask
flask-cors
gunicorn
nltk
openai
pypdf2
python-dotenv
werkzeug

⚙️ Configuração Local

1.Clone o repositório
git clone <seu-repositorio>
cd <nome-do-projeto>

2.Configure a API Key da OpenAI
cp .env.example .env
# Edite .env e adicione sua chave: OPENAI_API_KEY=sk-...

3.Instale as dependências
pip install -r requirements.txt

4.Execute a aplicação
python main.py
Acesse: http://localhost:5000

🌐 Deploy em Produção
Replit (Recomendado)
1.Este projeto já está configurado para deploy no Replit
2.Clique no botão "Deploy" no painel do Replit
3.Configure o secret OPENAI_API_KEY nas configurações
4.O deploy será feito automaticamente com gunicorn

Outras Plataformas
Heroku:

heroku create <nome-app>
heroku config:set OPENAI_API_KEY=sk-...
git push heroku main

Vercel/Netlify: Configure como aplicação Flask seguindo a documentação da plataforma
AWS/GCP: Use o gunicorn configurado no deployment:

gunicorn --bind=0.0.0.0:5000 --reuse-port main:app

📝 Categorias de Classificação

Produtivo
Emails que requerem ação ou resposta específica:

Solicitações de suporte técnico
Atualizações sobre casos em aberto
Dúvidas sobre o sistema
Requisições de informação

Improdutivo
Emails que não necessitam ação imediata:

Mensagens de felicitações
Agradecimentos
Mensagens pessoais
Comunicados gerais
🔧 Estrutura do Projeto
.
├── main.py                 # Backend Flask
├── templates/
│   └── index.html         # Interface web
├── static/
│   ├── style.css          # Estilos
│   └── script.js          # Lógica frontend
├── uploads/               # Diretório temporário (criado automaticamente)
├── .env.example           # Template de configuração
├── .gitignore            # Arquivos ignorados
└── README.md             # Esta documentação

🔐 Obtendo API Key da OpenAI
1.Acesse: https://platform.openai.com/api-keys
2.Faça login ou crie uma conta
3.Clique em "Create new secret key"
4.Copie a chave (começa com "sk-")
5.Adicione ao arquivo .env ou secrets da plataforma

🐛 Solução de Problemas
Erro: API key não configurada

Verifique se a variável OPENAI_API_KEY está configurada
PDF sem texto extraível

Use PDFs com texto pesquisável (não escaneados)
Ou digite o conteúdo manualmente
Erro ao processar arquivo

Verifique se o arquivo é .txt ou .pdf válido
Tamanho máximo: 16MB

📄 Licença
Este projeto foi desenvolvido como solução para desafio técnico.

👥 Suporte
Para dúvidas ou suporte, entre em contato através dos canais disponíveis.
