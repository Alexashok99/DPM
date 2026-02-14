"""Tool for file and folder operations."""

import os
import shutil
import stat
import time
from pathlib import Path
from typing import List, Tuple, Optional
from tools.base_tool import BaseTool
from util.utils import Utils


class FileOperationsTool(BaseTool):
    """Perform file and folder operations."""

    name = "📁 File Operations"
    description = "List, copy, move, delete files and folders"

    def run(self) -> None:
        """Display file operations menu."""
        while True:
            Utils.clear_screen()
            Utils.print_header("FILE OPERATIONS")

            print("\n1. List all project files (for copy path)")
            print("2. Copy file/folder")
            print("3. Move file/folder")
            print("4. Delete file/folder")
            print("5. File information")
            print("6. Create new folder")
            print("7. Create new file")
            print("8. Back to Main Menu")

            choice = input("\nSelect option (1-8): ").strip()

            if choice == "1":
                self._list_project_files()
            elif choice == "2":
                self._copy_file_folder()
            elif choice == "3":
                self._move_file_folder()
            elif choice == "4":
                self._delete_file_folder()
            elif choice == "5":
                self._file_info()
            elif choice == "6":
                self._create_folder()
            elif choice == "7":
                self._create_file()
            elif choice == "8":
                break
            else:
                print("❌ Invalid option")

            if choice != "8":
                input("\nPress Enter to continue...")

    def _list_project_files(self) -> None:
        """List all files in project with copyable paths."""
        Utils.clear_screen()
        Utils.print_header("LIST PROJECT FILES")

        current_dir = os.getcwd()
        print(f"📍 Current directory: {current_dir}")

        print("\n🔍 Scanning files...")

        # Get list of all files
        all_files = []
        total_size = 0

        for root, dirs, files in os.walk(current_dir):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith(".")]

            for file in files:
                if file.startswith("."):
                    continue

                file_path = os.path.join(root, file)
                try:
                    file_size = os.path.getsize(file_path)
                    rel_path = os.path.relpath(file_path, current_dir)

                    all_files.append(
                        {"path": rel_path, "size": file_size, "full_path": file_path}
                    )
                    total_size += file_size
                except (OSError, PermissionError):
                    continue

        if not all_files:
            print("❌ No files found.")
            return

        # Sort files by path
        all_files.sort(key=lambda x: x["path"])

        print(f"\n📊 Found {len(all_files)} files ({self._format_size(total_size)})")

        # Display options
        print("\n📋 Display options:")
        print("1. Show all files with details")
        print("2. Show only file paths (for copying)")
        print("3. Search for specific files")
        print("4. Export list to file")

        display_choice = input("\nSelect option (1-4): ").strip()

        if display_choice == "1":
            self._show_files_with_details(all_files)
        elif display_choice == "2":
            self._show_file_paths_only(all_files)
        elif display_choice == "3":
            self._search_files(all_files)
        elif display_choice == "4":
            self._export_file_list(all_files, current_dir)
        else:
            self._show_files_with_details(all_files)

    def _show_files_with_details(self, files: List[dict]) -> None:
        """Show files with detailed information.

        Args:
            files: List of file dictionaries.
        """
        print("\n📄 Files with details:")
        print("-" * 80)
        print(f"{'No.':<4} {'Size':<10} {'Path'}")
        print("-" * 80)

        for idx, file_info in enumerate(files, 1):
            if idx <= 100:  # Show first 100 files
                size_str = self._format_size(file_info["size"])
                print(f"{idx:<4} {size_str:<10} {file_info['path']}")
            else:
                print(f"... and {len(files) - 100} more files")
                break

        print("-" * 80)

        if len(files) > 0:
            print("\n📋 Copy options:")
            print("   Enter file number to copy path to clipboard")
            print("   Enter 'a' to copy all paths")
            print("   Enter 'q' to quit")

            while True:
                choice = input("\nSelect file number (or q to quit): ").strip().lower()

                if choice == "q":
                    break
                elif choice == "a":
                    self._copy_all_paths(files)
                    break
                elif choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(files):
                        self._copy_to_clipboard(files[idx]["path"])
                        print(f"✅ Copied: {files[idx]['path']}")
                    else:
                        print("❌ Invalid file number")
                else:
                    print("❌ Invalid input")

    def _show_file_paths_only(self, files: List[dict]) -> None:
        """Show only file paths for easy copying.

        Args:
            files: List of file dictionaries.
        """
        print("\n📄 File paths only:")
        print("-" * 60)

        for idx, file_info in enumerate(files, 1):
            if idx <= 50:  # Show first 50 files
                print(f"{file_info['path']}")
            else:
                print(f"... and {len(files) - 50} more files")
                break

        print("-" * 60)

        if len(files) > 0:
            copy_all = input("\n📋 Copy all paths to file? (y/n): ").lower()
            if copy_all == "y":
                self._copy_all_paths(files)

    def _search_files(self, files: List[dict]) -> None:
        """Search for files by name or extension.

        Args:
            files: List of file dictionaries.
        """
        print("\n🔍 Search files:")
        print("1. Search by filename")
        print("2. Search by extension")
        print("3. Search by size range")

        search_choice = input("\nSelect search type (1-3): ").strip()

        if search_choice == "1":
            search_term = input("Enter filename or part of filename: ").strip().lower()
            results = [f for f in files if search_term in f["path"].lower()]
            title = f"Files containing '{search_term}'"
        elif search_choice == "2":
            extension = input("Enter extension (e.g., .py, .txt): ").strip().lower()
            if not extension.startswith("."):
                extension = "." + extension
            results = [f for f in files if f["path"].lower().endswith(extension)]
            title = f"Files with extension '{extension}'"
        elif search_choice == "3":
            try:
                min_size = input("Minimum size in KB (press Enter for 0): ").strip()
                max_size = input(
                    "Maximum size in KB (press Enter for no limit): "
                ).strip()

                min_bytes = int(float(min_size or 0) * 1024)
                max_bytes = (
                    int(float(max_size or float("inf")) * 1024)
                    if max_size
                    else float("inf")
                )

                results = [f for f in files if min_bytes <= f["size"] <= max_bytes]
                title = f"Files between {min_size or 0}KB and {max_size or '∞'}KB"
            except ValueError:
                print("❌ Invalid size input")
                return
        else:
            print("❌ Invalid choice")
            return

        if not results:
            print(f"\n❌ No files found.")
            return

        print(f"\n📊 {title}: {len(results)} files found")
        self._show_files_with_details(results)

    def _export_file_list(self, files: List[dict], current_dir: str) -> None:
        """Export file list to a text file.

        Args:
            files: List of file dictionaries.
            current_dir: Current working directory.
        """
        filename = input("\nEnter output filename [file_list.txt]: ").strip()
        if not filename:
            filename = "file_list.txt"

        print("\n📋 Export options:")
        print("1. Simple list (paths only)")
        print("2. Detailed list (with sizes)")
        print("3. CSV format")

        format_choice = input("\nSelect format (1-3): ").strip()

        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"File list for: {current_dir}\n")
                f.write(f"Generated on: {self._get_current_timestamp()}\n")
                f.write(f"Total files: {len(files)}\n")
                f.write(
                    f"Total size: {self._format_size(sum(f['size'] for f in files))}\n"
                )
                f.write("=" * 80 + "\n\n")

                if format_choice == "1":
                    for file_info in files:
                        f.write(f"{file_info['path']}\n")
                elif format_choice == "2":
                    for file_info in files:
                        size_str = self._format_size(file_info["size"])
                        f.write(f"{size_str:<12} {file_info['path']}\n")
                elif format_choice == "3":
                    f.write("Path,Size(bytes),Size(human)\n")
                    for file_info in files:
                        size_str = self._format_size(file_info["size"])
                        # Escape quotes in path
                        path_escaped = file_info["path"].replace('"', '""')
                        f.write(f'"{path_escaped}",{file_info["size"]},"{size_str}"\n')
                else:
                    for file_info in files:
                        f.write(f"{file_info['path']}\n")

            print(f"✅ File list exported to: {os.path.abspath(filename)}")
            print(f"📏 File size: {self._format_size(os.path.getsize(filename))}")

        except Exception as e:
            print(f"❌ Failed to export file list: {e}")

    def _copy_all_paths(self, files: List[dict]) -> None:
        """Copy all file paths to clipboard or file.

        Args:
            files: List of file dictionaries.
        """
        print("\n📋 Copy all paths:")
        print("1. Copy to clipboard (if supported)")
        print("2. Save to text file")
        print("3. Show in console")

        copy_choice = input("\nSelect option (1-3): ").strip()

        all_paths = "\n".join(f["path"] for f in files)

        if copy_choice == "1":
            success = self._copy_to_clipboard(all_paths)
            if success:
                print(f"✅ Copied {len(files)} paths to clipboard")
            else:
                print("⚠️  Clipboard not available, showing paths instead:")
                print(all_paths[:500] + ("..." if len(all_paths) > 500 else ""))
        elif copy_choice == "2":
            filename = input("Enter filename [paths.txt]: ").strip()
            if not filename:
                filename = "paths.txt"

            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(all_paths)
                print(f"✅ Saved {len(files)} paths to {filename}")
            except Exception as e:
                print(f"❌ Failed to save file: {e}")
        elif copy_choice == "3":
            print("\n📄 All file paths:")
            print("-" * 60)
            print(all_paths[:1000])  # Limit output
            if len(all_paths) > 1000:
                print(f"... and {len(all_paths) - 1000} more characters")
            print("-" * 60)

    def _copy_file_folder(self) -> None:
        """Copy a file or folder."""
        Utils.clear_screen()
        Utils.print_header("COPY FILE/FOLDER")

        current_dir = os.getcwd()
        print(f"📍 Current directory: {current_dir}")

        source = input("\nEnter source file/folder path: ").strip()
        if not source:
            print("❌ Source path cannot be empty.")
            return

        # Handle relative paths
        if not os.path.isabs(source):
            source = os.path.join(current_dir, source)

        if not os.path.exists(source):
            print(f"❌ Source not found: {source}")
            return

        # Suggest destination
        dest_dir = (
            os.path.dirname(source)
            if os.path.isfile(source)
            else os.path.dirname(os.path.dirname(source))
        )
        dest_suggestion = os.path.join(dest_dir, f"copy_of_{os.path.basename(source)}")

        dest = input(f"Enter destination path [{dest_suggestion}]: ").strip()
        if not dest:
            dest = dest_suggestion

        # Handle relative destination
        if not os.path.isabs(dest):
            dest = os.path.join(current_dir, dest)

        # Check if destination exists
        if os.path.exists(dest):
            print(f"⚠️  Destination already exists: {dest}")
            action = input("Overwrite, Rename, or Cancel? (o/r/c): ").lower()

            if action == "c":
                print("❌ Operation cancelled.")
                return
            elif action == "r":
                base, ext = os.path.splitext(dest)
                counter = 1
                while os.path.exists(f"{base}_{counter}{ext}"):
                    counter += 1
                dest = f"{base}_{counter}{ext}"
                print(f"📝 New destination: {dest}")

        # Confirm copy
        source_size = self._get_path_size(source)
        print(f"\n📋 Copy details:")
        print(f"   Source: {source}")
        print(f"   Destination: {dest}")
        print(f"   Size: {self._format_size(source_size)}")
        print(f"   Type: {'File' if os.path.isfile(source) else 'Folder'}")

        confirm = input("\n📝 Confirm copy? (y/n): ").lower()
        if confirm != "y":
            print("❌ Operation cancelled.")
            return

        # Perform copy
        try:
            if os.path.isfile(source):
                shutil.copy2(source, dest)  # copy2 preserves metadata
                print(f"✅ File copied successfully!")
            else:
                shutil.copytree(source, dest, dirs_exist_ok=True)
                print(f"✅ Folder copied successfully!")

            # Verify
            if os.path.exists(dest):
                dest_size = self._get_path_size(dest)
                print(
                    f"📏 Verification: Source {self._format_size(source_size)} -> Destination {self._format_size(dest_size)}"
                )

        except Exception as e:
            print(f"❌ Copy failed: {e}")

    def _move_file_folder(self) -> None:
        """Move a file or folder."""
        Utils.clear_screen()
        Utils.print_header("MOVE FILE/FOLDER")

        current_dir = os.getcwd()
        print(f"📍 Current directory: {current_dir}")

        source = input("\nEnter source file/folder path: ").strip()
        if not source:
            print("❌ Source path cannot be empty.")
            return

        # Handle relative paths
        if not os.path.isabs(source):
            source = os.path.join(current_dir, source)

        if not os.path.exists(source):
            print(f"❌ Source not found: {source}")
            return

        # Get destination directory
        dest_dir = input("Enter destination directory: ").strip()
        if not dest_dir:
            print("❌ Destination cannot be empty.")
            return

        # Handle relative destination
        if not os.path.isabs(dest_dir):
            dest_dir = os.path.join(current_dir, dest_dir)

        # Create destination directory if it doesn't exist
        if not os.path.exists(dest_dir):
            create = input(
                f"Destination directory doesn't exist. Create it? (y/n): "
            ).lower()
            if create == "y":
                try:
                    os.makedirs(dest_dir, exist_ok=True)
                    print(f"✅ Created directory: {dest_dir}")
                except Exception as e:
                    print(f"❌ Failed to create directory: {e}")
                    return
            else:
                print("❌ Operation cancelled.")
                return

        # Build full destination path
        dest = os.path.join(dest_dir, os.path.basename(source))

        # Check if destination exists
        if os.path.exists(dest):
            print(f"⚠️  Destination already exists: {dest}")
            action = input("Overwrite, Rename, or Cancel? (o/r/c): ").lower()

            if action == "c":
                print("❌ Operation cancelled.")
                return
            elif action == "r":
                base, ext = os.path.splitext(dest)
                counter = 1
                while os.path.exists(f"{base}_{counter}{ext}"):
                    counter += 1
                dest = f"{base}_{counter}{ext}"
                print(f"📝 New destination: {dest}")

        # Confirm move
        source_size = self._get_path_size(source)
        print(f"\n📋 Move details:")
        print(f"   Source: {source}")
        print(f"   Destination: {dest}")
        print(f"   Size: {self._format_size(source_size)}")
        print(f"   Type: {'File' if os.path.isfile(source) else 'Folder'}")

        confirm = input("\n⚠️  Confirm move? (y/n): ").lower()
        if confirm != "y":
            print("❌ Operation cancelled.")
            return

        # Perform move
        try:
            shutil.move(source, dest)
            print(f"✅ Moved successfully!")

            # Verify
            if os.path.exists(dest) and not os.path.exists(source):
                print(f"📏 Verification: File moved from {source} to {dest}")
            else:
                print("⚠️  Warning: Source still exists or destination missing")

        except Exception as e:
            print(f"❌ Move failed: {e}")

    def _delete_file_folder(self) -> None:
        """Delete a file or folder."""
        Utils.clear_screen()
        Utils.print_header("DELETE FILE/FOLDER")

        current_dir = os.getcwd()
        print(f"📍 Current directory: {current_dir}")

        target = input("\nEnter file/folder path to delete: ").strip()
        if not target:
            print("❌ Path cannot be empty.")
            return

        # Handle relative paths
        if not os.path.isabs(target):
            target = os.path.join(current_dir, target)

        if not os.path.exists(target):
            print(f"❌ Path not found: {target}")
            return

        # Get information about the target
        is_file = os.path.isfile(target)
        size = self._get_path_size(target)
        modified = time.ctime(os.path.getmtime(target))

        print(f"\n📋 Target information:")
        print(f"   Path: {target}")
        print(f"   Type: {'File' if is_file else 'Folder'}")
        print(f"   Size: {self._format_size(size)}")
        print(f"   Modified: {modified}")

        if not is_file:
            # Count contents for folders
            try:
                file_count = sum(len(files) for _, _, files in os.walk(target))
                folder_count = sum(len(dirs) for _, dirs, _ in os.walk(target))
                print(f"   Contains: {file_count} files, {folder_count} folders")
            except:
                pass

        # Safety check - prevent deleting important paths
        important_paths = [
            os.path.expanduser("~"),
            "/",
            "C:\\",
            os.getcwd(),
            os.path.dirname(os.getcwd()),
        ]

        if any(target.startswith(important) for important in important_paths):
            print(f"\n⚠️  WARNING: You're about to delete an important path!")
            print(f"   This could cause system instability!")
            confirm = input("Are you ABSOLUTELY sure? (type 'YES' to confirm): ")
            if confirm != "YES":
                print("❌ Operation cancelled.")
                return
        else:
            confirm = input(
                "\n⚠️  Are you sure you want to delete this? (y/n): "
            ).lower()
            if confirm != "y":
                print("❌ Operation cancelled.")
                return

        # Perform deletion
        try:
            if is_file:
                os.remove(target)
                print(f"✅ File deleted: {target}")
            else:
                # For folders, we need to handle permissions
                def remove_readonly(func, path, _):
                    """Remove readonly attribute on Windows."""
                    os.chmod(path, stat.S_IWRITE)
                    func(path)

                shutil.rmtree(target, onerror=remove_readonly)
                print(f"✅ Folder deleted: {target}")

            # Verify
            if not os.path.exists(target):
                print(f"📏 Verification: {target} successfully removed")
            else:
                print("⚠️  Warning: Path still exists after deletion")

        except PermissionError:
            print(f"❌ Permission denied: Cannot delete {target}")
            print("   The file/folder might be in use or you don't have permission.")
        except Exception as e:
            print(f"❌ Deletion failed: {e}")

    def _file_info(self) -> None:
        """Show detailed information about a file or folder."""
        Utils.clear_screen()
        Utils.print_header("FILE INFORMATION")

        current_dir = os.getcwd()
        print(f"📍 Current directory: {current_dir}")

        target = input("\nEnter file/folder path: ").strip()
        if not target:
            print("❌ Path cannot be empty.")
            return

        # Handle relative paths
        if not os.path.isabs(target):
            target = os.path.join(current_dir, target)

        if not os.path.exists(target):
            print(f"❌ Path not found: {target}")
            return

        # Get detailed information
        path_obj = Path(target)

        print(f"\n📋 Basic Information:")
        print(f"   Path: {target}")
        print(f"   Name: {path_obj.name}")
        print(f"   Type: {'File' if path_obj.is_file() else 'Folder'}")
        print(f"   Absolute path: {path_obj.absolute()}")

        if path_obj.is_file():
            print(f"   Extension: {path_obj.suffix}")
            print(f"   Stem (without extension): {path_obj.stem}")

        # Size information
        size = self._get_path_size(target)
        print(f"\n📏 Size Information:")
        print(f"   Size: {self._format_size(size)} ({size:,} bytes)")

        if path_obj.is_dir():
            try:
                # Count files and folders
                file_count = 0
                folder_count = 0
                total_size = 0

                for root, dirs, files in os.walk(target):
                    folder_count += len(dirs)
                    file_count += len(files)
                    for file in files:
                        try:
                            total_size += os.path.getsize(os.path.join(root, file))
                        except:
                            pass

                print(f"   Contains: {file_count} files, {folder_count} folders")
                print(
                    f"   Total size (including subfolders): {self._format_size(total_size)}"
                )
            except:
                pass

        # Time information
        print(f"\n🕒 Time Information:")
        try:
            created = time.ctime(os.path.getctime(target))
            modified = time.ctime(os.path.getmtime(target))
            accessed = time.ctime(os.path.getatime(target))

            print(f"   Created: {created}")
            print(f"   Modified: {modified}")
            print(f"   Accessed: {accessed}")
        except:
            print("   Time information not available")

        # Permission information
        print(f"\n🔒 Permission Information:")
        try:
            stat_info = os.stat(target)

            # Unix-like permissions
            if hasattr(stat_info, "st_mode"):
                mode = stat_info.st_mode
                print(f"   Permissions: {oct(mode)[-3:]}")

                # Human readable
                perms = []
                perms.append("r" if mode & stat.S_IRUSR else "-")
                perms.append("w" if mode & stat.S_IWUSR else "-")
                perms.append("x" if mode & stat.S_IXUSR else "-")
                perms.append("r" if mode & stat.S_IRGRP else "-")
                perms.append("w" if mode & stat.S_IWGRP else "-")
                perms.append("x" if mode & stat.S_IXGRP else "-")
                perms.append("r" if mode & stat.S_IROTH else "-")
                perms.append("w" if mode & stat.S_IWOTH else "-")
                perms.append("x" if mode & stat.S_IXOTH else "-")

                print(f"   Human readable: {''.join(perms)}")

            # Owner information (Unix)
            if hasattr(stat_info, "st_uid"):
                import pwd

                try:
                    owner = pwd.getpwuid(stat_info.st_uid).pw_name
                    print(f"   Owner: {owner} (UID: {stat_info.st_uid})")
                except:
                    pass

            # Group information (Unix)
            if hasattr(stat_info, "st_gid"):
                import grp

                try:
                    group = grp.getgrgid(stat_info.st_gid).gr_name
                    print(f"   Group: {group} (GID: {stat_info.st_gid})")
                except:
                    pass

        except:
            print("   Permission information not available")

        # For Python files, show additional info
        if path_obj.is_file() and path_obj.suffix == ".py":
            print(f"\n🐍 Python File Analysis:")
            try:
                with open(target, "r", encoding="utf-8") as f:
                    content = f.read()
                    lines = content.split("\n")
                    code_lines = [
                        l for l in lines if l.strip() and not l.strip().startswith("#")
                    ]
                    comment_lines = [l for l in lines if l.strip().startswith("#")]
                    blank_lines = [l for l in lines if not l.strip()]

                    print(f"   Total lines: {len(lines)}")
                    print(f"   Code lines: {len(code_lines)}")
                    print(f"   Comment lines: {len(comment_lines)}")
                    print(f"   Blank lines: {len(blank_lines)}")

                    # Check for imports
                    import re

                    imports = re.findall(
                        r"^\s*(import|from)\s+(\w+)", content, re.MULTILINE
                    )
                    if imports:
                        print(f"   Imports: {len(imports)} found")
                        # Show unique imports
                        unique_imports = set()
                        for imp_type, module in imports:
                            unique_imports.add(module)
                        if unique_imports:
                            print(
                                f"   Modules: {', '.join(sorted(unique_imports)[:10])}"
                            )
                            if len(unique_imports) > 10:
                                print(f"     ... and {len(unique_imports) - 10} more")
            except:
                print("   Could not analyze Python file")

    def _create_folder(self) -> None:
        """Create a new folder."""
        Utils.clear_screen()
        Utils.print_header("CREATE NEW FOLDER")

        current_dir = os.getcwd()
        print(f"📍 Current directory: {current_dir}")

        folder_name = input("\nEnter folder name: ").strip()
        if not folder_name:
            print("❌ Folder name cannot be empty.")
            return

        # Handle relative paths
        if "/" in folder_name or "\\" in folder_name:
            # User might be specifying a path
            if not os.path.isabs(folder_name):
                folder_path = os.path.join(current_dir, folder_name)
            else:
                folder_path = folder_name
        else:
            folder_path = os.path.join(current_dir, folder_name)

        # Check if folder already exists
        if os.path.exists(folder_path):
            print(f"⚠️  Folder already exists: {folder_path}")
            choice = input("Open, Delete and recreate, or Cancel? (o/d/c): ").lower()

            if choice == "c":
                print("❌ Operation cancelled.")
                return
            elif choice == "d":
                try:
                    shutil.rmtree(folder_path, ignore_errors=True)
                    print(f"✅ Removed existing folder.")
                except Exception as e:
                    print(f"❌ Failed to remove existing folder: {e}")
                    return
            elif choice == "o":
                print(f"✅ Opening existing folder.")
                # Option to open folder could be added here
                return

        # Create folder
        try:
            os.makedirs(folder_path, exist_ok=True)
            print(f"✅ Folder created: {folder_path}")
            print(f"📍 Full path: {os.path.abspath(folder_path)}")

            # Create README file option
            create_readme = input(
                "\n📝 Create README.txt in new folder? (y/n): "
            ).lower()
            if create_readme == "y":
                readme_path = os.path.join(folder_path, "README.txt")
                with open(readme_path, "w", encoding="utf-8") as f:
                    f.write(f"Folder: {folder_name}\n")
                    f.write(f"Created: {self._get_current_timestamp()}\n")
                    f.write(f"Purpose: \n")
                print(f"✅ README.txt created.")

        except Exception as e:
            print(f"❌ Failed to create folder: {e}")

    def _create_file(self) -> None:
        """Create a new file."""
        Utils.clear_screen()
        Utils.print_header("CREATE NEW FILE")

        current_dir = os.getcwd()
        print(f"📍 Current directory: {current_dir}")

        file_name = input("\nEnter file name (with extension): ").strip()
        if not file_name:
            print("❌ File name cannot be empty.")
            return

        # Handle relative paths
        if "/" in file_name or "\\" in file_name:
            # User might be specifying a path
            if not os.path.isabs(file_name):
                file_path = os.path.join(current_dir, file_name)
            else:
                file_path = file_name
        else:
            file_path = os.path.join(current_dir, file_name)

        # Check if file already exists
        if os.path.exists(file_path):
            print(f"⚠️  File already exists: {file_path}")
            choice = input("Open, Overwrite, or Cancel? (o/w/c): ").lower()

            if choice == "c":
                print("❌ Operation cancelled.")
                return
            elif choice == "o":
                print(f"✅ Opening existing file.")
                # Option to open file could be added here
                return

        # Create parent directories if needed
        parent_dir = os.path.dirname(file_path)
        if parent_dir and not os.path.exists(parent_dir):
            create_parent = input(
                f"Parent directory doesn't exist. Create it? (y/n): "
            ).lower()
            if create_parent == "y":
                try:
                    os.makedirs(parent_dir, exist_ok=True)
                    print(f"✅ Created directory: {parent_dir}")
                except Exception as e:
                    print(f"❌ Failed to create directory: {e}")
                    return
            else:
                print("❌ Operation cancelled.")
                return

        # Get initial content
        print("\n📝 Initial content options:")
        print("1. Empty file")
        print("2. Basic template (based on extension)")
        print("3. Custom content")

        content_choice = input("\nSelect option (1-3): ").strip()

        content = ""
        if content_choice == "2":
            # Provide template based on file extension
            ext = os.path.splitext(file_name)[1].lower()
            content = self._get_file_template(ext, file_name)
            if content:
                print(f"📄 Using {ext} template")
        elif content_choice == "3":
            print("\nEnter file content (end with empty line):")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            content = "\n".join(lines)

        # Create file
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            file_size = os.path.getsize(file_path)
            print(f"✅ File created: {file_path}")
            print(f"📍 Full path: {os.path.abspath(file_path)}")
            print(f"📏 Size: {self._format_size(file_size)}")

        except Exception as e:
            print(f"❌ Failed to create file: {e}")

    def _get_file_template(self, extension: str, filename: str) -> str:
        """Get file template based on extension.

        Args:
            extension: File extension.
            filename: Full filename.

        Returns:
            Template content.
        """
        name_without_ext = os.path.splitext(filename)[0]

        templates = {
            ".py": f'''"""                        
            {filename}
            Created on {self._get_current_timestamp()}
            """

            def main():
            """Main function."""
            print("Hello from {name_without_ext}!")

            if name == "main":
            main()
            ''',
            ".html": f"""<!DOCTYPE html>

            <html lang="en"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <title>{name_without_ext}</title> <style> body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; background-color: #f4f4f4; }} .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }} </style> </head> <body> <div class="container"> <h1>{name_without_ext}</h1> <p>Created on {self._get_current_timestamp()}</p> </div> </body> </html> """,
            ".js": f"""// {filename} // Created on {self._get_current_timestamp()}
            console.log("{name_without_ext} loaded");

            function main() {{
            console.log("Hello from {name_without_ext}!");
            }}

            // Call main function
            main();
            """,
            ".txt": f"""{filename}
            Created on {self._get_current_timestamp()}

            This is a text file.
            """,
            ".md": f"""# {name_without_ext}

            Created on {self._get_current_timestamp()}

            Description
            This is a Markdown file.

            Usage
            Edit this file to add your content.
            """,
            ".json": '''{
            "name": "file",
            "version": "1.0.0",
            "description": "JSON file",
            "created": "'''
            + self._get_current_timestamp()
            + """"
            }""",
            ".css": f"""/* {filename} */
            /* Created on {self._get_current_timestamp()} */

            body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #ffffff;
            }}

            .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            }}
            """,
            ".sql": f"""-- {filename}
            -- Created on {self._get_current_timestamp()}

            -- Create tables
            CREATE TABLE IF NOT EXISTS example (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            -- Insert sample data
            INSERT INTO example (name) VALUES ('Sample Record');

            -- Select data
            SELECT * FROM example;
            """,
        }
        return templates.get(extension, "")

    @staticmethod
    def _get_path_size(path: str) -> int:
        """Get size of file or folder in bytes.

        Args:
            path: Path to file or folder.

        Returns:
            Size in bytes.
        """
        if os.path.isfile(path):
            try:
                return os.path.getsize(path)
            except:
                return 0
        elif os.path.isdir(path):
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(filepath)
                    except:
                        continue
            return total_size
        return 0

    @staticmethod
    def _format_size(size_bytes: int) -> str:
        """Format size in human readable format.

        Args:
            size_bytes: Size in bytes.

        Returns:
            Formatted size string.
        """
        if size_bytes == 0:
            return "0 B"

        units = ["B", "KB", "MB", "GB", "TB"]
        unit_index = 0

        while size_bytes >= 1024 and unit_index < len(units) - 1:
            size_bytes /= 1024.0
            unit_index += 1

        return f"{size_bytes:.2f} {units[unit_index]}"

    @staticmethod
    def _get_current_timestamp() -> str:
        """Get current timestamp string.

        Returns:
            Formatted timestamp.
        """
        from datetime import datetime

        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _copy_to_clipboard(text: str) -> bool:
        """Copy text to clipboard.

        Args:
            text: Text to copy.

        Returns:
            True if successful, False otherwise.
        """
        try:
            import pyperclip

            pyperclip.copy(text)
            return True
        except ImportError:
            # Try platform-specific methods
            try:
                if os.name == "nt":  # Windows
                    import subprocess

                    subprocess.run(["clip"], input=text.encode("utf-8"), check=True)
                    return True
                elif os.name == "posix":  # Linux/Unix
                    import subprocess

                    if "WAYLAND_DISPLAY" in os.environ:
                        subprocess.run(
                            ["wl-copy"], input=text.encode("utf-8"), check=True
                        )
                    else:
                        subprocess.run(
                            ["xclip", "-selection", "clipboard"],
                            input=text.encode("utf-8"),
                            check=True,
                        )
                    return True
                elif os.name == "darwin":  # macOS
                    import subprocess

                    subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=True)
                    return True
            except:
                return False
        except:
            return False
