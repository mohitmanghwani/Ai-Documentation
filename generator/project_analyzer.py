"""
Project Analyzer - Analyzes project structure and extracts information
"""

import os
import ast
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
import json
import subprocess

from .llm_handlers import BaseLLMHandler

logger = logging.getLogger(__name__)


class ProjectAnalyzer:
    """Analyzes project structure and extracts information"""
    
    def __init__(self, llm_handler: BaseLLMHandler):
        self.llm_handler = llm_handler
    
    def analyze_project(self, project_path: Path) -> Dict[str, Any]:
        """Analyze the project and return structured information"""
        try:
            project_info = {
                'project_name': project_path.name,
                'project_path': str(project_path),
                'project_type': self._detect_project_type(project_path),
                'files': self._scan_files(project_path),
                'dependencies': self._extract_dependencies(project_path),
                'structure': self._analyze_structure(project_path),
                'code_analysis': self._analyze_code(project_path),
                'git_history': self._detect_git_history(project_path)
            }
            
            logger.info(f"Project analysis complete for: {project_path}")
            return project_info
            
        except Exception as e:
            logger.error(f"Error analyzing project: {e}")
            return {
                'project_name': project_path.name,
                'project_path': str(project_path),
                'project_type': 'unknown',
                'files': [],
                'dependencies': {},
                'structure': {},
                'code_analysis': {},
                'error': str(e)
            }
    
    def _detect_project_type(self, project_path: Path) -> str:
        """Detect the type of project based on files present"""
        files = [f.name.lower() for f in project_path.rglob('*') if f.is_file()]
        
        if any('package.json' in f for f in files):
            return 'nodejs'
        elif any('requirements.txt' in f for f in files):
            return 'python'
        elif any('pom.xml' in f for f in files):
            return 'java'
        elif any('go.mod' in f for f in files):
            return 'go'
        elif any('Cargo.toml' in f for f in files):
            return 'rust'
        elif any('composer.json' in f for f in files):
            return 'php'
        else:
            return 'general'
    
    def _scan_files(self, project_path: Path) -> List[Dict[str, Any]]:
        """Scan all files in the project"""
        files = []
        exclude_dirs = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', '.env'}
        
        for file_path in project_path.rglob('*'):
            if file_path.is_file():
                # Skip files in excluded directories
                if any(exclude_dir in file_path.parts for exclude_dir in exclude_dirs):
                    continue
                
                try:
                    file_info = {
                        'name': file_path.name,
                        'path': str(file_path.relative_to(project_path)),
                        'size': file_path.stat().st_size,
                        'extension': file_path.suffix,
                        'is_binary': self._is_binary_file(file_path)
                    }
                    files.append(file_info)
                except Exception as e:
                    logger.warning(f"Error scanning file {file_path}: {e}")
        
        return files
    
    def _is_binary_file(self, file_path: Path) -> bool:
        """Check if file is binary"""
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                return b'\x00' in chunk
        except:
            return True
    
    def _extract_dependencies(self, project_path: Path) -> Dict[str, Any]:
        """Extract project dependencies"""
        dependencies = {}
        
        # Python dependencies
        requirements_file = project_path / 'requirements.txt'
        if requirements_file.exists():
            try:
                with open(requirements_file, 'r') as f:
                    deps = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                dependencies['python'] = deps
            except Exception as e:
                logger.warning(f"Error reading requirements.txt: {e}")
        
        # Node.js dependencies
        package_json = project_path / 'package.json'
        if package_json.exists():
            try:
                with open(package_json, 'r') as f:
                    data = json.load(f)
                dependencies['nodejs'] = {
                    'dependencies': data.get('dependencies', {}),
                    'devDependencies': data.get('devDependencies', {})
                }
            except Exception as e:
                logger.warning(f"Error reading package.json: {e}")
        
        return dependencies
    
    def _analyze_structure(self, project_path: Path) -> Dict[str, Any]:
        """Analyze project directory structure"""
        structure = {
            'directories': [],
            'file_count': 0,
            'total_size': 0
        }
        
        exclude_dirs = {'.git', '__pycache__', 'node_modules', '.venv', 'venv'}
        
        for item in project_path.rglob('*'):
            if any(exclude_dir in item.parts for exclude_dir in exclude_dirs):
                continue
                
            if item.is_dir():
                structure['directories'].append(str(item.relative_to(project_path)))
            elif item.is_file():
                structure['file_count'] += 1
                try:
                    structure['total_size'] += item.stat().st_size
                except:
                    pass
        
        return structure
    
    def _analyze_code(self, project_path: Path) -> Dict[str, Any]:
        """Analyze code files for patterns and structure"""
        code_analysis = {
            'python_files': [],
            'javascript_files': [],
            'html_files': [],
            'css_files': [],
            'api_endpoints': [],
            'database_models': [],
            'functions': []
        }
        
        # Analyze Python files
        for py_file in project_path.rglob('*.py'):
            try:
                analysis = self._analyze_python_file(py_file)
                code_analysis['python_files'].append(analysis)
            except Exception as e:
                logger.warning(f"Error analyzing Python file {py_file}: {e}")
        
        # Analyze JavaScript files
        for js_file in project_path.rglob('*.js'):
            try:
                analysis = self._analyze_javascript_file(js_file)
                code_analysis['javascript_files'].append(analysis)
            except Exception as e:
                logger.warning(f"Error analyzing JavaScript file {js_file}: {e}")
        
        return code_analysis
    
    def _analyze_python_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a Python file using AST"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            analysis = {
                'file': str(file_path),
                'classes': [],
                'functions': [],
                'imports': [],
                'has_api': False,
                'has_database': False
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    analysis['classes'].append({
                        'name': node.name,
                        'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    })
                elif isinstance(node, ast.FunctionDef):
                    analysis['functions'].append(node.name)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        analysis['imports'].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        analysis['imports'].append(node.module)
            
            # Detect API patterns
            api_keywords = ['fastapi', 'flask', 'django', 'app.route', 'api']
            if any(keyword in str(analysis['imports']).lower() for keyword in api_keywords):
                analysis['has_api'] = True
            
            # Detect database patterns
            db_keywords = ['sqlalchemy', 'django.db', 'models', 'database']
            if any(keyword in str(analysis['imports']).lower() for keyword in db_keywords):
                analysis['has_database'] = True
            
            return analysis
            
        except Exception as e:
            logger.warning(f"Error parsing Python file {file_path}: {e}")
            return {'file': str(file_path), 'error': str(e)}
    
    def _analyze_javascript_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a JavaScript file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            analysis = {
                'file': str(file_path),
                'functions': [],
                'classes': [],
                'has_api': False,
                'has_react': False
            }
            
            # Simple pattern matching for JavaScript
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('function ') or line.startswith('const ') and 'function' in line:
                    # Extract function name
                    if 'function' in line:
                        func_name = line.split('function')[1].split('(')[0].strip()
                        analysis['functions'].append(func_name)
                elif line.startswith('class '):
                    class_name = line.split('class')[1].split('{')[0].strip()
                    analysis['classes'].append(class_name)
            
            # Detect API patterns
            if any(keyword in content.lower() for keyword in ['fetch', 'axios', 'api', 'endpoint']):
                analysis['has_api'] = True
            
            # Detect React patterns
            if any(keyword in content.lower() for keyword in ['react', 'jsx', 'component']):
                analysis['has_react'] = True
            
            return analysis
            
        except Exception as e:
            logger.warning(f"Error analyzing JavaScript file {file_path}: {e}")
            return {'file': str(file_path), 'error': str(e)}
    
    def _detect_git_history(self, project_path: Path) -> Dict[str, Any]:
        """Detect Git history and repository information"""
        git_info = {
            'is_git_repo': False,
            'branch': None,
            'commit_count': 0,
            'last_commit': None,
            'branches': [],
            'recent_commits': []
        }
        
        try:
            # Check if .git directory exists
            git_dir = project_path / '.git'
            if not git_dir.exists():
                return git_info
            
            git_info['is_git_repo'] = True
            
            # Get current branch
            try:
                result = subprocess.run(
                    ['git', 'branch', '--show-current'],
                    cwd=project_path,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    git_info['branch'] = result.stdout.strip()
            except Exception as e:
                logger.warning(f"Error getting current branch: {e}")
            
            # Get commit count
            try:
                result = subprocess.run(
                    ['git', 'rev-list', '--count', 'HEAD'],
                    cwd=project_path,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    git_info['commit_count'] = int(result.stdout.strip())
            except Exception as e:
                logger.warning(f"Error getting commit count: {e}")
            
            # Get last commit
            try:
                result = subprocess.run(
                    ['git', 'log', '-1', '--format=%H|%an|%ae|%ad|%s', '--date=short'],
                    cwd=project_path,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0 and result.stdout.strip():
                    parts = result.stdout.strip().split('|')
                    if len(parts) >= 5:
                        git_info['last_commit'] = {
                            'hash': parts[0],
                            'author': parts[1],
                            'email': parts[2],
                            'date': parts[3],
                            'message': parts[4]
                        }
            except Exception as e:
                logger.warning(f"Error getting last commit: {e}")
            
            # Get branches
            try:
                result = subprocess.run(
                    ['git', 'branch', '-r'],
                    cwd=project_path,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    branches = [b.strip() for b in result.stdout.split('\n') if b.strip()]
                    git_info['branches'] = branches
            except Exception as e:
                logger.warning(f"Error getting branches: {e}")
            
            # Get recent commits
            try:
                result = subprocess.run(
                    ['git', 'log', '--oneline', '-10'],
                    cwd=project_path,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    commits = [c.strip() for c in result.stdout.split('\n') if c.strip()]
                    git_info['recent_commits'] = commits
            except Exception as e:
                logger.warning(f"Error getting recent commits: {e}")
                
        except Exception as e:
            logger.warning(f"Error detecting Git history: {e}")
        
        return git_info 