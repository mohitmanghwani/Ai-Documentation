# TASK.md

## Project Goal

Create **Version 3** of the "AI Documentation and Diagram Generator" by combining the best features from **Version 1** and **Version 2**, while resolving previous limitations.

---

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript (no frameworks)
- **Backend:** Django (preferred over FastAPI)
- **Diagram Generation:** Mermaid.js via CLI
- **LLM Providers:** Ollama (local), Groq (cloud) selectable via UI

---

## Requirements for Version 3

### ✅ Take from Version 1:

- The simple and user-friendly **UI/frontend**
- **Detailed and customizable diagram generation** aligned with the codebase

### ✅ Take from Version 2:

- **Ability to select model and framework via UI** (Groq, Ollama, etc.)
- More **custom options and functionality for script execution**
- **Well-structured and categorized documentation output** (technical vs. business)

---

## New Features to Implement

### 1. Frontend:

- Provide option to either:
  - **Upload a ZIP folder/project**, or
  - **Enter a local directory path**
- Allow user to:
  - **Select LLM model & framework** (Groq, Ollama, etc.) via dropdown
  - Click a **Generate button** to trigger documentation & diagram creation
  - **Download all generated files** (diagrams & documents) via provided download links/buttons

### 2. Backend:

- Use **Django only** (no FastAPI)
- Expose REST API endpoints to:
  - Accept file upload or directory path
  - Automatically generate **all diagram types**:
    - System Architecture
    - Data Flow
    - Component Diagram
  - Return URLs for frontend to download generated files
- Retain CLI functionality (for developers), but ensure app is usable via UI

### 3. Output Structure:

All generated outputs must be saved in the following structure:

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

### 4. Documents & Diagrams to Generate:

- **Diagrams:**
  - System Architecture
  - Data Flow
  - Component Diagram
- **Technical Docs:**
  - API Documentation
  - Database Schema
  - Installation Guide
  - Architecture Document
  - Code Documentation
- **Business Docs:**
  - User Manual
  - Business Requirements Document (BRD)
  - Sales Pitch Document
  - Project Overview

### 5. Diagram Output Format:

- All Mermaid diagrams must be generated as **both **``** and **``** files**

---

## Merge Logic from Version 1 & 2:

- Retain **AST parsing** and **Langchain-based LLM pipeline**
- Use **Mermaid CLI** for diagrams
- Retain **environment variable handling** (`.env`)

---

## Additional Notes

- Generated files must be **accessible via frontend download feature**
- Output folder structure must allow easy extension for potential **multi-user or multi-project support in the future**

---

## Deliverables

- Full working **Django + HTML/CSS/JS project**
- Clear, simple **UI for non-technical users**
- Complete **backend API** for file handling, document & diagram generation
- Well-structured, reusable, and maintainable codebase

