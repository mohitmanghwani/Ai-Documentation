"""
Document Generator - Generates various types of documentation
"""

import logging
from typing import Dict, Any, List
from pathlib import Path

from .llm_handlers import BaseLLMHandler

logger = logging.getLogger(__name__)


class DocumentGenerator:
    """Generates comprehensive documentation for projects"""
    
    def __init__(self, llm_handler: BaseLLMHandler):
        self.llm_handler = llm_handler
    
    def generate_all_documents(self, project_data: Dict[str, Any], technical_details: Dict[str, Any] = None) -> Dict[str, str]:
        """Generate all types of documentation"""
        documents = {}
        
        # Technical documents
        documents['api_documentation'] = self._generate_api_documentation(project_data, technical_details)
        documents['database_schema'] = self._generate_database_schema_doc(project_data, technical_details)
        documents['installation_guide'] = self._generate_installation_guide(project_data, technical_details)
        documents['architecture_documentation'] = self._generate_architecture_doc(project_data, technical_details)
        documents['code_documentation'] = self._generate_code_documentation(project_data, technical_details)
        
        # Business documents
        documents['user_manual'] = self._generate_user_manual(project_data, technical_details)
        documents['business_requirements'] = self._generate_business_requirements(project_data, technical_details)
        documents['sales_pitch'] = self._generate_sales_pitch(project_data, technical_details)
        documents['project_overview'] = self._generate_project_overview(project_data, technical_details)
        
        return documents
    
    def _generate_api_documentation(self, project_data: Dict[str, Any], technical_details: Dict[str, Any] = None) -> str:
        """Generate API documentation"""
        prompt = f"""
        Generate comprehensive API documentation for the project: {project_data.get('project_name', 'Unknown Project')}
        
        Project Type: {project_data.get('project_type', 'Unknown')}
        Project Path: {project_data.get('project_path', 'Unknown')}
        
        Code Analysis:
        {self._format_code_analysis(project_data.get('code_analysis', {}))}
        
        Dependencies:
        {self._format_dependencies(project_data.get('dependencies', {}))}
        
        Please generate detailed API documentation including:
        1. Overview of the API
        2. Authentication methods
        3. Endpoints with HTTP methods, parameters, and responses
        4. Request/response examples
        5. Error handling
        6. Rate limiting information
        7. SDK examples if applicable
        
        Format the response in Markdown.
        """
        
        system_message = "You are an expert technical writer specializing in API documentation. Generate clear, comprehensive, and well-structured API documentation."
        
        return self.llm_handler.generate_response(prompt, system_message)
    
    def _generate_database_schema_doc(self, project_data: Dict[str, Any], technical_details: Dict[str, Any] = None) -> str:
        """Generate database schema documentation"""
        prompt = f"""
        Generate comprehensive database schema documentation for the project: {project_data.get('project_name', 'Unknown Project')}
        
        Project Type: {project_data.get('project_type', 'Unknown')}
        Project Path: {project_data.get('project_path', 'Unknown')}
        
        Code Analysis:
        {self._format_code_analysis(project_data.get('code_analysis', {}))}
        
        Dependencies:
        {self._format_dependencies(project_data.get('dependencies', {}))}
        
        Please generate detailed database schema documentation including:
        1. Database overview and technology used
        2. Entity Relationship Diagram (ERD) description
        3. Table definitions with columns, data types, and constraints
        4. Relationships between tables
        5. Indexes and performance considerations
        6. Data migration strategies
        7. Backup and recovery procedures
        
        Format the response in Markdown.
        """
        
        system_message = "You are an expert database architect and technical writer. Generate clear, comprehensive database schema documentation."
        
        return self.llm_handler.generate_response(prompt, system_message)
    
    def _generate_installation_guide(self, project_data: Dict[str, Any], technical_details: Dict[str, Any] = None) -> str:
        """Generate installation guide"""
        prompt = f"""
        Generate a comprehensive installation guide for the project: {project_data.get('project_name', 'Unknown Project')}
        
        Project Type: {project_data.get('project_type', 'Unknown')}
        Project Path: {project_data.get('project_path', 'Unknown')}
        
        Dependencies:
        {self._format_dependencies(project_data.get('dependencies', {}))}
        
        Project Structure:
        {self._format_structure(project_data.get('structure', {}))}
        
        Please generate a detailed installation guide including:
        1. Prerequisites and system requirements
        2. Step-by-step installation instructions
        3. Configuration setup
        4. Environment variables setup
        5. Database setup (if applicable)
        6. Testing the installation
        7. Troubleshooting common issues
        8. Development environment setup
        
        Format the response in Markdown.
        """
        
        system_message = "You are an expert DevOps engineer and technical writer. Generate clear, step-by-step installation instructions."
        
        return self.llm_handler.generate_response(prompt, system_message)
    
    def _generate_architecture_doc(self, project_data: Dict[str, Any], technical_details: Dict[str, Any] = None) -> str:
        """Generate architecture documentation"""
        prompt = f"""
        Generate comprehensive architecture documentation for the project: {project_data.get('project_name', 'Unknown Project')}
        
        Project Type: {project_data.get('project_type', 'Unknown')}
        Project Path: {project_data.get('project_path', 'Unknown')}
        
        Code Analysis:
        {self._format_code_analysis(project_data.get('code_analysis', {}))}
        
        Dependencies:
        {self._format_dependencies(project_data.get('dependencies', {}))}
        
        Project Structure:
        {self._format_structure(project_data.get('structure', {}))}
        
        Please generate detailed architecture documentation including:
        1. System overview and high-level architecture
        2. Component diagram and relationships
        3. Technology stack and rationale
        4. Data flow and processing
        5. Security considerations
        6. Scalability and performance
        7. Deployment architecture
        8. Monitoring and logging
        
        Format the response in Markdown.
        """
        
        system_message = "You are an expert software architect and technical writer. Generate comprehensive architecture documentation."
        
        return self.llm_handler.generate_response(prompt, system_message)
    
    def _generate_code_documentation(self, project_data: Dict[str, Any], technical_details: Dict[str, Any] = None) -> str:
        """Generate code documentation"""
        prompt = f"""
        Generate comprehensive code documentation for the project: {project_data.get('project_name', 'Unknown Project')}
        
        Project Type: {project_data.get('project_type', 'Unknown')}
        Project Path: {project_data.get('project_path', 'Unknown')}
        
        Code Analysis:
        {self._format_code_analysis(project_data.get('code_analysis', {}))}
        
        Project Structure:
        {self._format_structure(project_data.get('structure', {}))}
        
        Please generate detailed code documentation including:
        1. Codebase overview and organization
        2. Key modules and their purposes
        3. Important functions and classes
        4. Coding standards and conventions
        5. Testing strategy and coverage
        6. Build and deployment process
        7. Code examples and usage patterns
        8. Contributing guidelines
        
        Format the response in Markdown.
        """
        
        system_message = "You are an expert software developer and technical writer. Generate comprehensive code documentation."
        
        return self.llm_handler.generate_response(prompt, system_message)
    
    def _generate_user_manual(self, project_data: Dict[str, Any], technical_details: Dict[str, Any] = None) -> str:
        """Generate user manual"""
        prompt = f"""
        Generate a comprehensive user manual for the project: {project_data.get('project_name', 'Unknown Project')}
        
        Project Type: {project_data.get('project_type', 'Unknown')}
        Project Path: {project_data.get('project_path', 'Unknown')}
        
        Code Analysis:
        {self._format_code_analysis(project_data.get('code_analysis', {}))}
        
        Please generate a detailed user manual including:
        1. Introduction and purpose of the application
        2. Getting started guide
        3. Features and functionality overview
        4. Step-by-step usage instructions
        5. User interface walkthrough
        6. Common tasks and workflows
        7. Troubleshooting and FAQ
        8. Tips and best practices
        
        Format the response in Markdown with a focus on user-friendly language.
        """
        
        system_message = "You are an expert technical writer specializing in user documentation. Generate clear, user-friendly documentation."
        
        return self.llm_handler.generate_response(prompt, system_message)
    
    def _generate_business_requirements(self, project_data: Dict[str, Any], technical_details: Dict[str, Any] = None) -> str:
        """Generate business requirements document"""
        prompt = f"""
        Generate a comprehensive business requirements document for the project: {project_data.get('project_name', 'Unknown Project')}
        
        Project Type: {project_data.get('project_type', 'Unknown')}
        Project Path: {project_data.get('project_path', 'Unknown')}
        
        Code Analysis:
        {self._format_code_analysis(project_data.get('code_analysis', {}))}
        
        Please generate a detailed business requirements document including:
        1. Executive summary
        2. Business objectives and goals
        3. Stakeholder analysis
        4. Functional requirements
        5. Non-functional requirements
        6. Business processes and workflows
        7. Success criteria and KPIs
        8. Risk assessment and mitigation
        9. Timeline and milestones
        
        Format the response in Markdown with a business focus.
        """
        
        system_message = "You are an expert business analyst and technical writer. Generate comprehensive business requirements documentation."
        
        return self.llm_handler.generate_response(prompt, system_message)
    
    def _generate_sales_pitch(self, project_data: Dict[str, Any], technical_details: Dict[str, Any] = None) -> str:
        """Generate sales pitch document"""
        prompt = f"""
        Generate a compelling sales pitch document for the project: {project_data.get('project_name', 'Unknown Project')}
        
        Project Type: {project_data.get('project_type', 'Unknown')}
        Project Path: {project_data.get('project_path', 'Unknown')}
        
        Code Analysis:
        {self._format_code_analysis(project_data.get('code_analysis', {}))}
        
        Please generate a compelling sales pitch including:
        1. Executive summary and value proposition
        2. Problem statement and market opportunity
        3. Solution overview and key features
        4. Competitive advantages and differentiation
        5. Target market and customer segments
        6. Revenue model and pricing strategy
        7. Go-to-market strategy
        8. Success stories and testimonials
        9. Call to action and next steps
        
        Format the response in Markdown with persuasive language.
        """
        
        system_message = "You are an expert sales and marketing professional. Generate compelling sales documentation."
        
        return self.llm_handler.generate_response(prompt, system_message)
    
    def _generate_project_overview(self, project_data: Dict[str, Any], technical_details: Dict[str, Any] = None) -> str:
        """Generate project overview document"""
        prompt = f"""
        Generate a comprehensive project overview document for: {project_data.get('project_name', 'Unknown Project')}
        
        Project Type: {project_data.get('project_type', 'Unknown')}
        Project Path: {project_data.get('project_path', 'Unknown')}
        
        Code Analysis:
        {self._format_code_analysis(project_data.get('code_analysis', {}))}
        
        Dependencies:
        {self._format_dependencies(project_data.get('dependencies', {}))}
        
        Project Structure:
        {self._format_structure(project_data.get('structure', {}))}
        
        Please generate a comprehensive project overview including:
        1. Project summary and purpose
        2. Key features and capabilities
        3. Technology stack and architecture
        4. Development status and roadmap
        5. Team and contributors
        6. Documentation and resources
        7. Getting started guide
        8. Support and community
        
        Format the response in Markdown.
        """
        
        system_message = "You are an expert project manager and technical writer. Generate comprehensive project overview documentation."
        
        return self.llm_handler.generate_response(prompt, system_message)
    
    def _format_code_analysis(self, code_analysis: Dict[str, Any]) -> str:
        """Format code analysis for prompts"""
        if not code_analysis:
            return "No code analysis available"
        
        formatted = []
        
        if code_analysis.get('python_files'):
            formatted.append(f"Python Files: {len(code_analysis['python_files'])}")
            for py_file in code_analysis['python_files'][:5]:  # Limit to first 5
                formatted.append(f"  - {py_file.get('file', 'Unknown')}: {len(py_file.get('functions', []))} functions, {len(py_file.get('classes', []))} classes")
        
        if code_analysis.get('javascript_files'):
            formatted.append(f"JavaScript Files: {len(code_analysis['javascript_files'])}")
            for js_file in code_analysis['javascript_files'][:5]:  # Limit to first 5
                formatted.append(f"  - {js_file.get('file', 'Unknown')}: {len(js_file.get('functions', []))} functions, {len(js_file.get('classes', []))} classes")
        
        return '\n'.join(formatted)
    
    def _format_dependencies(self, dependencies: Dict[str, Any]) -> str:
        """Format dependencies for prompts"""
        if not dependencies:
            return "No dependencies found"
        
        formatted = []
        for lang, deps in dependencies.items():
            if isinstance(deps, list):
                formatted.append(f"{lang.title()}: {', '.join(deps[:10])}")  # Limit to first 10
            elif isinstance(deps, dict):
                deps_list = list(deps.get('dependencies', {}).keys()) + list(deps.get('devDependencies', {}).keys())
                formatted.append(f"{lang.title()}: {', '.join(deps_list[:10])}")  # Limit to first 10
        
        return '\n'.join(formatted)
    
    def _format_structure(self, structure: Dict[str, Any]) -> str:
        """Format project structure for prompts"""
        if not structure:
            return "No structure information available"
        
        return f"Files: {structure.get('file_count', 0)}, Size: {structure.get('total_size', 0)} bytes, Directories: {len(structure.get('directories', []))}" 