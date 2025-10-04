# Case_PraticoAutoU

📧 Classificador Inteligente de Emails com IA
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
Clone o repositório
git clone <seu-repositorio>
cd <nome-do-projeto>
Configure a API Key da OpenAI
cp .env.example .env
# Edite .env e adicione sua chave: OPENAI_API_KEY=sk-...
Instale as dependências
pip install -r requirements.txt
Execute a aplicação
python main.py
Acesse: http://localhost:5000

🌐 Deploy em Produção
Replit (Recomendado)
Este projeto já está configurado para deploy no Replit
Clique no botão "Deploy" no painel do Replit
Configure o secret OPENAI_API_KEY nas configurações
O deploy será feito automaticamente com gunicorn
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
├── main.py                 # Backend Flask (ponto de entrada da aplicação)
├── templates/
│   └── index.html          # Interface web (HTML principal)
├── static/
│   ├── style.css           # Estilos da interface
│   └── script.js           # Lógica frontend em JavaScript
├── uploads/                # Diretório temporário para salvar arquivos enviados
├── .env.example            # Exemplo de variáveis de ambiente (OPENAI_API_KEY, etc.)
├── .gitignore              # Lista de arquivos/pastas ignorados no Git
├── requirements.txt        # Dependências do projeto (Flask, OpenAI, etc.)
├── Procfile                # Instrução para o Render iniciar a aplicação
└── README.md               # Documentação principal do projeto
🎨 Exemplos de Uso
Email Produtivo:

Olá equipe,

Gostaria de solicitar uma atualização sobre o caso #12345 
que abri na semana passada. Ainda não recebi retorno sobre 
a análise solicitada.

Aguardo retorno.
Atenciosamente,
João Silva
Email Improdutivo:

Olá equipe,

Gostaria de desejar um Feliz Natal a todos!

Abraços,
Maria
🔐 Obtendo API Key da OpenAI
Acesse: https://platform.openai.com/api-keys
Faça login ou crie uma conta
Clique em "Create new secret key"
Copie a chave (começa com "sk-")
Adicione ao arquivo .env ou secrets da plataforma
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

Desenvolvido com 📚🤖 usando Flask, OpenAI e NLTK
