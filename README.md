# ♟️ Chess Tournament Manager

A command-line interface (CLI) program developed in Python to manage offline chess tournaments. This application allows you to create players, manage tournaments, automate match pairings, and generate reports.

The project follows the **MVC** (Model-View-Controller) architecture.

## ✨ Features

* **Player Management**: Create, update, and delete players in a JSON database.

* **Tournament Management**: Configuration (name, location, dates, number of rounds), adding players.

* **Tournament System**:
    * Automatic pairing generation.
    * Score management (Win, Loss, Draw).
    * Exempt player management.

* **Reports**: Standings, alphabetical player list, tournament history.


## 📦 Installation

Follow these steps to set up the development environment:

### 1. Clone the repository
Clone the GitHub repository or download the source files.

git clone https://github.com/Mnr04/chess_tournament_manager.git

### 2. Create a virtual environment

On windows:
```bash
   python -m venv env
   env\Scripts\activate
```
On macOs / Linux:
python3 -m venv env
source env/bin/activate

### 3. Install dependencies

pip install -r requirements.txt

## 🚀 Launch the program 

python main.py

### ➤ Navigation

- Use the Arrow Keys (Up/Down) to navigate through menus.
- Press Enter to validate a choice.
- Follow the on-screen instructions to enter information.

## 🔍 Code Quality Report (Flake8)

The project includes a linting report generated with flake8 to ensure compliance with PEP 8 standards.

### 👁️ View the existing report
Simply open the following file in your web browser: flake-report/index.html

### 📝 Generate a new report
If you modify the code and want to check its quality or generate a new HTML report:

Ensure you are at the root of the project.

Run the following command:

flake8 --format=html --htmldir=flake-report
