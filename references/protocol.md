# Agent Reasoning & Action Protocol: CMake

Follow this logic when handling CMake build/test cycles:

## 1. Discovery Phase

- If the agent doesn't know which preset to use, run `cmake-skill list`.
- **Preference**: Use `dev` or `default` presets for local development.

## 2. Recovery Strategies (Autonomous Fixing)

### Build Failures

- **Missing Header**: Check if the header exists in `include/` or `src/`.
  If it's a dependency, ensure `vcpkg` or `CPM` is initialized.
- **Linker Error**: Verify that the source file is added to `add_library` or
  `add_executable` in the corresponding `CMakeLists.txt`.
- **Syntax Error**: Open the file at the reported `line`/`column` and apply
  a fix.

### Configuration Failures

- **Missing Database**: If `compile_commands.json` is missing, run
  `cmake-skill configure`.
- **Toolchain Issues**: Ensure `clang` or the expected compiler is in the PATH.

## 3. Verification

- After any fix, **Always** re-run `cmake-skill build` then `cmake-skill test`.
- Success is only achieved when `success: true` is reported in the final JSON.

## 4. jq Quick Reference (Surgical Triage)

Query the `machine_report` to find specific failures:

```bash
# Check status of all steps
jq '.quick_ref.steps' <machine_report>

# Get detailed errors for the 'build' phase
jq '.build.errors' <machine_report>

# Filter build errors by file
jq '.build.errors[] | select(.file | contains("state_machine.cpp"))' <machine_report>
```

## 5. Advanced jq Triage Patterns

```bash
# List all failed steps with their first error message
jq '. | to_entries[] | select(.value.success == false) | {step: .key, first_error: .value.errors[0].message}' \\
  <machine_report>

# Filter errors by a specific source file
jq '.build.errors[] | select(.file | contains("state_machine.cpp"))' <machine_report>
```
