# DPM - Developer's Productivity Manager

A powerful command-line toolbox for Python developers, featuring Django project management, virtual environment handling, file operations, Git helpers, and AI context generation – all in one place.

![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20|%20Linux%20|%20macOS-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📦 Features

- **🚀 Django Manager** – Create projects, apps, run migrations, start development server.
- **🐍 Environment Manager** – Create/delete virtual environments (`.venv`/`venv`), manage `.env` files, check Python environment.
- **📁 File Operations** – List, copy, move, delete files/folders with safety confirmations and size calculations.
- **📊 File Statistics** – Count files and folders by extension, see project size.
- **📄 Generate AI Context** – Produce an optimised project snapshot for AI assistants (smart file selection, ignore patterns).
- **🔧 Git & Requirements** – Generate/update `.gitignore` from templates, create `requirements.txt`, install packages.
- **🧹 Clean __pycache__** – Recursively delete all `__pycache__` folders with space summary.

All tools are accessible via a clean, numbered menu.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.6 or higher
- Git (optional, for cloning)

### Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/Alexashok99/dpm.git
   cd dpm
   ```

2. **(Optional) Create and activate a virtual environment**  
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/macOS
   source .venv/bin/activate
   ```

3. **No external dependencies required** – the tool uses only Python standard library.

4. **Run the application**  
   ```bash
   python main.py
   ```

---

## 🖥️ Usage

When you run `python main.py`, you'll see the main menu:

```
==================================================
                 🛠 TOOL EXECUTER                 
==================================================
1. 🧹 Clean __pycache__ — Remove all __pycache__ folders recursively
2. 🚀 Django Manager — Create Django project, check, create app, migrate, runserver
3. 🐍 Environment Manager — Create/delete virtual env, create/delete .env file
4. 📊 File Statistics — Count files and folders by type
5. 📁 File Operations — List, copy, move, delete files and folders
6. 📄 Generate AI Context — Create optimized project context with filtering options for AI
7. 🔧 Git & Requirements — Manage .gitignore, requirements.txt, install packages
0. Exit
----------------------------------------
Select option:
```

Just enter the number of the tool you need and follow the interactive prompts.

---

## ⚙️ Configuration

### Ignore Lists
The default directories and files to ignore (e.g., `.git`, `__pycache__`, `.env`) are stored in `configs_file/config.py`. You can modify the `DEFAULT_IGNORE_DIRS` and `DEFAULT_IGNORE_FILES` sets there, or use the tool’s interactive options (e.g., in **Generate AI Context**) to add custom exclusions.

### Environment Variables
Some tools (like **Environment Manager**) let you create `.env` files with common templates. The tool itself does not require any environment variables to run, but you can set the following to customise behaviour:

- `DPM_NO_COLOR` – Set to any value to disable coloured output (not yet implemented, but reserved for future use).

---

## 🪟 Using `dpm.bat` (Windows)

A batch file `dpm.bat` is included in the project root. It allows you to run the tool from any command prompt by simply typing `dpm`.

### What `dpm.bat` does
It calls `python main.py` from the directory where the script is located, so you don't have to navigate to the project folder each time.

### Make `dpm` available globally (Windows)

1. **Copy `dpm.bat` to a folder in your PATH**  
   For example, create a folder `C:\bin` and add it to your system PATH:
   - Open **System Properties** → **Advanced** → **Environment Variables**
   - Under **System variables**, select `Path` and click **Edit**
   - Add `C:\bin` (or your chosen folder)
   - Copy `dpm.bat` into that folder

2. **Or add the project folder to PATH**  
   Add the full path of the `dpm` project folder to your PATH instead. Then you can run `dpm` from anywhere.

After either step, open a new Command Prompt and type:
```bash
dpm
```
You should see the main menu.

### For Linux/macOS users
Create an alias in your `~/.bashrc` or `~/.zshrc`:
```bash
alias dpm='python3 /path/to/dpm/main.py'
```
Then reload with `source ~/.bashrc`.

---

## 📂 Project Structure Overview

```
dpm/
├── configs_file/          # Configuration classes
│   └── config.py
├── tools/                 # All tool implementations
│   ├── base_tool.py       # Base class for all tools
│   ├── clean_pycache_script.py
│   ├── django_tool.py
│   ├── env_tool.py
│   ├── file_counter_tool.py
│   ├── file_ops_tool.py
│   ├── full_context_tool.py
│   ├── git_requirements_tool.py
│   └── loader.py          # Dynamic tool loader
├── util/                  # Utility functions
│   └── utils.py
├── main.py                # Application entry point
├── dpm.bat                # Windows launcher
└── README.md              # This file
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests. Please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some amazing feature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👤 Author

**Alex Ashok**  
- GitHub: [@Alexashok99](https://github.com/Alexashok99)

---

## 🙏 Acknowledgements

- Inspired by everyday development needs – from Django project setup to cleaning up `__pycache__`.
- Built with Python's standard library – no extra dependencies required.

---

*Happy coding!* 🚀

