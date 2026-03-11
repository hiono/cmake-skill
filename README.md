# cmake-skill

Agent-Native CMake automation pipeline with persistent dashboard reporting.

## Features

- **Zero-Setup**: Powered by \`uv run\`.
- **Persistent Dashboard**: Maintains state across runs in \`cmake_report.md\`.
- **Pipeline Logic**: Supports atomic workflows.

## Usage

\`\`\`bash
./scripts/cmake-skill pipeline   # Run full flow
./scripts/cmake-skill configure  # Only configure
./scripts/cmake-skill build      # Only build
./scripts/cmake-skill test       # Only test
\`\`\`
