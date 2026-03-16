# cmake-skill 🤖 [AI Agent Skill]

**Diagnostic-First CMake Automation for Autonomous AI Agents.**

`cmake-skill` provides deep visibility into the CMake build lifecycle. It captures complex configuration failures and maintains a persistent view of project health across multiple development phases.

## 🌟 Key Features

- **Hierarchical Parsing**: State-machine engine captures multi-line error messages and full `include()` call stacks.
- **Unified Pipeline**: Coordinated execution of formatting, linting, configuration, building, and testing.
- **Persistent Status**: Tracks the state of each build phase across runs via a structured dashboard.
- **Domain Specificity**: Custom command validation for IP development workflows (e.g., CPM.cmake integration).

## 🛠 Installation

Requires `cmake`, `ninja`, and `uv`.

```bash
git clone https://github.com/hiono/cmake-skill ~/.agents/skills/cmake-skill
```

## 📖 Usage

```bash
# Run full quality-gate pipeline
./scripts/cmake-skill pipeline

# Configure with precision error capture
./scripts/cmake-skill configure

# Static analysis for CMake scripts
./scripts/cmake-skill lint
```

## 🤖 Reasoning Protocol

Refer to **[protocol.md](references/protocol.md)** to maintain project health and recover from build failures.

## 🔗 Orchestration

```mermaid
graph TD
    subgraph Quality Pipeline
        A[cmake-skill]
        B[cpp-lint]
    end

    A -->|writes| A1[.cmake-skill-manifest.json]
    A -->|writes| A2[build/preset/cmake_reports/]

    B -->|writes| B1[.cpp-lint-manifest.json]
    B -->|writes| B2[cpp_lint_reports/]

    A1 --> C[verify-quality]
    A2 --> C
    B1 --> C
    B2 --> C

    C -->|writes| D[quality_reports/]

    style A fill:#4a90d9,stroke:#333,color:#fff
    style B fill:#d94a4a,stroke:#333,color:#fff
    style C fill:#50b85f,stroke:#333,color:#fff
    style D fill:#f5a623,stroke:#333,color:#fff
```

This skill **writes** reports to `cmake_reports/` and `.cmake-skill-manifest.json`.
It does **not** depend on other skills, but other skills (verify-quality) read its output.

---
Maintained by **hiono**. Version **v0.3.2**.