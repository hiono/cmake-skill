# cmake-skill 🤖 [AI Agent Skill]

**High-Performance CMake Automation Pipeline for Autonomous AI Agents.**

`cmake-skill` is a streamlined, agent-native interface for managing CMake
projects. It handles configuration, parallel building, and testing with a
focus on structured error reporting and token efficiency.

Originally refactored from `mcp-cmake`, it is optimized for high-speed
build/fix cycles.

## 🌟 Key Features

- **Zero-Setup**: Powered by `uv run` (PEP 723). No manual dependency
  installation required.
- **Heuristic Discovery**: Automatically finds `CMakePresets.json` and selects
  appropriate presets.
- **Persistent Dashboard**: Maintains state across runs in `cmake_report.md`.
- **Agent-Ready**: Generates structured JSON/SARIF error reports for
  autonomous agent reasoning.
- **Surgical Building**: Parallelized builds with automatic structured
  diagnostic injection.
- **Clean Policy**: Stores all metadata and reports within the build
  directory.

## 🛠 Skill Installation

### Global (Recommended)

```bash
git clone https://github.com/hiono/cmake-skill ~/.agents/skills/cmake-skill
export PATH="$HOME/.agents/skills/cmake-skill/scripts:$PATH"
```

## 📖 Usage

```bash
# List presets
cmake-skill list

# Configure (Auto-discovery)
cmake-skill configure

# Build (Parallel)
cmake-skill build

# Test (CTest)
cmake-skill test

# Run full pipeline
cmake-skill pipeline
```

## 🔄 What's New in v0.2.0

- **Single-File Architecture**: Script is now a single `.py` file (`cmake-skill`)
  instead of separate Python + shell wrapper. Simpler installation!
- **uv Run Powered**: Dependencies (Jinja2) handled automatically via `uv run`.
  No manual `pip install` needed.
- **Persistent Dashboard**: `cmake_report.md` now persists across runs, showing
  build history and cumulative error data.

## 🤖 Reasoning Protocol

The agent follows the **[protocol.md](references/protocol.md)** to recover
from build failures autonomously by parsing the structured error logs.

---

Maintained by **hiono**. Distributed under the MIT License.
