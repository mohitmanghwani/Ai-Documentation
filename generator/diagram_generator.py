"""
Diagram Generator - Generates Mermaid diagrams
"""

import logging
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any, List, Optional
import os

from .llm_handlers import BaseLLMHandler

logger = logging.getLogger(__name__)


class DiagramGenerator:
    """Generates Mermaid diagrams for projects"""
    
    def __init__(self, llm_handler: BaseLLMHandler):
        self.llm_handler = llm_handler
    
    def generate_diagrams(self, project_data: Dict[str, Any], technical_details: Dict[str, Any] = None) -> Dict[str, str]:
        """Generate all diagrams for the project"""
        diagrams = {}
        
        # Generate existing diagrams
        diagrams['system_architecture'] = self._generate_system_architecture(project_data, technical_details)
        diagrams['data_flow'] = self._generate_data_flow(project_data, technical_details)
        diagrams['component'] = self._generate_component_diagram(project_data, technical_details)
        
        # Generate new diagrams
        diagrams['er_diagram'] = self._generate_er_diagram(project_data, technical_details)
        diagrams['requirement_diagram'] = self._generate_requirement_diagram(project_data, technical_details)
        diagrams['gantt_chart'] = self._generate_gantt_chart(project_data, technical_details)
        diagrams['git_graph'] = self._generate_git_graph(project_data, technical_details)
        
        return diagrams
    
    def _generate_system_architecture(self, project_data: Dict[str, Any], technical_details: Dict[str, Any] = None) -> str:
        """Generate system architecture diagram"""
        prompt = f"""
        Generate ONLY a Mermaid system architecture diagram for the project: {project_data.get('project_name', 'Unknown Project')}
        
        Project Type: {project_data.get('project_type', 'Unknown')}
        Code Analysis: {self._format_code_analysis(project_data.get('code_analysis', {}))}
        Dependencies: {self._format_dependencies(project_data.get('dependencies', {}))}
        
        Requirements:
        1. Main system components and their relationships
        2. Data flow between components
        3. External dependencies and services
        4. Technology stack layers
        5. Security boundaries
        
        IMPORTANT: Return ONLY the Mermaid code starting with ```mermaid and ending with ```. Do not include any explanations or text outside the code block.
        Use Mermaid graph syntax with clear, descriptive node names and relationships.
        """

        prompt1= f"""
        Generate ONLY a Mermaid system architecture diagram for the project: {project_data.get('project_name', 'Unknown Project')}.

        Project Type: {project_data.get('project_type', 'Unknown')}
        Code Analysis: {self._format_code_analysis(project_data.get('code_analysis', {}))}
        Dependencies: {self._format_dependencies(project_data.get('dependencies', {}))}

        Strict, Non-Negotiable Requirements:

        1. Use Mermaid 'classDiagram' syntax ONLY. No other diagram types allowed.
        2. The diagram MUST start with:
        ```mermaid
        classDiagram
            class ComponentName {{
                + attribute_or_function1
                + attribute_or_function2
            }}
        3. Main system components and their relationships
        4. Include external services, databases, APIs, etc.
        5. Do NOT generate any explanation — ONLY valid Mermaid diagram.
        6. Technology stack layers
        7. Security boundaries
        8. No spaces in class names. Use CamelCase or snake_case naming. (e.g., Valid: DataService or data_service)
        9. All classes must be declared BEFORE they are referenced in relationships.
        10. If you need to represent files, functions, or attributes, do so inside their corresponding class using the '+' symbol (e.g., + 5 functions).
        11. Do NOT include explanations, descriptions, comments, or markdown outside of the Mermaid code block.

        Example Start:

        ```mermaid
        classDiagram
            class Frontend {{
                + attribute1: string
                + method1()
            }}
            class Backend {{
                + attribute2: number
                + method2()
            }}
            Frontend --> Backend
        ```

        Ensure Mermaid syntax validity.
        """
        
        system_message = "You are an expert software architect. Generate ONLY Mermaid diagram code without any explanations or text outside the code block."
        
        response = self.llm_handler.generate_response(prompt1, system_message)
        
        # Extract Mermaid code from response
        if '```mermaid' in response:
            start = response.find('```mermaid') + 10
            end = response.find('```', start)
            if end != -1:
                return response[start:end].strip()
        
        # If no code block found, try to extract any graph-like content
        if 'graph' in response.lower():
            lines = response.split('\n')
            mermaid_lines = []
            in_graph = False
            for line in lines:
                if 'graph' in line.lower():
                    in_graph = True
                if in_graph:
                    mermaid_lines.append(line)
                    if line.strip().endswith(';') or 'end' in line.lower():
                        break
            if mermaid_lines:
                return '\n'.join(mermaid_lines)
    
    def _generate_data_flow(self, project_data: Dict[str, Any], technical_details: Dict[str, Any] = None) -> str:
        """Generate data flow diagram"""
        prompt = f"""
        Generate ONLY a Mermaid data flow diagram for the project: {project_data.get('project_name', 'Unknown Project')}
        
        Project Type: {project_data.get('project_type', 'Unknown')}
        Code Analysis: {self._format_code_analysis(project_data.get('code_analysis', {}))}
        Dependencies: {self._format_dependencies(project_data.get('dependencies', {}))}
        
        Requirements:
        1. Data sources and destinations
        2. Data processing steps and transformations
        3. Data storage locations
        4. Data movement between components
        5. Data validation and error handling
        
        IMPORTANT: Return ONLY the Mermaid code starting with ```mermaid and ending with ```. Do not include any explanations or text outside the code block.
        Use Mermaid flowchart syntax with clear data flow paths and processing steps.
        """

        prompt1= f"""
        Generate ONLY a Mermaid data flow diagram for the project: {project_data.get('project_name', 'Unknown Project')}.

        Project Type: {project_data.get('project_type', 'Unknown')}
        Code Analysis: {self._format_code_analysis(project_data.get('code_analysis', {}))}
        Dependencies: {self._format_dependencies(project_data.get('dependencies', {}))}

        Strict Requirements:
        1. Use Mermaid 'sequenceDiagram' syntax ONLY.
        2. Show data sources, destinations, processing steps and transformations.
        3. Do NOT mix with any other diagram types.
        4. Diagram must start with: ```mermaid\nsequenceDiagram
        5. No explanations or non-Mermaid text in the response.
        6. Data validation and error handling
        7. Data storage locations
        8. Data movement between components

        Example Start:

        ```mermaid
        sequenceDiagram
            User->>+Server: Request
            Server->>+Database: Query
            Database-->>-Server: Response
            Server-->>-User: Response
        ```

        Ensure Mermaid syntax validity.
        """
        
        system_message = "You are an expert data architect. Generate ONLY Mermaid diagram code without any explanations or text outside the code block."
        
        response = self.llm_handler.generate_response(prompt1, system_message)
        
        # Extract Mermaid code from response
        if '```mermaid' in response:
            start = response.find('```mermaid') + 10
            end = response.find('```', start)
            if end != -1:
                return response[start:end].strip()
        
        # If no code block found, try to extract any flowchart-like content
        if 'flowchart' in response.lower():
            lines = response.split('\n')
            mermaid_lines = []
            in_flowchart = False
            for line in lines:
                if 'flowchart' in line.lower():
                    in_flowchart = True
                if in_flowchart:
                    mermaid_lines.append(line)
                    if line.strip().endswith(';') or 'end' in line.lower():
                        break
            if mermaid_lines:
                return '\n'.join(mermaid_lines)
        
    
    def _generate_component_diagram(self, project_data: Dict[str, Any], technical_details: Dict[str, Any] = None) -> str:
        """Generate component diagram"""
        prompt = f"""
        Generate ONLY a Mermaid component diagram for the project: {project_data.get('project_name', 'Unknown Project')}
        
        Project Type: {project_data.get('project_type', 'Unknown')}
        Code Analysis: {self._format_code_analysis(project_data.get('code_analysis', {}))}
        Dependencies: {self._format_dependencies(project_data.get('dependencies', {}))}
        
        Requirements:
        1. Main software components and modules
        2. Component interfaces and APIs
        3. Component dependencies and relationships
        4. Component responsibilities and functions
        5. Component communication patterns
        
        IMPORTANT: Return ONLY the Mermaid code starting with ```mermaid and ending with ```. Do not include any explanations or text outside the code block.
        Use Mermaid graph syntax with clear component boundaries and interfaces.
        """

        prompt1= f"""
        Generate ONLY a Mermaid component diagram for the project: {project_data.get('project_name', 'Unknown Project')}.

        Project Type: {project_data.get('project_type', 'Unknown')}
        Code Analysis: {self._format_code_analysis(project_data.get('code_analysis', {}))}
        Dependencies: {self._format_dependencies(project_data.get('dependencies', {}))}

        Strict Requirements:
        1. Use Mermaid 'classDiagram' or 'sequenceDiagram' only.
        2. Show main software components/modules.
        3. Show component interfaces and APIs.
        4. Show component dependencies and relationships.
        5. Show component responsibilities and functions.
        6. Show component communication patterns.
        6. Do NOT generate explanatory text — ONLY valid Mermaid code block.

        Example Start (you MUST follow this pattern):

        ```mermaid
        classDiagram
            class ComponentA {{
                + attribute1: string
                + method1()
            }}
            class ComponentB {{
                + attribute2: number
                + method2()
            }}
            ComponentA --> ComponentB
        ```

        Ensure Mermaid syntax correctness for 'classDiagram' or 'sequenceDiagram'.
        """
        
        system_message = "You are an expert software architect. Generate ONLY Mermaid diagram code without any explanations or text outside the code block."
        
        response = self.llm_handler.generate_response(prompt1, system_message)
        
        # Extract Mermaid code from response
        if '```mermaid' in response:
            start = response.find('```mermaid') + 10
            end = response.find('```', start)
            if end != -1:
                return response[start:end].strip()
        
        # If no code block found, try to extract any graph-like content
        if 'graph' in response.lower():
            lines = response.split('\n')
            mermaid_lines = []
            in_graph = False
            for line in lines:
                if 'graph' in line.lower():
                    in_graph = True
                if in_graph:
                    mermaid_lines.append(line)
                    if line.strip().endswith(';') or 'end' in line.lower():
                        break
            if mermaid_lines:
                return '\n'.join(mermaid_lines)
    
    def _generate_er_diagram(self, project_data: Dict[str, Any], technical_details: Dict[str, Any] = None) -> str:
        """Generate ER diagram for database structures"""
        prompt = f"""
        Generate ONLY a Mermaid ER diagram for the project: {project_data.get('project_name', 'Unknown Project')}.
        
        Project Type: {project_data.get('project_type', 'Unknown')}
        Code Analysis: {self._format_code_analysis(project_data.get('code_analysis', {}))}
        Dependencies: {self._format_dependencies(project_data.get('dependencies', {}))}
        
        Strict Requirements:
        1. Use Mermaid 'erDiagram' syntax ONLY.
        2. Show database entities, attributes, and relationships.
        3. Include primary keys, foreign keys, and data types.
        4. Show cardinality relationships (1:1, 1:N, M:N).
        5. Diagram must start with: ```mermaid\nerDiagram
        6. No explanations or non-Mermaid text in the response.
        
        Example Start:
        ```mermaid
        erDiagram
            USER {{
                int id PK
                string name
                string email
                datetime created_at
            }}
            POST {{
                int id PK
                int user_id FK
                string title
                text content
                datetime created_at
            }}
            USER ||--o{{ POST : "creates"
        ```
        
        Ensure Mermaid syntax validity.
        """
        
        system_message = "You are an expert database architect. Generate ONLY Mermaid ER diagram code without any explanations or text outside the code block."
        
        response = self.llm_handler.generate_response(prompt, system_message)
        
        # Extract Mermaid code from response
        if '```mermaid' in response:
            start = response.find('```mermaid') + 10
            end = response.find('```', start)
            if end != -1:
                return response[start:end].strip()
        
        # If no code block found, try to extract any erDiagram-like content
        if 'erDiagram' in response.lower():
            lines = response.split('\n')
            mermaid_lines = []
            in_er = False
            for line in lines:
                if 'erDiagram' in line.lower():
                    in_er = True
                if in_er:
                    mermaid_lines.append(line)
                    if line.strip().endswith(';') or 'end' in line.lower():
                        break
            if mermaid_lines:
                return '\n'.join(mermaid_lines)
    
    def _generate_requirement_diagram(self, project_data: Dict[str, Any], technical_details: Dict[str, Any] = None) -> str:
        """Generate requirement diagram for functional and non-functional requirements"""
        prompt = f"""
        Generate ONLY a Mermaid requirement diagram for the project: {project_data.get('project_name', 'Unknown Project')}.
        
        Project Type: {project_data.get('project_type', 'Unknown')}
        Code Analysis: {self._format_code_analysis(project_data.get('code_analysis', {}))}
        Dependencies: {self._format_dependencies(project_data.get('dependencies', {}))}
        
        Strict Requirements:
        1. Use Mermaid 'graph TD' syntax for requirement hierarchy.
        2. Show functional and non-functional requirements.
        3. Group requirements by categories (Performance, Security, Usability, etc.).
        4. Show requirement dependencies and relationships.
        5. Diagram must start with: ```mermaid\ngraph TD
        6. No explanations or non-Mermaid text in the response.
        
        Example Start:
        ```mermaid
        graph TD
            A[Project Requirements] --> B[Functional Requirements]
            A --> C[Non-Functional Requirements]
            B --> D[User Authentication]
            B --> E[Data Processing]
            C --> F[Performance]
            C --> G[Security]
            C --> H[Usability]
        ```
        
        Ensure Mermaid syntax validity.
        """
        
        system_message = "You are an expert requirements analyst. Generate ONLY Mermaid requirement diagram code without any explanations or text outside the code block."
        
        response = self.llm_handler.generate_response(prompt, system_message)
        
        # Extract Mermaid code from response
        if '```mermaid' in response:
            start = response.find('```mermaid') + 10
            end = response.find('```', start)
            if end != -1:
                return response[start:end].strip()
        
        # If no code block found, try to extract any graph-like content
        if 'graph' in response.lower():
            lines = response.split('\n')
            mermaid_lines = []
            in_graph = False
            for line in lines:
                if 'graph' in line.lower():
                    in_graph = True
                if in_graph:
                    mermaid_lines.append(line)
                    if line.strip().endswith(';') or 'end' in line.lower():
                        break
            if mermaid_lines:
                return '\n'.join(mermaid_lines)
    
    def _generate_gantt_chart(self, project_data: Dict[str, Any], technical_details: Dict[str, Any] = None) -> str:
        """Generate Gantt chart for project timeline and milestones"""
        # Extract business requirements for timeline information
        business_requirements = technical_details.get('business_requirements', '') if technical_details else ''
        project_overview = technical_details.get('project_overview', '') if technical_details else ''
        
        prompt = f"""
        Generate ONLY a Mermaid Gantt chart for the project: {project_data.get('project_name', 'Unknown Project')}.
        
        Project Type: {project_data.get('project_type', 'Unknown')}
        Code Analysis: {self._format_code_analysis(project_data.get('code_analysis', {}))}
        Dependencies: {self._format_dependencies(project_data.get('dependencies', {}))}
        
        Business Context:
        {business_requirements[:500] if business_requirements else 'No business requirements available'}
        
        Project Overview:
        {project_overview[:500] if project_overview else 'No project overview available'}
        
        Strict Requirements:
        1. Use Mermaid 'gantt' syntax ONLY.
        2. Show project phases, tasks, and milestones based on business requirements.
        3. Include realistic timelines and dependencies.
        4. Show task completion status and durations.
        5. Diagram must start with: ```mermaid\ngantt
        6. No explanations or non-Mermaid text in the response.
        7. Use business requirements to determine project phases and milestones.
        
        Example Start:
        ```mermaid
        gantt
            title Project Timeline
            dateFormat  YYYY-MM-DD
            section Planning
            Requirements Analysis    :done, req1, 2024-01-01, 7d
            Design Phase           :active, design, 2024-01-08, 14d
            section Development
            Implementation         :dev, 2024-01-22, 21d
            Testing               :test, after dev, 7d
        ```
        
        Ensure Mermaid syntax validity.
        """
        
        system_message = "You are an expert project manager. Generate ONLY Mermaid Gantt chart code without any explanations or text outside the code block."
        
        response = self.llm_handler.generate_response(prompt, system_message)
        
        # Extract Mermaid code from response
        if '```mermaid' in response:
            start = response.find('```mermaid') + 10
            end = response.find('```', start)
            if end != -1:
                return response[start:end].strip()
        
        # If no code block found, try to extract any gantt-like content
        if 'gantt' in response.lower():
            lines = response.split('\n')
            mermaid_lines = []
            in_gantt = False
            for line in lines:
                if 'gantt' in line.lower():
                    in_gantt = True
                if in_gantt:
                    mermaid_lines.append(line)
                    if line.strip().endswith(';') or 'end' in line.lower():
                        break
            if mermaid_lines:
                return '\n'.join(mermaid_lines)
    
    def _generate_git_graph(self, project_data: Dict[str, Any], technical_details: Dict[str, Any] = None) -> str:
        """Generate git graph diagram from project git history"""
        git_history = project_data.get('git_history', {})
        
        if not git_history.get('is_git_repo', False):
            return """gitGraph
    commit id: "no-git"
    note right of "no-git": "No Git repository found"
    commit id: "placeholder"
    note right of "placeholder": "This project is not a Git repository" """
        
        prompt = f"""
        Generate ONLY a Mermaid git graph diagram for the project: {project_data.get('project_name', 'Unknown Project')}.
        
        Git History Information:
        - Current Branch: {git_history.get('branch', 'Unknown')}
        - Total Commits: {git_history.get('commit_count', 0)}
        - Recent Commits: {git_history.get('recent_commits', [])}
        - Branches: {git_history.get('branches', [])}
        - Last Commit: {git_history.get('last_commit', {})}
        
        Strict Requirements:
        1. Use Mermaid 'gitGraph' syntax ONLY.
        2. Show main branch, feature branches, and commits.
        3. Include realistic commit, tag and branch names.
        4. Show merge points and branch relationships.
        5. Diagram must start with: ```mermaid\ngitGraph
        6. No explanations or non-Mermaid text in the response.
        7. Use actual Git history data if available.
        8. Do not use message and label in the commit, tag and branch names.
        
        Example Start:
        ```mermaid
        gitGraph
            commit
            branch feature-branch
            checkout feature-branch
            commit
            commit
            checkout main
            merge feature-branch
            commit
        ```
        
        Ensure Mermaid syntax validity.
        """
        
        system_message = "You are an expert Git workflow specialist. Generate ONLY Mermaid git graph code without any explanations or text outside the code block."
        
        response = self.llm_handler.generate_response(prompt, system_message)
        
        # Extract Mermaid code from response
        if '```mermaid' in response:
            start = response.find('```mermaid') + 10
            end = response.find('```', start)
            if end != -1:
                return response[start:end].strip()
        
        # If no code block found, try to extract any gitgraph-like content
        if 'gitGraph' in response.lower():
            lines = response.split('\n')
            mermaid_lines = []
            in_gitgraph = False
            for line in lines:
                if 'gitgraph' in line.lower():
                    in_gitgraph = True
                if in_gitgraph:
                    mermaid_lines.append(line)
                    if line.strip().endswith(';') or 'end' in line.lower():
                        break
            if mermaid_lines:
                return '\n'.join(mermaid_lines)
    
    def save_diagrams(self, diagrams: Dict[str, str], output_dir: Path) -> Dict[str, str]:
        """Save diagrams as both .mmd and .png files"""
        saved_files = {}
        
        # Create diagrams directory
        diagrams_dir = output_dir / "diagrams"
        diagrams_dir.mkdir(exist_ok=True)
        
        for diagram_type, mermaid_code in diagrams.items():
            try:
                # Save Mermaid code
                mmd_file = diagrams_dir / f"{diagram_type}.mmd"
                with open(mmd_file, 'w', encoding='utf-8') as f:
                    f.write(mermaid_code)
                
                # Generate PNG from Mermaid
                png_file = diagrams_dir / f"{diagram_type}.png"
                self._generate_png_from_mermaid(mermaid_code, png_file)
                
                saved_files[diagram_type] = {
                    'mmd': str(mmd_file),
                    'png': str(png_file)
                }
                
                logger.info(f"Saved {diagram_type} diagram: {mmd_file}, {png_file}")
                
            except Exception as e:
                logger.error(f"Error saving {diagram_type} diagram: {e}")
                saved_files[diagram_type] = {
                    'mmd': str(mmd_file) if 'mmd_file' in locals() else None,
                    'png': None,
                    'error': str(e)
                }
        
        return saved_files
    
    def _generate_png_from_mermaid(self, mermaid_code: str, output_file: Path) -> bool:
        """Generate PNG from Mermaid code using mmdc CLI"""
        try:
            # Check if mmdc is available
            result = subprocess.run(['mmdc', '--version'], capture_output=True, text=True)
            if result.returncode != 0:
                logger.warning("mmdc (Mermaid CLI) not available, skipping PNG generation")
                logger.warning(f"mmdc error: {result.stderr}")
                return False
            
            # Validate Mermaid code
            if not mermaid_code.strip():
                logger.warning("Empty Mermaid code, skipping PNG generation")
                return False
            
            # Check if code starts with valid Mermaid syntax
            mermaid_code = mermaid_code.strip()
            if not any(mermaid_code.startswith(prefix) for prefix in ['graph', 'flowchart', 'sequenceDiagram', 'classDiagram', 'stateDiagram', 'erDiagram', 'gantt', 'gitgraph']):
                logger.warning(f"Invalid Mermaid syntax, skipping PNG generation: {mermaid_code[:100]}...")
                return False
            
            # Create temporary input file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False, encoding='utf-8') as temp_file:
                temp_file.write(mermaid_code)
                temp_input = temp_file.name
            
            try:
                # Generate PNG using mmdc
                cmd = [
                    'mmdc',
                    '-i', temp_input,
                    '-o', str(output_file),
                    '-b', 'transparent',
                    '-w', '1200',
                    '-H', '800'
                ]
                
                logger.info(f"Running mmdc command: {' '.join(cmd)}")
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    if output_file.exists() and output_file.stat().st_size > 0:
                        logger.info(f"Generated PNG: {output_file} ({output_file.stat().st_size} bytes)")
                        return True
                    else:
                        logger.error(f"PNG file not created or empty: {output_file}")
                        return False
                else:
                    logger.error(f"Error generating PNG: {result.stderr}")
                    logger.error(f"mmdc stdout: {result.stdout}")
                    return False
                    
            finally:
                # Clean up temporary file
                try:
                    os.unlink(temp_input)
                except:
                    pass
                
        except FileNotFoundError:
            logger.warning("mmdc (Mermaid CLI) not found in PATH")
            logger.warning("Please install Mermaid CLI: npm install -g @mermaid-js/mermaid-cli")
            return False
        except subprocess.TimeoutExpired:
            logger.error("PNG generation timed out")
            return False
        except Exception as e:
            logger.error(f"Error generating PNG: {e}")
            return False
    
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