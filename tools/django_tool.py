"""Tool for Django project and app management."""

import os
import subprocess
import sys
from typing import Tuple, Optional
from tools.base_tool import BaseTool
from util.utils import Utils

class DjangoTool(BaseTool):
    """Manage Django projects and apps."""

    name = "🚀 Django Manager"
    description = "Create Django project, check, create app, migrate, runserver"

    def run(self) -> None:
        """Display Django management menu."""
        while True:
            Utils.clear_screen()
            Utils.print_header("DJANGO PROJECT MANAGER")

            print("\n1. Create Django Project")
            print("2. Check Django Installation")
            print("3. Create Django App")
            print("4. Make Migrations")
            print("5. Apply Migrations")
            print("6. Run Development Server")
            print("7. Back to Main Menu")

            choice = input("\nSelect option (1-7): ").strip()

            if choice == "1":
                self._create_project()
            elif choice == "2":
                self._check_django()
            elif choice == "3":
                self._create_app()
            elif choice == "4":
                self._make_migrations()
            elif choice == "5":
                self._migrate()
            elif choice == "6":
                self._run_server()
            elif choice == "7":
                break
            else:
                print("❌ Invalid option")

            if choice != "7":
                input("\nPress Enter to continue...")

    def _create_project(self) -> None:
        """Create a new Django project."""
        Utils.clear_screen()
        Utils.print_header("CREATE DJANGO PROJECT")

        print("\nℹ️  This will create a new Django project in current directory.")
        print("   Make sure you're in the right directory first.")

        current_dir = os.getcwd()
        print(f"\n📂 Current directory: {current_dir}")

        confirm = input("\nDo you want to continue? (y/n): ").lower()
        if confirm != "y":
            print("❌ Operation cancelled.")
            return

        project_name = input("Enter project name: ").strip()
        if not project_name:
            print("❌ Project name cannot be empty.")
            return

        print(f"\n🚀 Creating Django project '{project_name}'...")
        success, output = self._run_command(["django-admin", "startproject", project_name])

        if success:
            print(f"✅ Django project '{project_name}' created successfully!")
            print(f"📁 Location: {os.path.join(current_dir, project_name)}")
            print("\n📋 Next steps:")
            print(f"   1. cd {project_name}")
            print("   2. python manage.py migrate")
            print("   3. python manage.py runserver")
        else:
            print(f"❌ Failed to create project: {output}")

    def _check_django(self) -> None:
        """Check if Django is installed and show version."""
        Utils.clear_screen()
        Utils.print_header("CHECK DJANGO INSTALLATION")

        print("🔍 Checking Django installation...")

        # Try python -m django --version
        success, output = self._run_command([sys.executable, "-m", "django", "--version"])
        
        if success:
            version = output.strip()
            print(f"✅ Django {version} is installed and working.")
            
            # Try import in Python
            try:
                import django
                print(f"📦 Django module path: {django.__file__}")
            except ImportError as e:
                print(f"⚠️  Django import issue: {e}")
        else:
            print("❌ Django is not installed or not in PATH.")
            print("\n💡 Installation commands:")
            print("   pip install django")
            print("   or")
            print("   pip3 install django")

        # Check for pip packages
        print("\n🔍 Checking related packages...")
        self._run_command([sys.executable, "-m", "pip", "list", "|", "findstr", "Django"], shell=True)

    def _create_app(self) -> None:
        """Create a new Django app within a project."""
        Utils.clear_screen()
        Utils.print_header("CREATE DJANGO APP")

        project_dir = self._find_django_project()
        if not project_dir:
            print("❌ Not in a Django project directory.")
            print("   Navigate to your Django project root and try again.")
            return

        print(f"📁 Django project found: {os.path.basename(project_dir)}")
        
        app_name = input("\nEnter app name: ").strip()
        if not app_name:
            print("❌ App name cannot be empty.")
            return

        print(f"\n🚀 Creating app '{app_name}'...")
        
        # Change to project directory
        original_dir = os.getcwd()
        os.chdir(project_dir)
        
        success, output = self._run_command(["python", "manage.py", "startapp", app_name])
        
        # Change back
        os.chdir(original_dir)

        if success:
            print(f"✅ Django app '{app_name}' created successfully!")
            app_path = os.path.join(project_dir, app_name)
            print(f"📁 Location: {app_path}")
            
            # Show next steps
            print("\n📋 Next steps:")
            print(f"   1. Add '{app_name}' to INSTALLED_APPS in settings.py")
            print(f"   2. Create models in {app_name}/models.py")
            print(f"   3. python manage.py makemigrations {app_name}")
            print(f"   4. python manage.py migrate")
        else:
            print(f"❌ Failed to create app: {output}")

    def _make_migrations(self) -> None:
        """Create database migrations."""
        Utils.clear_screen()
        Utils.print_header("MAKE MIGRATIONS")

        project_dir = self._find_django_project()
        if not project_dir:
            print("❌ Not in a Django project directory.")
            return

        print(f"📁 Django project: {os.path.basename(project_dir)}")
        
        app_name = input("\nEnter app name (leave empty for all apps): ").strip()
        
        # Change to project directory
        original_dir = os.getcwd()
        os.chdir(project_dir)
        
        if app_name:
            print(f"\n🔨 Making migrations for '{app_name}'...")
            success, output = self._run_command(["python", "manage.py", "makemigrations", app_name])
        else:
            print("\n🔨 Making migrations for all apps...")
            success, output = self._run_command(["python", "manage.py", "makemigrations"])
        
        # Change back
        os.chdir(original_dir)

        if success:
            print("✅ Migrations created successfully!")
            if output:
                print(f"\n📄 Output: {output}")
        else:
            print(f"❌ Failed to create migrations: {output}")

    def _migrate(self) -> None:
        """Apply database migrations."""
        Utils.clear_screen()
        Utils.print_header("APPLY MIGRATIONS")

        project_dir = self._find_django_project()
        if not project_dir:
            print("❌ Not in a Django project directory.")
            return

        print(f"📁 Django project: {os.path.basename(project_dir)}")
        
        confirm = input("\nApply all migrations? (y/n): ").lower()
        if confirm != "y":
            print("❌ Operation cancelled.")
            return

        # Change to project directory
        original_dir = os.getcwd()
        os.chdir(project_dir)
        
        print("\n🔄 Applying migrations...")
        success, output = self._run_command(["python", "manage.py", "migrate"])
        
        # Change back
        os.chdir(original_dir)

        if success:
            print("✅ Migrations applied successfully!")
            if output:
                # Show only last few lines
                lines = output.strip().split('\n')
                if len(lines) > 10:
                    print("\n".join(lines[-10:]))
                else:
                    print(output)
        else:
            print(f"❌ Failed to apply migrations: {output}")

    def _run_server(self) -> None:
        """Run Django development server."""
        Utils.clear_screen()
        Utils.print_header("RUN DEVELOPMENT SERVER")

        project_dir = self._find_django_project()
        if not project_dir:
            print("❌ Not in a Django project directory.")
            return

        print(f"📁 Django project: {os.path.basename(project_dir)}")
        
        port = input("\nEnter port number [8000]: ").strip()
        if not port:
            port = "8000"
        
        if not port.isdigit():
            print("❌ Port must be a number.")
            return

        print(f"\n🌐 Starting development server on port {port}...")
        print("   Press Ctrl+C to stop the server")
        print("-" * 50)

        # Change to project directory
        original_dir = os.getcwd()
        os.chdir(project_dir)
        
        try:
            # Run server in foreground
            subprocess.run([sys.executable, "manage.py", "runserver", f"127.0.0.1:{port}"])
        except KeyboardInterrupt:
            print("\n\n🛑 Server stopped by user.")
        except Exception as e:
            print(f"❌ Error running server: {e}")
        finally:
            # Change back
            os.chdir(original_dir)

    def _find_django_project(self) -> Optional[str]:
        """Find Django project directory by looking for manage.py.

        Returns:
            Optional[str]: Path to Django project directory or None.
        """
        current_dir = os.getcwd()
        
        # Check current directory and parent directories
        check_dir = current_dir
        for _ in range(5):  # Check up to 5 levels up
            manage_py = os.path.join(check_dir, "manage.py")
            if os.path.exists(manage_py):
                return check_dir
            
            # Move up one directory
            parent = os.path.dirname(check_dir)
            if parent == check_dir:  # Reached root
                break
            check_dir = parent
        
        return None

    def _run_command(self, cmd: list, shell: bool = False) -> Tuple[bool, str]:
        """Run a shell command and return success status and output.

        Args:
            cmd (list): Command list.
            shell (bool): Whether to use shell.

        Returns:
            Tuple[bool, str]: (success, output)
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
        
        