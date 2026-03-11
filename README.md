# cmake-skill

Agent-Native CMake automation pipeline with persistent dashboard reporting.

## Features

- **Zero-Setup**: Powered by `uv run`. Dependencies (Jinja2) are handled automatically.
- **Robust Parsing**: State-machine based parser captures multi-line errors and full call stacks.
- **Static Analysis**: Integrated `cmake-lint` and `cmake-format --check`.
- **Custom Commands**: Supports custom command specifications (e.g., CPM.cmake) via `.cmake-format.py`.
- **Persistent Dashboard**: Maintains state across runs in `cmake_report.md`.
- **Pipeline Logic**: Supports atomic workflows: `format` -> `lint` -> `configure` -> `build` -> `test`.

## Usage

```bash
./scripts/cmake-skill pipeline   # Run full flow
./scripts/cmake-skill format     # Check formatting
./scripts/cmake-skill lint       # Run static analysis
./scripts/cmake-skill configure  # Only configure
./scripts/cmake-skill build      # Only build
./scripts/cmake-skill test       # Only test
```

## Requirements

- `uv` (Fast Python package manager)
- `cmake`, `ctest`, `ninja` (Build tools)
- `cmake-format`, `cmake-lint` (Static analysis tools)
