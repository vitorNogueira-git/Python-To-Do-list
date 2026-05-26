#To do CLI

A simple yet complete command-line To-Do List application built in Python — great for learning project structure, testing, and CLI design.

---

## Features

- Add tasks with **title** and **priority** (low / medium / high)
- Mark tasks as **complete**
- **Edit** task titles
- **Delete** individual tasks or **clear** all completed ones
- **List** all, pending, or done tasks
- **Search** by keyword
- **Filter** by priority
- Persistent storage via a local JSON file (`~/.todo_data.json`)
- Colorized terminal output
- Full unit test coverage with `pytest`

---

## Project Structure

```
todo-app/
├── todo/
│   ├── __init__.py     # Package metadata
│   ├── models.py       # Task data model (dataclass + enums)
│   ├── storage.py      # JSON file persistence
│   ├── manager.py      # Business logic (add, complete, delete, …)
│   └── cli.py          # argparse CLI entry-point
├── tests/
│   ├── test_models.py  # Tests for the Task model
│   └── test_manager.py # Tests for TaskManager
├── setup.py
├── pyproject.toml
├── requirements-dev.txt
├── LICENSE
└── README.md
```

---

## Installation

### Option 1 — Run directly (no install)

```bash
git clone https://github.com/your-username/todo-app.git
cd todo-app
python -m todo.cli --help
```

### Option 2 — Install as a package (adds `todo` command)

```bash
git clone https://github.com/your-username/todo-app.git
cd todo-app
pip install -e .
todo --help
```

---

## Usage

```bash
# Add tasks
todo add "Buy groceries"
todo add "Finish report" --priority high
todo add "Read a book" -p low

# List tasks
todo list          # all tasks
todo pending       # pending only
todo done-list     # completed only

# Complete / Delete / Edit
todo complete 1
todo delete 2
todo edit 3 "Updated title"

# Search & Filter
todo search groceries
todo filter high

# Housekeeping
todo clear-done    # removes all completed tasks
```

### Example Output

```
────────────────────────────────────────────────────────────
  All Tasks
────────────────────────────────────────────────────────────
  [✓] #1  → medium  Buy groceries       (2024-01-15T10:30:00)
  [○] #2  ↑ high    Finish report       (2024-01-15T10:31:00)
  [○] #3  ↓ low     Read a book         (2024-01-15T10:32:00)

  Total: 3  |  Done: 1  |  Pending: 2
```

---

## Running Tests

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage report
pytest --cov=todo --cov-report=term-missing
```

---

## Architecture Overview

| Layer | File | Responsibility |
|---|---|---|
| Model | `models.py` | `Task` dataclass, `Priority` & `Status` enums |
| Storage | `storage.py` | Read/write tasks to `~/.todo_data.json` |
| Manager | `manager.py` | All business logic; depends on Storage |
| CLI | `cli.py` | Parses `sys.argv`, calls Manager, prints output |

The layers are kept intentionally separate so you can swap the storage backend (e.g. SQLite) or the UI (e.g. a web API) without touching business logic.

---

## Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## License

[MIT](LICENSE)
