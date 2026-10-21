# Agent Equipment Config Codex Plugin Security Closeout

Scope: repo marketplace entry, Codex plugin manifest, bundled MCP config,
plugin-local launcher, `PreToolUse` guard hook, routing skill, and validator
coverage for the Agent Equipment Config Codex plugin.

## Boundary

The plugin exposes the existing standalone Config MCP server to Codex. It does
not add a network endpoint, secret resolver, provider mutation path, or Config
runtime implementation. The plugin runs from the Codex plugin cache and binds
back to a live Armory checkout only when `AGENT_ARMORY_ROOT` or the process
working directory resolves to a checkout containing these markers:

- `tools/agent_equipment_config_mcp_server.py`
- `inventory/equipment.toml`
- `.agents/plugins/marketplace.json`

The MCP launcher changes directory to the resolved checkout before executing
`tools/agent_equipment_config_mcp_server.py` with the absolute path of the
current Python interpreter.

## Controls

- `.mcp.json` uses a direct local server map, `python3.14`, plugin-local
  launcher args, `env_vars = ["AGENT_ARMORY_ROOT"]`, default prompt approval,
  and prompt overrides for `config.apply` and `migrate.config_apply`.
- No static secrets, HTTP MCP endpoint, broad server environment pass-through,
  or alternate executable path is allowed by the validator.
- The launcher rejects lookalike roots without the Armory marketplace marker,
  uses an absolute interpreter path and an `AGENT_ARMORY_ROOT`-only server
  environment for the final `exec`, and fails closed with install guidance when
  no trusted checkout is found.
- The guard hook no-ops unrelated tools and denies Config local-write MCP calls
  unless the tool input includes `apply_authority = "operator"`.
- The validator statically restricts launcher and hook imports, functions,
  entrypoints, constants, decorators, command paths, MCP config, and hook shape
  before running bounded behavior probes.
- Codex hook trust and MCP approval prompts remain host policy surfaces.

## Review Disposition

The review loop found actionable validator gaps: launchers without `_argv`
assignment could pass static validation, reviewed functions could carry
decorators that run during import, stock inventory could omit the plugin
component paths while the plugin files still existed, and launcher failure
branches could pass with nonterminal return or misplaced module-entrypoint
shapes. The validator now requires the `_argv` assignment, rejects decorators on
reviewed launcher and guard functions before behavior probes import plugin code,
checks inventory component projection, accepts only terminal failure returns in
the reviewed launcher guards, and requires the module entrypoint to be final
after `launch()`.

A fresh isolated Codex prototype using `CODEX_HOME` under `/tmp` installed
`agent-equipment-config@agent-armory` from `.agents/plugins/marketplace.json`
and exposed the bundled MCP server from the cached plugin path. That confirms
the marketplace source path is resolved from the marketplace root, not the JSON
file's directory.

## Evidence

This committed closeout is the durable security evidence record for the Codex
plugin delivery. The Codex Security diff scan covered the executable plugin
boundary and found no reportable findings. Instance-scoped scan output stayed in
scratch storage; the durable conclusion is this document's scope, controls, and
findings disposition.

Validation commands completed for the security-relevant surface:

- `python3.14 -m unittest tests.test_agent_equipment_config_codex_plugin`
- `python3.14 -m unittest tests.test_validate_armory_integrity`
- `python3.14 -m unittest`
- `python3.14 tools/harness_capability_profiles.py validate --json`
- `python3.14 tools/validate_armory_integrity.py --final-closeout --json`
- `git diff --check`


## Installed runtime provenance correction

The historical review above did not bind the installed plugin to executable
server bytes. Marker-valid checkout code could replace the server after plugin
installation. Security Cloud finding `csf_e454d541d2d1852ee17c28f8`, occurrence
`occ_e97d6bdcc70fd1253a2798b3`, identified this gap.

The plugin now packages the canonical Config engine and stdio wrapper under
`mcp/runtime/tools/` with an empty package initializer. Both launcher startup
and child execution use Python `-I -S`. The selected checkout supplies only the
data working directory; the executable path resolves from the installed
launcher. Missing runtime files fail closed without a checkout fallback.

`tools/build_agent_equipment_config_plugin.py` refreshes the snapshot, and
repository integrity validation checks byte parity, initializer content,
symlink-free bundle paths, installation arguments, and stock component paths.
This preserves one canonical implementation while binding installed executable
behavior to the plugin installation. Runtime updates require updating or
reinstalling the plugin.

The subprocess regression copies the plugin before changing checkout server,
engine, package initializer, and import-shadow files. It exercises environment
selection, ancestor discovery, symlink aliases, initialization, tool listing,
and a read-only Config request using a relative layer path. A separate test
removes each bundled file and verifies refusal without checkout execution.
Existing approval, write guard, and runtime mutation contracts remain in place.

Security verification uses the Codex Security finding-fix workflow and a fresh
read-only bypass/regression review. This narrower action covers the executable
boundary and its complete stdlib-only import closure; a new repository-wide scan
would add unrelated scope. The canonical engine and wrapper are copied without
behavior changes. Portable test and review results belong in the PR and tracking
issue. Instance-specific logs and temporary reproducer directories are scratch
evidence and are not retained as project truth.

This correction does not claim installation on an operator machine. Existing
cached plugins require an update or reinstall. Repository-scan status writeback
is separate from code verification.
