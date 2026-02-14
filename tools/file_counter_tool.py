"""Tool to count files and folders by type."""

import os
from collections import defaultdict
from tools.base_tool import BaseTool
from util.utils import Utils

class FileCounterTool(BaseTool):
    """Count files and folders by type."""

    name = "📊 File Statistics"
    description = "Count files and folders by type"

    def run(self) -> None:
        """Execute the file counting process."""
        Utils.clear_screen()
        Utils.print_header("FILE STATISTICS")

        project_path = Utils.get_project_path()

        file_stats = defaultdict(int)
        total_files = 0
        total_dirs = 0

        for root, dirs, files in os.walk(project_path):
            total_dirs += len(dirs)
            total_files += len(files)
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                file_stats[ext] += 1

        print(f"\n📁 Project: {os.path.basename(project_path)}")
        print(f"📍 Path: {project_path}")
        print("\n📈 Statistics:")
        print(f"   • Total folders: {total_dirs}")
        print(f"   • Total files: {total_files}")

        print("\n📄 Files by extension:")
        for ext, count in sorted(file_stats.items(), key=lambda x: x[1], reverse=True):
            ext_display = ext if ext else "[no extension]"
            print(f"   • {ext_display}: {count}")

        input("\nPress Enter to continue...")
        