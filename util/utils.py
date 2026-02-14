"""Utility functions for the application."""

import os
import datetime
from configs_file.config import Config

class Utils:
    """Utility functions for the application."""

    @staticmethod
    def clear_screen() -> None:
        """Clear terminal screen."""
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def print_header(title: str) -> None:
        """Print formatted header.

        Args:
            title (str): Header title.
        """
        print("\n" + "=" * 50)
        print(f"{title:^50}")
        print("=" * 50)

    @staticmethod
    def get_project_path() -> str:
        """Get project path from user or use current directory.

        Returns:
            str: Valid project path.
        """
        default_path = os.getcwd()
        print(f"\nCurrent directory: {default_path}")

        choice = input("Use current directory? (y/n): ").strip().lower()
        if choice in ("y", ""):
            return default_path

        while True:
            custom_path = input("Enter project path: ").strip()
            if os.path.isdir(custom_path):
                return custom_path
            print(f"❌ Error: Path '{custom_path}' does not exist or is not a directory.")

    @staticmethod
    def show_ignore_lists(config: Config) -> None:
        """Display current ignore lists.

        Args:
            config (Config): Configuration instance.
        """
        print("\n📁 Current Ignore Directories:")
        print("-" * 30)
        if config.ignore_dirs:
            for dir_name in sorted(config.ignore_dirs):
                print(f"  • {dir_name}")
        else:
            print("  (Empty)")

        print("\n📄 Current Ignore Files:")
        print("-" * 30)
        if config.ignore_files:
            for file_name in sorted(config.ignore_files):
                print(f"  • {file_name}")
        else:
            print("  (Empty)")

    @staticmethod
    def get_timestamp() -> str:
        """Get current timestamp in readable format."""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")