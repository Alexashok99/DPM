"""Tool to clean pycache directories."""

import os
import shutil
from tools.base_tool import BaseTool
from util.utils import Utils

class CleanPycacheTool(BaseTool):
    """Remove all pycache folders recursively."""

    name = "🧹 Clean __pycache__"
    description = "Remove all __pycache__ folders recursively"

    def run(self) -> None:
        """Execute the cleaning process."""
        Utils.clear_screen()
        Utils.print_header("CLEAN PYTHON CACHE")

        start_path = os.getcwd()
        print(f"🔍 Cleaning in: {start_path}")

        confirm = input("\n⚠️  Are you sure you want to delete all __pycache__ folders? (y/n): ").lower()
        if confirm != "y":
            print("❌ Operation cancelled.")
            return

        deleted = 0
        total_size = 0

        for root, dirs, _ in os.walk(start_path, topdown=True):
            if "__pycache__" in dirs:
                path = os.path.join(root, "__pycache__")
                try:
                    folder_size = self._calculate_folder_size(path)
                    shutil.rmtree(path, ignore_errors=True)
                    dirs.remove("__pycache__")  # Prevent further walking
                    deleted += 1
                    total_size += folder_size

                    print(f"✅ Deleted: {os.path.relpath(path, start_path)}")
                    if folder_size > 0:
                        print(f"   Size: {self._format_size(folder_size)}")
                except Exception as e:
                    print(f"❌ Failed to delete {path}: {e}")

        if deleted > 0:
            print(f"\n🎯 Summary:")
            print(f"   • Folders deleted: {deleted}")
            print(f"   • Space freed: {self._format_size(total_size)}")
        else:
            print("\nℹ️  No __pycache__ folders found.")
        input("\nPress Enter to continue...")

    @staticmethod
    def _calculate_folder_size(folder_path: str) -> int:
        """Calculate total size of a folder in bytes.

        Args:
            folder_path (str): Path to folder.

        Returns:
            int: Total size in bytes.
        """
        total_size = 0
        for dirpath, _, filenames in os.walk(folder_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                total_size += os.path.getsize(filepath)
        return total_size

    @staticmethod
    def _format_size(size_bytes: int) -> str:
        """Format file size in human readable format.

        Args:
            size_bytes (int): Size in bytes.

        Returns:
            str: Formatted size string.
        """
        for unit in ["B", "KB", "MB", "GB"]:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"