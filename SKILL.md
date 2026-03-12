name: cmake-skill
description: "Agent-native CMake lifecycle automation. Use when Claude needs to: (1) Configure, build, or test CMake projects, (2) Capture and parse multi-line configuration errors or call stacks, or (3) Maintain project health visibility via a persistent dashboard."

# CMake Build & Diagnostics

Manage CMake projects with persistent situational awareness.

## 📋 Workflow

1. **Orchestration**: Prefer `./skill/cmake-skill/scripts/cmake-skill pipeline` for full verification.
2. **Monitoring**: Review `cmake_report.md` at project root for an immediate health summary.
3. **Extraction**: Parse `.lint/cmake_report.json` for structured diagnostic data.
4. **Customization**: Adjust `.cmake-format.py` to add specs for project-specific commands.

## 🤖 Failure Recovery

Refer to **[protocol.md](references/protocol.md)** for hierarchical error parsing and state management logic.