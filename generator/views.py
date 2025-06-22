import os
import uuid
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from django.conf import settings
from django.http import JsonResponse, HttpResponse, FileResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from .llm_handlers import get_llm_handler
from .project_analyzer import ProjectAnalyzer
from .document_generator import DocumentGenerator
from .diagram_generator import DiagramGenerator

# Ensure templates directory exists
TEMPLATES_DIR = Path(__file__).parent.parent / 'templates'
TEMPLATES_DIR.mkdir(exist_ok=True)

# Helper to create output folder structure
def create_output_folder() -> Path:
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = f"{timestamp}_{uuid.uuid4().hex[:8]}"
    output_dir = settings.OUTPUT_DIR / unique_id
    (output_dir / 'diagrams').mkdir(parents=True, exist_ok=True)
    (output_dir / 'technical_docs').mkdir(exist_ok=True)
    (output_dir / 'business_docs').mkdir(exist_ok=True)
    return output_dir

def index(request):
    return render(request, 'index.html')

@csrf_exempt
@require_POST
def upload_project(request):
    """Handle ZIP file upload, extract, and trigger generation"""
    uploaded_file = request.FILES.get('file')
    llm_provider = request.POST.get('llm_provider', 'groq')
    model_name = request.POST.get('model_name', 'llama3-8b-8192')
    if llm_provider not in ['groq', 'ollama']:
        return JsonResponse({'error': "Invalid LLM provider. Only 'groq' and 'ollama' are supported."}, status=400)
    if not uploaded_file:
        return JsonResponse({'error': 'No file uploaded'}, status=400)
    if not uploaded_file.name.endswith('.zip'):
        return JsonResponse({'error': 'Only ZIP files are allowed'}, status=400)
    # Save and extract ZIP
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_zip_path = os.path.join(temp_dir, uploaded_file.name)
        with open(temp_zip_path, 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)
        extract_dir = os.path.join(temp_dir, 'extracted')
        shutil.unpack_archive(temp_zip_path, extract_dir)
        # Use extracted dir as project path
        return _generate_docs_and_diagrams(extract_dir, llm_provider, model_name)

@csrf_exempt
@require_POST
def generate_from_path(request):
    """Handle local directory path input and trigger generation"""
    project_path = request.POST.get('project_path')
    llm_provider = request.POST.get('llm_provider', 'groq')
    model_name = request.POST.get('model_name', 'llama3-8b-8192')
    if llm_provider not in ['groq', 'ollama']:
        return JsonResponse({'error': "Invalid LLM provider. Only 'groq' and 'ollama' are supported."}, status=400)
    if not project_path or not os.path.isdir(project_path):
        return JsonResponse({'error': 'Invalid project path'}, status=400)
    return _generate_docs_and_diagrams(project_path, llm_provider, model_name)

def _generate_docs_and_diagrams(project_path, llm_provider, model_name):
    output_dir = create_output_folder()
    request_id = output_dir.name
    # LLM handler
    llm_handler = get_llm_handler(llm_provider, model_name)
    # Analyze project
    analyzer = ProjectAnalyzer(llm_handler)
    project_data = analyzer.analyze_project(Path(project_path))
    # Generate docs
    doc_gen = DocumentGenerator(llm_handler)
    docs = doc_gen.generate_all_documents(project_data)
    # Generate diagrams with business documents context
    diagram_gen = DiagramGenerator(llm_handler)
    technical_details = {
        'business_requirements': docs.get('business_requirements', ''),
        'project_overview': docs.get('project_overview', '')
    }
    diagrams = diagram_gen.generate_diagrams(project_data, technical_details)
    # Save outputs
    # Save docs
    for doc_type, content in docs.items():
        if doc_type in ['api_documentation', 'database_schema', 'installation_guide', 'architecture_documentation', 'code_documentation']:
            subdir = output_dir / 'technical_docs'
        else:
            subdir = output_dir / 'business_docs'
        subdir.mkdir(exist_ok=True)
        with open(subdir / f'{doc_type}.md', 'w', encoding='utf-8') as f:
            f.write(content)
    # Save diagrams
    diagram_gen.save_diagrams(diagrams, output_dir)
    # Prepare download URLs
    base_url = f"/output/{request_id}/"
    download_links = {
        'technical_docs': [f"{base_url}technical_docs/{doc}.md" for doc in ['api_documentation','database_schema','installation_guide','architecture_documentation','code_documentation']],
        'business_docs': [f"{base_url}business_docs/{doc}.md" for doc in ['user_manual','business_requirements','sales_pitch','project_overview']],
        'diagrams': [f"{base_url}diagrams/{name}.{ext}" for name in ['system_architecture','data_flow','component','er_diagram','requirement_diagram','gantt_chart','git_graph'] for ext in ['mmd','png']]
    }
    return JsonResponse({
        'request_id': request_id,
        'output_dir': str(output_dir),
        'download_links': download_links
    })

def download_files(request, request_id):
    """Download all generated files as a ZIP archive"""
    output_dir = settings.OUTPUT_DIR / request_id
    if not output_dir.exists():
        raise Http404('Output not found')
    # Create ZIP in memory
    import io, zipfile
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zipf:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, output_dir)
                zipf.write(file_path, arcname)
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{request_id}_output.zip"'
    return response

def get_status(request, request_id):
    """Check if output exists for a request_id"""
    output_dir = settings.OUTPUT_DIR / request_id
    exists = output_dir.exists()
    return JsonResponse({'exists': exists}) 