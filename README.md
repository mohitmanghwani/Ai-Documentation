# AI Documentation & Diagram Generator (Version 3)

## Overview

This project is an AI-powered tool that generates comprehensive documentation and diagrams for any codebase. It combines the best features of previous versions, offering:

- **Simple, user-friendly web UI**
- **Upload ZIP or enter local directory path**
- **Select LLM provider (Ollama, Groq, or Simple)**
- **Generates technical and business documentation**
- **Creates Mermaid diagrams as both `.mmd` and `.png`**
- **Download all outputs easily**

---

## Features
- Upload a project as a ZIP or specify a local directory
- Choose LLM provider/model (Ollama, Groq, or Simple)
- Generates:
  - System Architecture, Data Flow, and Component Diagrams
  - API Documentation, Database Schema, Installation Guide, Architecture & Code Docs
  - User Manual, Business Requirements, Sales Pitch, Project Overview
- All outputs organized in `/output/{timestamp}_{uuid}/...`
- Download individual files or all as a ZIP

---

## Tech Stack
- **Backend:** Django 4.x, Python 3.8+
- **Frontend:** HTML, Tailwind CSS, JavaScript
- **LLM Providers:** Ollama (local), Groq (cloud), Simple (template)
- **Diagram Generation:** Mermaid.js CLI (`mmdc`)

---

## Setup Instructions

### 1. Clone the Repository
```
git clone <your-repo-url>
cd Version_3
```

### 2. Create and Activate a Virtual Environment
```
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Python Dependencies
```
pip install -r requirements.txt
```

### 4. Install Mermaid CLI (for PNG diagrams)
```
npm install -g @mermaid-js/mermaid-cli
```

### 5. Set Up Environment Variables
Copy the example environment file and configure your settings:
```bash
# Windows:
copy env.example .env
# macOS/Linux:
cp env.example .env
```

Edit `.env` file with your configuration:
```env
# Django Settings
DJANGO_SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True

# LLM API Keys
GROQ_API_KEY=your-groq-api-key-here
OLLAMA_BASE_URL=http://localhost:11434
```

**Note:** 
- For **Groq**: Get your API key from [Groq Console](https://console.groq.com/)
- For **Ollama**: Ensure Ollama is running locally (default: http://localhost:11434)
- The **Simple** provider works without any API keys

### 6. Apply Django Migrations
```
python manage.py migrate
```

### 7. Run the Development Server
```
python manage.py runserver
```
Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## Usage
1. Open the web UI.
2. Upload a ZIP file or enter a local directory path.
3. Select LLM provider and model.
4. Click **Generate Documentation & Diagrams**.
5. Download generated files from the results section.

---

## Output Structure
```
/output/{timestamp}_{uuid}/
    ├── diagrams/
    │   ├── system_architecture.mmd
    │   ├── system_architecture.png
    │   ├── data_flow.mmd
    │   ├── data_flow.png
    │   ├── component.mmd
    │   └── component.png
    ├── technical_docs/
    │   ├── api_documentation.md
    │   ├── database_schema.md
    │   ├── installation_guide.md
    │   ├── architecture_documentation.md
    │   └── code_documentation.md
    └── business_docs/
        ├── user_manual.md
        ├── business_requirements.md
        ├── sales_pitch.md
        └── project_overview.md
```

---

## Troubleshooting
- **Mermaid PNG not generated?**
  - Ensure `mmdc` is installed and in your PATH (`npm install -g @mermaid-js/mermaid-cli`).
- **LLM errors?**
  - Check your API keys in the `.env` file and that Ollama/Groq are accessible.
- **Static file issues?**
  - Ensure `DEBUG = True` in your `.env` file during development.
- **Permission errors?**
  - Run your terminal as administrator or check folder permissions.
- **Environment variables not loading?**
  - Ensure your `.env` file is in the project root directory.

---

## Contributing
Pull requests and suggestions are welcome! Please open an issue or PR.

---

## License
[MIT License](LICENSE) (add your license file if needed) 