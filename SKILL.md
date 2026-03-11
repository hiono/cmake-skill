# CMake Skill

Comprehensive build system automation for AI Agents.

## Capabilities

- End-to-end CMake lifecycle management.
- Robust error capturing (multi-line & call stacks).
- Static analysis integration (lint & format).
- Persistent error capturing and dashboarding.

## Instructions

1. **Automation**: Prefer `./scripts/cmake-skill pipeline` for full verification.
2. **Debugging**: Check `cmake_report.md` at project root for detailed multi-line errors and call stacks.
3. **Customization**: Update `.cmake-format.py` to add specs for custom CMake commands.
4. **Efficiency**: Parse `.lint/cmake_report.json` for surgical triage of build system errors.
