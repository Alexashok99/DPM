# main.py
"""Main entry point for Scripts_module."""

from tools.loader import load_tools
from util.utils import Utils

class ProjectStructureApp:
    """Main application class."""

    def __init__(self):
        """Initialize application."""
        self.tools = load_tools()
        self.running = True

    def display_menu(self) -> None:
        """Display the main menu."""
        Utils.clear_screen()
        Utils.print_header("🛠 TOOL EXECUTOR")

        for idx, tool in enumerate(self.tools, start=1):
            print(f"{idx}. {tool.name} — {tool.description}")
        print("0. Exit")
        print("-" * 40)

    def run(self) -> None:
        """Run the main application loop."""
        while self.running:
            self.display_menu()
            choice = input("Select option: ").strip()

            if choice == "0":
                break

            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(self.tools):
                    self.tools[index].run()
                else:
                    print("❌ Invalid option")
            else:
                print("❌ Invalid input")

            input("\nPress Enter to continue...")

def main():
    """Main entry point"""
    app = ProjectStructureApp()
    app.run()


if __name__ == "__main__":
    main()