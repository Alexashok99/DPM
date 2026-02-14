"""Tool to generate optimized project context for AI assistance."""

import os
from pathlib import Path
from typing import List, Set, Optional
from tools.base_tool import BaseTool
from util.utils import Utils

class FullContextTool(BaseTool):
    """Create optimized project context for AI assistance with flexible filtering."""

    name = "📄 Generate AI Context"
    description = "Create optimized project context with filtering options for AI"

    # Default ignore settings
    DEFAULT_IGNORE_DIRS = {
        ".git", ".github", ".gitlab",
        ".venv", "venv", "env", "virtualenv",
        "__pycache__", ".pytest_cache", ".mypy_cache",
        ".idea", ".vscode", ".vs",
        "node_modules", "bower_components",
        "dist", "build", "out", "target",
        "instance", ".extra", "migrations", "logs",
        "static/images", "media",
        "coverage", ".coverage",
        "site-packages", ".eggs", "eggs",
    }

    DEFAULT_IGNORE_FILES = {
        ".DS_Store", "Thumbs.db", "desktop.ini",
        "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
        "full_project_context.txt", "ai_context.txt",
        "generate_context.py",
        "db.sqlite3", "database.db", "*.db",
        ".env", ".env.local", ".env.*",
        ".antigravityignore", ".gitignore",
        "requirements.txt", "requirements-dev.txt",
        "poetry.lock", "Pipfile.lock",
        "*.pyc", "*.pyo", "*.pyd",
        "*.so", "*.dll", "*.dylib",
        "*.log", "*.tmp", "*.temp",
        "*.cache", "*.swp", "*.swo",
    }

    # Prioritized extensions for AI understanding
    PRIORITY_EXTENSIONS = {
        ".py", ".js", ".jsx", ".ts", ".tsx",  # Code
        ".html", ".htm", ".css", ".scss", ".sass",  # Web
        ".json", ".yaml", ".yml", ".toml",  # Config
        ".md", ".txt", ".rst",  # Documentation
        ".sql", ".graphql", ".gql",  # Database
        ".java", ".cpp", ".c", ".h", ".hpp",  # Other languages
        ".go", ".rs", ".rb", ".php",
        ".cs", ".swift", ".kt", ".dart",
    }

    def run(self) -> None:
        """Execute the context generation process with user options."""
        Utils.clear_screen()
        Utils.print_header("🤖 AI-PROJECT CONTEXT GENERATOR")
        
        project_path = Utils.get_project_path()
        project_name = os.path.basename(project_path)
        
        print(f"\n📁 Project: {project_name}")
        print(f"📍 Location: {project_path}")
        
        # User configuration
        config = self._get_user_config()
        
        print(f"\n🔍 Scanning project...")
        
        # Generate structure
        tree_structure = self._generate_tree(project_path, config['ignore_dirs'])
        
        # Get file contents based on selection mode
        if config['selection_mode'] == 'custom':
            file_contents = self._get_custom_files_content(project_path, config)
        elif config['selection_mode'] == 'all':
            file_contents = self._get_all_files_content(project_path, config)
        else:  # smart
            file_contents = self._get_smart_files_content(project_path, config)
        
        # Prepare final output
        final_output = self._format_output(project_name, tree_structure, file_contents, config)
        
        # Preview
        self._show_preview(final_output)
        
        # Save options
        self._handle_save_options(project_name, final_output)
        
        input("\nPress Enter to continue...")
    
    def _get_user_config(self) -> dict:
        """Get user configuration for context generation."""
        config = {}
        
        print("\n⚙️  Configuration Options:")
        print("-" * 40)
        
        # Ignore directories
        print("\n1. Ignore Directories:")
        default_dirs = ", ".join(sorted(list(self.DEFAULT_IGNORE_DIRS))[:5]) + "..."
        print(f"   Default: {default_dirs}")
        custom_ignore = input("   Add more (comma separated, leave empty for default): ").strip()
        
        ignore_dirs = set(self.DEFAULT_IGNORE_DIRS)
        if custom_ignore:
            ignore_dirs.update([d.strip() for d in custom_ignore.split(',')])
        
        # Ignore files
        print("\n2. Ignore File Patterns:")
        print("   Default includes: *.log, *.tmp, .env*, etc.")
        custom_files = input("   Add more patterns (comma separated): ").strip()
        
        ignore_files = set(self.DEFAULT_IGNORE_FILES)
        if custom_files:
            ignore_files.update([f.strip() for f in custom_files.split(',')])
        
        # Selection mode
        print("\n3. File Selection Mode:")
        print("   [1] Smart (recommended) - Key files only")
        print("   [2] All - All readable files")
        print("   [3] Custom - Select specific files/folders")
        
        mode_choice = input("   Choose mode (1/2/3): ").strip()
        mode_map = {'1': 'smart', '2': 'all', '3': 'custom'}
        selection_mode = mode_map.get(mode_choice, 'smart')
        
        config.update({
            'ignore_dirs': ignore_dirs,
            'ignore_files': ignore_files,
            'selection_mode': selection_mode,
            'max_file_size': 10000,
            'max_total_size': 50000
        })
        
        return config
    
    def _generate_tree(self, start_path: str, ignore_dirs: Set[str]) -> str:
        """Generate tree structure with ignore support."""
        def _tree_recursive(path: Path, prefix: str = "", depth: int = 0, max_depth: int = 5) -> str:
            if depth > max_depth:
                return prefix + "└── [depth limit reached]\n"
            
            try:
                items = sorted(path.iterdir())
            except (PermissionError, OSError):
                return ""
            
            # Filter items
            dirs = []
            files = []
            for item in items:
                if item.name.startswith('.'):
                    continue
                    
                if item.is_dir():
                    if item.name not in ignore_dirs:
                        dirs.append(item)
                else:
                    files.append(item)
            
            all_items = dirs + files
            tree_str = ""
            
            for idx, item in enumerate(all_items):
                is_last = idx == len(all_items) - 1
                connector = "└── " if is_last else "├── "
                icon = "📁 " if item.is_dir() else "📄 "
                tree_str += f"{prefix}{connector}{icon}{item.name}\n"
                
                if item.is_dir():
                    extension = "    " if is_last else "│   "
                    tree_str += _tree_recursive(item, prefix + extension, depth + 1, max_depth)
            
            return tree_str
        
        return f"Project Tree:\n{_tree_recursive(Path(start_path))}"
    
    def _get_smart_files_content(self, project_path: str, config: dict) -> str:
        """Get contents of important files for AI understanding."""
        important_patterns = [
            "README*", "readme*",
            "requirements*.txt", "pyproject.toml", "package.json",
            "setup.py", "setup.cfg",
            "*.py", "*.js", "*.ts", "*.jsx", "*.tsx",
            "*.html", "*.css",
            "*.json", "*.yaml", "*.yml",
        ]
        
        content_str = ""
        total_size = 0
        
        for root, dirs, files in os.walk(project_path):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if d not in config['ignore_dirs']]
            
            for file in files:
                # Check ignore patterns
                if self._should_ignore_file(file, config['ignore_files']):
                    continue
                
                # Check if file is important
                if not self._is_important_file(file, important_patterns):
                    continue
                
                path = os.path.join(root, file)
                content = self._read_file_safe(path, config['max_file_size'])
                
                if content:
                    rel_path = os.path.relpath(path, project_path)
                    total_size += len(content)
                    
                    if total_size > config['max_total_size']:
                        content_str += f"\n[⚠️  Total size limit reached. Some files omitted.]\n"
                        break
                    
                    content_str += self._format_file_content(rel_path, content)
        
        return content_str
    
    def _get_all_files_content(self, project_path: str, config: dict) -> str:
        """Get contents of all allowed files."""
        content_str = ""
        total_size = 0
        
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if d not in config['ignore_dirs']]
            
            for file in files:
                if self._should_ignore_file(file, config['ignore_files']):
                    continue
                
                path = os.path.join(root, file)
                content = self._read_file_safe(path, config['max_file_size'])
                
                if content:
                    rel_path = os.path.relpath(path, project_path)
                    total_size += len(content)
                    
                    if total_size > config['max_total_size']:
                        content_str += f"\n[⚠️  Total size limit reached. Some files omitted.]\n"
                        break
                    
                    content_str += self._format_file_content(rel_path, content)
        
        return content_str
    
    def _get_custom_files_content(self, project_path: str, config: dict) -> str:
        """Get contents of user-selected files/folders."""
        print("\n🎯 Custom File Selection:")
        print("-" * 40)
        print("Enter file/folder paths (relative to project, one per line).")
        print("Type 'done' when finished, or 'tree' to see structure.")
        
        selected_paths = []
        
        while True:
            user_input = input("\nEnter path (or 'done'/'tree'): ").strip()
            
            if user_input.lower() == 'done':
                break
            elif user_input.lower() == 'tree':
                print("\nCurrent tree (first 2 levels):")
                self._show_quick_tree(project_path, 2)
                continue
            
            if user_input:
                full_path = os.path.join(project_path, user_input)
                if os.path.exists(full_path):
                    selected_paths.append(full_path)
                    print(f"✓ Added: {user_input}")
                else:
                    print(f"✗ Not found: {user_input}")
        
        if not selected_paths:
            print("No files selected. Using smart selection instead.")
            return self._get_smart_files_content(project_path, config)
        
        # Process selected paths
        content_str = ""
        total_size = 0
        
        for selected_path in selected_paths:
            if os.path.isfile(selected_path):
                content = self._read_file_safe(selected_path, config['max_file_size'])
                if content:
                    rel_path = os.path.relpath(selected_path, project_path)
                    total_size += len(content)
                    
                    if total_size > config['max_total_size']:
                        content_str += f"\n[⚠️  Total size limit reached.]\n"
                        break
                    
                    content_str += self._format_file_content(rel_path, content)
            
            elif os.path.isdir(selected_path):
                for root, dirs, files in os.walk(selected_path):
                    dirs[:] = [d for d in dirs if d not in config['ignore_dirs']]
                    
                    for file in files:
                        if self._should_ignore_file(file, config['ignore_files']):
                            continue
                        
                        path = os.path.join(root, file)
                        content = self._read_file_safe(path, config['max_file_size'])
                        
                        if content:
                            rel_path = os.path.relpath(path, project_path)
                            total_size += len(content)
                            
                            if total_size > config['max_total_size']:
                                content_str += f"\n[⚠️  Total size limit reached.]\n"
                                break
                            
                            content_str += self._format_file_content(rel_path, content)
        
        return content_str
    
    def _should_ignore_file(self, filename: str, ignore_patterns: Set[str]) -> bool:
        """Check if file should be ignored based on patterns."""
        for pattern in ignore_patterns:
            if pattern.startswith('*'):
                if filename.endswith(pattern[1:]):
                    return True
            elif filename == pattern:
                return True
        return False
    
    def _is_important_file(self, filename: str, patterns: List[str]) -> bool:
        """Check if file is important based on patterns."""
        import fnmatch
        
        for pattern in patterns:
            if fnmatch.fnmatch(filename, pattern):
                return True
        
        # Check by extension
        ext = os.path.splitext(filename)[1].lower()
        return ext in self.PRIORITY_EXTENSIONS
    
    def _read_file_safe(self, filepath: str, max_size: int) -> Optional[str]:
        """Safely read file with size limit."""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(max_size * 2)  # Read slightly more for truncation check
                
                if len(content) > max_size:
                    content = content[:max_size] + "\n\n...[File truncated due to size]..."
                
                return content if content.strip() else None
        except Exception as e:
            return f"[Error reading file: {e}]"
    
    def _format_file_content(self, rel_path: str, content: str) -> str:
        """Format file content for output."""
        separator = "=" * 60
        return f"\n{separator}\n📄 FILE: {rel_path}\n{separator}\n{content}\n"
    
    def _format_output(self, project_name: str, tree: str, contents: str, config: dict) -> str:
        """Format the final output."""
        output = f"""🤖 PROJECT CONTEXT FOR AI ASSISTANCE
{'=' * 60}
PROJECT: {project_name}
SELECTION MODE: {config['selection_mode'].upper()}
GENERATED: {Utils.get_timestamp()}
{'=' * 60}

📁 PROJECT STRUCTURE:
{tree}

{'=' * 60}
📝 FILE CONTENTS:
{contents}

{'=' * 60}
💡 FOR AI ASSISTANT:
This is the complete context of the project. Please analyze the structure
and code to provide accurate assistance. Key files include configuration
files, source code, and documentation.

When responding, reference specific files and paths from the structure above.
"""
        return output
    
    def _show_preview(self, output: str) -> None:
        """Show preview of generated context."""
        print("\n📋 PREVIEW:")
        print("-" * 60)
        
        lines = output.split('\n')
        for i, line in enumerate(lines[:30]):
            print(line)
        
        if len(lines) > 30:
            print(f"...\n(Showing first 30 of {len(lines)} lines)")
        
        print(f"\n📊 Statistics:")
        print(f"  • Total lines: {len(lines)}")
        print(f"  • Approx. size: {len(output.encode('utf-8')):,} bytes")
    
    def _show_quick_tree(self, path: str, depth: int = 2) -> None:
        """Show quick tree view."""
        def _quick_tree(p: Path, current_depth: int, max_depth: int):
            if current_depth > max_depth:
                return
            
            prefix = "  " * current_depth
            try:
                for item in sorted(p.iterdir()):
                    if item.name.startswith('.'):
                        continue
                    
                    icon = "📁" if item.is_dir() else "📄"
                    print(f"{prefix}{icon} {item.name}")
                    
                    if item.is_dir():
                        _quick_tree(item, current_depth + 1, max_depth)
            except:
                pass
        
        _quick_tree(Path(path), 0, depth)
    
    def _handle_save_options(self, project_name: str, content: str) -> None:
        """Handle file saving options."""
        print("\n💾 Save Options:")
        print("  [1] Save full context")
        print("  [2] Save only specific section")
        print("  [3] Save as AI prompt template")
        print("  [4] Don't save")
        
        choice = input("Choose option (1-4): ").strip()
        
        if choice == '4':
            return
        
        filename = input(f"Enter filename [{project_name}_context.txt]: ").strip()
        if not filename:
            filename = f"{project_name}_context.txt"
        
        if choice == '1':
            save_content = content
        elif choice == '2':
            print("\nSelect section to save:")
            print("  [1] Only project structure")
            print("  [2] Only file contents")
            section = input("Choose (1/2): ").strip()
            
            if section == '1':
                # Extract structure section
                lines = content.split('\n')
                start = next(i for i, line in enumerate(lines) if "PROJECT STRUCTURE:" in line)
                end = next(i for i, line in enumerate(lines[start+1:]) if "="*60 in line)
                save_content = '\n'.join(lines[start:start+end+1])
            else:
                # Extract contents section
                lines = content.split('\n')
                start = next(i for i, line in enumerate(lines) if "FILE CONTENTS:" in line)
                save_content = '\n'.join(lines[start:])
        else:  # choice == '3'
            save_content = self._create_ai_prompt_template(content, project_name)
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(save_content)
            
            print(f"✅ Saved to: {os.path.abspath(filename)}")
            print(f"📏 Size: {os.path.getsize(filename):,} bytes")
            
            # Show AI prompt suggestion
            if choice == '3':
                print("\n🤖 AI Prompt Suggestion:")
                print("=" * 60)
                print(save_content[:500] + "...\n[Full prompt in file]")
                
        except Exception as e:
            print(f"❌ Error saving file: {e}")
    
    def _create_ai_prompt_template(self, context: str, project_name: str) -> str:
        """Create an AI prompt template with the context."""
        return f"""You are an expert developer assistant. Below is the complete context of a project. Please analyze it thoroughly and provide accurate assistance.

PROJECT CONTEXT:
{context}

YOUR TASK:
Based on the project structure and code above, please:

1. First, understand the project architecture and main components
2. Identify key files, dependencies, and configuration
3. Provide specific, actionable advice or code

My specific request is: [Describe what you need help with here]

Please reference specific files and paths from the project structure in your response. Be detailed but concise."""