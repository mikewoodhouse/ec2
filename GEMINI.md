# GEMINI.md

## Project Overview

**ec2** is a standalone cricket scoring package designed to provide value as both a standalone tool and a support package for the `extracover` project.

- **Primary Technologies:** Python 3.13+, [uv](https://docs.astral.sh/uv/) for dependency management, [NiceGUI](https://nicegui.io/) for the user interface.
- **Key Dependencies:** `dataclasses-json`, `nicegui`, `pytest`.
- **Architecture:** 
    - **Scorebook:** Core logic in `src/ec2/scorebook/`, defining data structures for `Ball`, `Extra`, `HowOut`, `Batter`, `Bowler`, and `ScoreCard`.
    - **UI:** NiceGUI-based interface in `src/ec2/ui/`, with `Display` and `InningsCard` classes managing the application state and view.
    - **State Management:** Utilizes `nicegui.binding` for reactive updates between the scoring logic and the UI.

## Building and Running

The project uses `uv` for environment management and task execution.

- **Run the Application:**
  ```bash
  uv run ec2
  ```
  *(Note: This executes the script defined in `pyproject.toml` pointing to `ec2:main`)*

- **Run Tests:**
  ```bash
  pytest
  ```

- **Run Tests with Watcher:**
  ```bash
  pytest-watcher .
  ```

- **Build the Project:**
  ```bash
  uv build
  ```

## Development Conventions

- **Data Classes:** Extensively uses standard library `dataclasses` combined with `dataclasses-json` for serialization and `nicegui.binding.bindable_dataclass` for UI reactivity.
- **Enums:** Uses `StrEnum` for `Extra` and `HowOut` types to ensure type safety and easy string representation.
- **Testing:** 
    - Tests are located in the `tests/` directory.
    - Uses `pytest` with fixtures that load historical match data from JSON files (e.g., `tests/951373.json`).
    - New features should be verified against these data-driven tests to ensure scoring accuracy.
- **Source Structure:** 
    - `src/ec2/`: Core package.
    - `main.py`: Entry point for the NiceGUI application.
- **Formatting & Style:** Adhere to modern Python standards (type hints, clean dataclass definitions).
