---
name: cmake-skill
description: |
  Agent-native CMake lifecycle automation with persistent project health monitoring. Use when Claude needs to:
    1. Configure, build, or test CMake projects,
    2. Capture and parse multi-line configuration errors or call stacks,
    3. Maintain project health visibility via a persistent dashboard.
---

# CMake Build & Diagnostics

Manage CMake projects with persistent situational awareness.

## Resources

- **Error parsing**: `references/protocol.md` for hierarchical error parsing and state management logic.
- **Dashboard**: Review `cmake_report.md` in build directory for health summary.
- **Script**: `scripts/cmake-skill` for the full pipeline.

## Workflow

1. **Orchestrate**: Run `scripts/cmake-skill pipeline` for full verification.
2. **Monitor**: Review `build/<preset>/cmake_reports/cmake_report.md` for health summary.
3. **Extract**: Parse `build/<preset>/cmake_reports/cmake_report.json` for structured diagnostic data.
4. **Customize**: Adjust `.cmake-format.py` to add specs for project-specific commands.
   **Build fails?** → Read `references/protocol.md` for hierarchical error parsing and state management.

## Execution

**Always use `uv run --script` to execute this skill:**
```bash
uv run --script scripts/cmake-skill <action> [options]
```

**Why:** Python environments managed by uv (PEP 668 externally-managed) block `pip install`. Running with `python3` directly will fail when auto-installing jinja2. `uv run --script` handles PEP 723 inline dependencies correctly.

**Note:** Run from the skill root directory (`~/.agents/skills/cmake-skill/`) or use the agent's skill tool to resolve the path.
