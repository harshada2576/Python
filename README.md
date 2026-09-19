# Python Learning Projects

A collection of Python practice scripts and small applications covering language fundamentals, desktop GUIs, command-line tools, and data processing.

## Contents

### Task manager CLI

The most complete standalone application is the JSON-backed task manager in `cli_app/`. It supports adding tasks with priorities, listing and filtering tasks, completing and deleting tasks, and displaying statistics.

Run it from the repository root:

```bash
python cli_app/task.py --help
python cli_app/task.py add "Finish the README" --priority high
python cli_app/task.py list
python cli_app/task.py complete 1
python cli_app/task.py stats
```

Task data is stored in `cli_app/tasks.json`.

### Calculator GUI

`calculator.py` is a PyQt5 calculator with arithmetic operators, decimals, sign changes, clearing, backspace, and evaluation.

```bash
python calculator.py
```

The generated executable under `dist/` and PyInstaller working files under `build/` are local build artifacts and are intentionally ignored by Git.

### Weather GUI

`weather.py` is a PyQt5 weather viewer that queries OpenWeatherMap for the current conditions of a city.

```bash
python weather.py
```

The script currently contains an API key in its source. Replace it with a key that you own, and avoid committing real credentials. The free endpoint used by the script provides current weather; the displayed forecast is informational only.

### CSV to SQLite

`csv_to_sqlite.py` reads `data/sample.csv`, validates names and email addresses, normalizes rows, and appends valid records to a SQLite `users` table in `data/mydb.sqlite`.

Install the data-processing dependencies and run it from the repository root:

```bash
python -m pip install pandas SQLAlchemy
python csv_to_sqlite.py
```

Invalid rows are reported in the terminal. Generated SQLite files are ignored by Git.

### Learning examples

The remaining top-level scripts are small, independent examples for practicing Python syntax and standard-library concepts, including variables, types, strings, collections, loops, functions, command-line arguments, decorators, type hints, file input/output, and execution timing.

They can generally be run directly with Python, for example:

```bash
python functions.py
python dictionary.py
python pydecorator.py
```

## Requirements

- Python 3.9 or newer is recommended.
- The task manager and learning examples mostly use the Python standard library.
- PyQt5 is needed for `calculator.py`, `weather.py`, and the PyQt examples.
- `requests` is needed by `weather.py`.
- `pandas` and `SQLAlchemy` are needed by `csv_to_sqlite.py`.

Install the optional application dependencies with:

```bash
python -m pip install PyQt5 requests pandas SQLAlchemy
```

## Repository layout

```text
cli_app/       JSON-backed command-line task manager
data/          Sample CSV input
ui/            UI resources and experiments
Basics/        Additional learning material
build/         Ignored PyInstaller build output
dist/          Ignored packaged executables
```

## Development notes

- Run commands from the repository root unless a command says otherwise.
- Python bytecode, virtual environments, build output, distribution output, and generated SQLite databases are excluded by `.gitignore`.
- These scripts are educational examples rather than a single packaged library or production application.
