---
name: cmake-skill
description: |
  High-performance CMake automation for AI Agents.
  Handles: (1) Configuration with Presets, (2) Parallel Building,
  (3) Testing via CTest, (4) Structured Error Reporting (JSON/SARIF).
  Heuristically discovers CMakePresets.json and provides structured data for
  autonomous fixing.
compatibility: opencode
---

# cmake-skill 🤖

Agent-Native CMake automation pipeline.

## Quick Start

```bash
# List available presets
cmake-skill list

# Configure project (auto-selects 'dev' or first preset)
cmake-skill configure

# Build project (Parallelized)
cmake-skill build

# Run tests
cmake-skill test
```

## Agent Protocol

When a build or test fails, the agent should:
1.  Read the structured report at the path output by the command
    (e.g., `build/{preset}/.lint/cmake_build.json`).
2.  Analyze `errors` for missing headers, syntax errors, or linker issues.
3.  Consult [protocol.md](references/protocol.md) for recovery strategies.

## Integration

- Stores artifacts in `build/{preset}/.lint/` to keep root clean.
- Works seamlessly with `cpp-lint`.
