# Email Classifier Application

## Overview

This is a web-based email classification system that uses artificial intelligence to automatically categorize emails and suggest appropriate responses. The application targets financial sector companies dealing with high volumes of daily emails, automating the classification process to save team time and improve response efficiency.

The system classifies emails into two main categories:
- **Produtivo (Productive)**: Emails requiring specific action or response (support requests, case updates, system inquiries)
- **Improdutivo (Unproductive)**: Emails not requiring immediate action (congratulations, thanks, general messages)

The application accepts email content through two input methods: direct text input or file upload (TXT/PDF formats), processes the content using Natural Language Processing (NLP) techniques, and returns the classification along with suggested automated responses.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Technology**: Vanilla JavaScript with HTML5 and CSS3
- **Design Pattern**: Single Page Application (SPA) with tab-based interface
- **Key Features**:
  - Dual input methods (text entry and file upload)
  - Drag-and-drop file upload functionality
  - Real-time validation and user feedback
  - Responsive gradient-based UI design
- **Styling Approach**: CSS custom properties (variables) for consistent theming with gradient backgrounds and card-based layouts

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Design Pattern**: RESTful API architecture
- **Key Components**:
  - File upload handling with security measures (secure_filename)
  - Text extraction from multiple formats (TXT, PDF via PyPDF2)
  - NLP preprocessing pipeline for Portuguese language
  - AI integration for classification and response generation
- **File Processing**: Supports up to 16MB file uploads with configurable upload directory

### Natural Language Processing Pipeline
- **Library**: NLTK (Natural Language Toolkit)
- **Language**: Portuguese (Brazilian Portuguese - RSLP stemmer)
- **Processing Steps**:
  1. Text tokenization using punkt tokenizer
  2. Stop words removal (Portuguese corpus)
  3. Stemming using RSLP (Removedor de Sufixos da Língua Portuguesa)
- **Rationale**: Portuguese-specific NLP tools ensure accurate text preprocessing for the target market (Brazilian financial sector)

### AI Integration
- **Service**: OpenAI API
- **Purpose**: Email classification and automated response generation
- **Configuration**: API key management through environment variables
- **Approach**: The application uses OpenAI's language models to determine email category (Produtivo/Improdutivo) and generate contextually appropriate responses

### Security Measures
- **CORS**: Enabled via Flask-CORS for cross-origin requests
- **File Validation**: Whitelist approach limiting uploads to TXT and PDF only
- **Filename Sanitization**: Werkzeug's secure_filename prevents directory traversal attacks
- **File Size Limits**: 16MB maximum to prevent resource exhaustion

### Configuration Management
- **Environment Variables**: Uses python-dotenv for secure credential management
- **Upload Directory**: Automatically created if not exists, stored in 'uploads' folder
- **NLTK Data Management**: Automatic download of required language models on first run

## External Dependencies

### Core Python Libraries
- **Flask**: Web framework for handling HTTP requests and serving the frontend
- **Flask-CORS**: Cross-Origin Resource Sharing support
- **Werkzeug**: WSGI utilities including secure file handling

### AI and NLP Services
- **OpenAI API**: Primary AI service for email classification and response generation
  - Requires API key stored in environment variables
  - Used for both classification decisions and natural language response generation
- **NLTK (Natural Language Toolkit)**: Text preprocessing and analysis
  - Tokenizers: punkt, punkt_tab
  - Corpora: Portuguese stopwords
  - Stemmers: RSLP for Portuguese stemming

### File Processing
- **PyPDF2**: PDF file parsing and text extraction
  - Enables support for PDF email attachments or exports

### Environment Management
- **python-dotenv**: Loads configuration from .env file
  - Stores sensitive credentials (OpenAI API key)
  - Separates configuration from code

### Frontend (Served Statically)
- No external CDN dependencies
- Pure JavaScript (no frameworks like React/Vue)
- CSS written from scratch without UI libraries

### Data Storage
- **Local File System**: Temporary storage for uploaded files in 'uploads' directory
- **No Database**: Current implementation doesn't require persistent data storage
- **Rationale**: Stateless processing approach where each email classification is independent

### Deployment Considerations
- Application requires NLTK data downloads on first run
- Environment variables must be configured before deployment
- Upload directory needs write permissions

### Production Deployment
- **Platform**: Configured for Replit Autoscale deployment
- **Web Server**: Gunicorn with process reuse for optimal performance
- **Configuration**: Deploy config set to autoscale (stateless architecture)
- **Command**: `gunicorn --bind=0.0.0.0:5000 --reuse-port main:app`
- **Environment**: OpenAI API key stored securely in Replit Secrets

### Recent Updates (October 2025)
- Fixed PDF processing to handle None values from extract_text()
- Implemented case-insensitive file extension checking (.pdf, .PDF, etc.)
- Added proper error handling for PDFs without extractable text
- Enhanced user feedback with clear error messages for unsupported file types
- Configured production deployment with gunicorn for Replit hosting