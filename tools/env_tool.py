"""Tool for environment management."""

import os
import shutil
import subprocess
import sys
from typing import Tuple
from tools.base_tool import BaseTool
from util.utils import Utils

class EnvTool(BaseTool):
    """Manage virtual environments and environment files."""

    name = "🐍 Environment Manager"
    description = "Create/delete virtual env, create/delete .env file"

    def run(self) -> None:
        """Display environment management menu."""
        while True:
            Utils.clear_screen()
            Utils.print_header("ENVIRONMENT MANAGER")

            print("\n1. Create Virtual Environment (.venv)")
            print("2. Delete Virtual Environment")
            print("3. Create .env File")
            print("4. Delete .env File")
            print("5. List Environment Variables")
            print("6. Check Python Environment")
            print("7. Back to Main Menu")

            choice = input("\nSelect option (1-7): ").strip()

            if choice == "1":
                self._create_venv()
            elif choice == "2":
                self._delete_venv()
            elif choice == "3":
                self._create_env_file()
            elif choice == "4":
                self._delete_env_file()
            elif choice == "5":
                self._list_env_vars()
            elif choice == "6":
                self._check_python_env()
            elif choice == "7":
                break
            else:
                print("❌ Invalid option")

            if choice != "7":
                input("\nPress Enter to continue...")

    def _create_venv(self) -> None:
        """Create a virtual environment."""
        Utils.clear_screen()
        Utils.print_header("CREATE VIRTUAL ENVIRONMENT")

        current_dir = os.getcwd()
        print(f"📂 Current directory: {current_dir}")

        print("\n🔧 Virtual Environment Options:")
        print("   1. .venv (Recommended)")
        print("   2. venv")
        print("   3. Custom name")

        choice = input("\nSelect option (1-3): ").strip()

        if choice == "1":
            venv_name = ".venv"
        elif choice == "2":
            venv_name = "venv"
        elif choice == "3":
            venv_name = input("Enter virtual environment name: ").strip()
            if not venv_name:
                print("❌ Name cannot be empty.")
                return
        else:
            print("❌ Invalid option.")
            return

        venv_path = os.path.join(current_dir, venv_name)

        # Check if already exists
        if os.path.exists(venv_path):
            print(f"⚠️  Virtual environment '{venv_name}' already exists.")
            overwrite = input("Delete and recreate? (y/n): ").lower()
            if overwrite != 'y':
                print("❌ Operation cancelled.")
                return
            shutil.rmtree(venv_path, ignore_errors=True)

        print(f"\n🚀 Creating virtual environment '{venv_name}'...")

        # Use sys.executable to ensure using current Python
        success, output = self._run_command([sys.executable, "-m", "venv", venv_name])

        if success:
            print(f"✅ Virtual environment created at: {venv_path}")
            
            # Show activation commands
            print("\n🔧 Activation commands:")
            if os.name == 'nt':  # Windows
                print(f"   {venv_name}\\Scripts\\activate")
            else:  # Unix/Linux/Mac
                print(f"   source {venv_name}/bin/activate")
            
            # Offer to install requirements if exists
            req_file = os.path.join(current_dir, "requirements.txt")
            if os.path.exists(req_file):
                install_req = input(f"\n📦 Install from requirements.txt? (y/n): ").lower()
                if install_req == 'y':
                    self._install_requirements(venv_path, req_file)
        else:
            print(f"❌ Failed to create virtual environment: {output}")

    def _delete_venv(self) -> None:
        """Delete a virtual environment."""
        Utils.clear_screen()
        Utils.print_header("DELETE VIRTUAL ENVIRONMENT")

        current_dir = os.getcwd()
        print(f"📂 Current directory: {current_dir}")

        # Look for common venv names
        common_venvs = ['.venv', 'venv', 'env']
        found_venvs = []

        for venv_name in common_venvs:
            venv_path = os.path.join(current_dir, venv_name)
            if os.path.exists(venv_path):
                found_venvs.append((venv_name, venv_path))

        if not found_venvs:
            print("\nℹ️  No standard virtual environments found in current directory.")
            custom_name = input("Enter virtual environment name to delete: ").strip()
            if custom_name:
                custom_path = os.path.join(current_dir, custom_name)
                if os.path.exists(custom_path):
                    found_venvs.append((custom_name, custom_path))
                else:
                    print(f"❌ Virtual environment '{custom_name}' not found.")
                    return
            else:
                print("❌ No virtual environment specified.")
                return

        print("\n📁 Found virtual environments:")
        for i, (name, path) in enumerate(found_venvs, 1):
            size = self._get_folder_size(path)
            print(f"   {i}. {name} ({self._format_size(size)})")

        if len(found_venvs) > 1:
            choice = input(f"\nSelect environment to delete (1-{len(found_venvs)}): ").strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(found_venvs):
                    venv_name, venv_path = found_venvs[idx]
                else:
                    print("❌ Invalid selection.")
                    return
            else:
                print("❌ Invalid input.")
                return
        else:
            venv_name, venv_path = found_venvs[0]

        print(f"\n⚠️  WARNING: This will permanently delete '{venv_name}'")
        print(f"📍 Path: {venv_path}")

        confirm = input(f"\nAre you sure you want to delete '{venv_name}'? (y/N): ").lower()
        if confirm != 'y':
            print("❌ Operation cancelled.")
            return

        try:
            shutil.rmtree(venv_path, ignore_errors=True)
            print(f"✅ Virtual environment '{venv_name}' deleted successfully.")
        except Exception as e:
            print(f"❌ Failed to delete: {e}")

    def _create_env_file(self) -> None:
        """Create a .env file with template."""
        Utils.clear_screen()
        Utils.print_header("CREATE .ENV FILE")

        current_dir = os.getcwd()
        env_path = os.path.join(current_dir, ".env")

        if os.path.exists(env_path):
            print("⚠️  .env file already exists.")
            overwrite = input("Overwrite? (y/n): ").lower()
            if overwrite != 'y':
                print("❌ Operation cancelled.")
                return

        print("\n📝 Creating .env file with common environment variables...")
        print("   (You can edit these values after creation)")

        env_template = """# Environment Variables
    Add your sensitive data here - never commit to version control
    Database Configuration
    DB_NAME=your_database_name
    DB_USER=your_username
    DB_PASSWORD=your_password
    DB_HOST=localhost
    DB_PORT=5432

    Django Settings
    DJANGO_SECRET_KEY=your-secret-key-here-change-this-in-production
    DJANGO_DEBUG=True
    DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

    Email Configuration
    EMAIL_HOST=smtp.gmail.com
    EMAIL_PORT=587
    EMAIL_USE_TLS=True
    EMAIL_HOST_USER=your-email@gmail.com
    EMAIL_HOST_PASSWORD=your-app-specific-password

    API Keys
    API_KEY=your_api_key_here
    SECRET_API_KEY=your_secret_api_key_here

    Application Settings
    LOG_LEVEL=INFO
    ENVIRONMENT=development
    """
        try:
            with open(env_path, 'w', encoding='utf-8') as f:
                f.write(env_template)
            
            print(f"✅ .env file created at: {env_path}")
            print(f"📏 File size: {os.path.getsize(env_path)} bytes")
            
            # Show security warning
            print("\n⚠️  SECURITY REMINDER:")
            print("   • Add .env to .gitignore")
            print("   • Never commit .env to version control")
            print("   • Use different .env files for different environments")
            
            # Show preview
            preview = input("\nShow file preview? (y/n): ").lower()
            if preview == 'y':
                print("\n📄 .env Preview:")
                print("-" * 40)
                with open(env_path, 'r', encoding='utf-8') as f:
                    print(f.read())
                print("-" * 40)
                
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")

    def _delete_env_file(self) -> None:
        """Delete .env file."""
        Utils.clear_screen()
        Utils.print_header("DELETE .ENV FILE")

        current_dir = os.getcwd()
        env_path = os.path.join(current_dir, ".env")

        if not os.path.exists(env_path):
            print("❌ .env file not found in current directory.")
            return

        file_size = os.path.getsize(env_path)
        print(f"📄 File: {env_path}")
        print(f"📏 Size: {self._format_size(file_size)}")
        
        # Show preview
        preview = input("\nShow file preview? (y/n): ").lower()
        if preview == 'y':
            try:
                with open(env_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print("\n📄 File Content:")
                    print("-" * 40)
                    print(content[:500])  # Show first 500 chars
                    if len(content) > 500:
                        print("... (truncated)")
                    print("-" * 40)
            except Exception:
                print("⚠️  Could not read file content.")

        confirm = input(f"\n⚠️  Delete .env file? (y/N): ").lower()
        if confirm != 'y':
            print("❌ Operation cancelled.")
            return

        try:
            os.remove(env_path)
            print("✅ .env file deleted successfully.")
        except Exception as e:
            print(f"❌ Failed to delete: {e}")

    def _list_env_vars(self) -> None:
        """List environment variables."""
        Utils.clear_screen()
        Utils.print_header("ENVIRONMENT VARIABLES")

        print("🌍 System Environment Variables:")
        print("-" * 50)
        
        # Common environment variables to show
        common_vars = [
            'PATH', 'PYTHONPATH', 'VIRTUAL_ENV', 'HOME', 'USER',
            'LANG', 'PYTHON_VERSION', 'PWD', 'SHELL'
        ]
        
        env_vars = dict(os.environ)
        
        print("\n🔧 Common Variables:")
        for var in common_vars:
            if var in env_vars:
                value = env_vars[var]
                # Truncate long values
                if len(value) > 100:
                    value = value[:100] + "..."
                print(f"   {var}: {value}")
        
        print("\n📊 All Variables (alphabetical):")
        print("-" * 50)
        
        for key in sorted(env_vars.keys()):
            if key not in common_vars:  # Already shown
                value = env_vars[key]
                if len(value) > 50:
                    value = value[:50] + "..."
                print(f"   {key}: {value}")
        
        print(f"\n📈 Total variables: {len(env_vars)}")

    def _check_python_env(self) -> None:
        """Check current Python environment."""
        Utils.clear_screen()
        Utils.print_header("PYTHON ENVIRONMENT CHECK")

        print("🐍 Python Information:")
        print(f"   Version: {sys.version}")
        print(f"   Executable: {sys.executable}")
        print(f"   Platform: {sys.platform}")
        print(f"   Prefix: {sys.prefix}")

        # Check if in virtual environment
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            print("   ✅ Running in virtual environment")
            if 'VIRTUAL_ENV' in os.environ:
                print(f"   Virtual env path: {os.environ['VIRTUAL_ENV']}")
        else:
            print("   ℹ️  Running in system Python")

        # Check pip version
        print("\n📦 Package Manager:")
        success, output = self._run_command([sys.executable, "-m", "pip", "--version"])
        if success:
            pip_info = output.split('\n')[0] if output else "Unknown"
            print(f"   {pip_info}")
        else:
            print("   ❌ pip not available")

        # List installed packages (top 10)
        print("\n📋 Top installed packages:")
        success, output = self._run_command([sys.executable, "-m", "pip", "list", "--format=freeze"])
        if success and output:
            packages = output.strip().split('\n')
            for pkg in packages[:10]:  # Show first 10
                print(f"   • {pkg}")
            if len(packages) > 10:
                print(f"   ... and {len(packages) - 10} more")
        else:
            print("   ℹ️  No packages found or pip error")

    def _install_requirements(self, venv_path: str, req_file: str) -> None:
        """Install requirements in virtual environment.
        
        Args:
            venv_path: Path to virtual environment.
            req_file: Path to requirements.txt.
        """
        print(f"\n📦 Installing packages from {req_file}...")
        
        # Determine pip path based on OS
        if os.name == 'nt':  # Windows
            pip_path = os.path.join(venv_path, "Scripts", "pip")
        else:  # Unix/Linux/Mac
            pip_path = os.path.join(venv_path, "bin", "pip")
        
        success, output = self._run_command([pip_path, "install", "-r", req_file])
        
        if success:
            print("✅ Requirements installed successfully!")
            if output:
                # Show last few lines of output
                lines = output.strip().split('\n')
                if len(lines) > 5:
                    print("\n".join(lines[-5:]))
        else:
            print(f"❌ Failed to install requirements: {output}")

    def _get_folder_size(self, folder_path: str) -> int:
        """Calculate folder size in bytes.
        
        Args:
            folder_path: Path to folder.
            
        Returns:
            Size in bytes.
        """
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.exists(filepath):
                    total_size += os.path.getsize(filepath)
        return total_size

    @staticmethod
    def _format_size(size_bytes: int) -> str:
        """Format size in human readable format.
        
        Args:
            size_bytes: Size in bytes.
            
        Returns:
            Formatted size string.
        """
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    def _run_command(self, cmd: list, shell: bool = False) -> Tuple[bool, str]:
        """Run a shell command.
        
        Args:
            cmd: Command list.
            shell: Whether to use shell.
            
        Returns:
            (success, output)
        """
        try:
            result = subprocess.run(
                cmd,
                shell=shell,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            
            if result.returncode == 0:
                return True, result.stdout.strip()
            else:
                error_msg = result.stderr.strip() or result.stdout.strip() or "Unknown error"
                return False, error_msg
                
        except FileNotFoundError:
            return False, f"Command not found: {' '.join(cmd)}"
        except Exception as e:
            return False, str(e)
        