

class Config:
    """Configuration class for storing ignore lists and settings."""
    
    # Default ignore directories
    DEFAULT_IGNORE_DIRS = {
        ".git",
        ".venv",
        "venv",
        "env",
        "__pycache__",
        ".idea",
        ".vscode",
        "node_modules",
        "dist",
        "build",
        ".antigravityignore",
        "migrations",
    }

    # Default ignore files
    DEFAULT_IGNORE_FILES = {
        ".DS_Store",
        ".antigravityignore",
        ".gitignore",
        "Thumbs.db",
        "project_structure.txt",
        "generate_structure.py",
    }

    def __init__(self):
        """Initialize Config with default ignore lists."""
        self.ignore_dirs = set(self.DEFAULT_IGNORE_DIRS)
        self.ignore_files = set(self.DEFAULT_IGNORE_FILES)

    def add_ignore_dir(self, dir_name: str) -> None:
        """Add a directory to ignore list."""
        self.ignore_dirs.add(dir_name)

    def add_ignore_dirs(self, dir_list: list[str]) -> None:
        """Add multiple directories to ignore list."""
        self.ignore_dirs.update(dir_list)

    def add_ignore_file(self, file_name: str) -> None:
        """Add a file to ignore list."""
        self.ignore_files.add(file_name)

    def add_ignore_files(self, file_list: list[str]) -> None:
        """Add multiple files to ignore list."""
        self.ignore_files.update(file_list)

    def remove_ignore_dir(self, dir_name: str) -> None:
        """Remove a directory from ignore list."""
        self.ignore_dirs.discard(dir_name)

    def remove_ignore_file(self, file_name: str) -> None:
        """Remove a file from ignore list."""
        self.ignore_files.discard(file_name)

    def get_ignore_dirs(self) -> list[str]:
        """Get current ignore directories sorted."""
        return sorted(self.ignore_dirs)

    def get_ignore_files(self) -> list[str]:
        """Get current ignore files sorted."""
        return sorted(self.ignore_files)

    def reset_to_defaults(self) -> None:
        """Reset to default ignore lists."""
        self.ignore_dirs = set(self.DEFAULT_IGNORE_DIRS)
        self.ignore_files = set(self.DEFAULT_IGNORE_FILES)

