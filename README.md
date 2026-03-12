# cmake-skill 🤖 [AI Agent Skill]

**Zero-Setup, Dashboard-Driven CMake Automation for Autonomous AI Agents.**

`cmake-skill` is a streamlined, agent-native interface for managing the complete
build lifecycle. It provides persistent dashboarding, robust multi-line error
parsing, and integrated static analysis—all with zero environment setup.

## 🌟 Key Features

- **Zero-Setup**: Powered by `uv run` (PEP 723). Dependencies are handled
  automatically.
- **Robust Parsing**: State-machine parser captures multi-line errors and
  full `include()` call stacks.
- **Persistent Dashboard**: Maintains a stateful `cmake_report.md` at project
  root for situational awareness.
- **Full Pipeline**: Orchestrates `format` -> `lint` -> `configure` ->
  `build` -> `test` in a single command.
- **IP-Core Ready**: Custom command specs for `CPM.cmake` and IP-specific
  conventions.

## 🛠 Installation

```bash
# Clone to the standard skill location
git clone https://github.com/hiono/cmake-skill ~/.agents/skills/cmake-skill
```

## 📖 Usage

Run directly as an executable (powered by `uv`):

```bash
# Run the full quality-gate pipeline
./scripts/cmake-skill pipeline

# Configure with precision error capture
./scripts/cmake-skill configure

# Static analysis for CMake scripts
./scripts/cmake-skill lint
```

## 🤖 Reasoning Protocol

The agent follows the **[protocol.md](references/protocol.md)** to maintain
project health and recover from build failures autonomously.

---

Maintained by **hiono**. Updated to **v0.2.0** with Dashboard Architecture.
