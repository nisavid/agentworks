# Agent Equipment Config Codex Plugin Security Closeout

Scope: repo marketplace entry, Codex plugin manifest, bundled MCP config,
plugin-local launcher, `PreToolUse` guard hook, routing skill, and validator
coverage for the Agent Equipment Config Codex plugin.

## Boundary

The plugin exposes the existing standalone Config MCP server to Codex. It does
not add a network endpoint, secret resolver, provider mutation path, or Config
runtime implementation. The plugin runs from the Codex plugin cache and binds
back to a live Agentworks checkout only when `AGENTWORKS_ROOT` or the process
working directory resolves to a checkout containing these markers:

- `tools/agent_equipment_config_mcp_server.py`
- `inventory/equipment.toml`
- `.agents/plugins/marketplace.json`

The MCP launcher changes directory to the resolved data checkout before executing
the installed `mcp/runtime/tools/agent_equipment_config_mcp_server.py` with the
absolute path of the current Python interpreter and `-I -S`. Checkout markers
select data; the installed runtime supplies executable code.

## Controls

- `.mcp.json` uses a direct local server map, `python3.14 -I -S`, plugin-local
  launcher args, `env_vars = ["AGENTWORKS_ROOT"]`, default prompt approval,
  and prompt overrides for `config.apply` and `migrate.config_apply`.
- No static secrets, HTTP MCP endpoint, broad server environment pass-through,
  or alternate executable path is allowed by the validator.
- The launcher rejects lookalike roots without the Agentworks marketplace marker,
  uses an absolute interpreter path and an `AGENTWORKS_ROOT`-only server
  environment for the final `exec`, and fails closed with install guidance when
  no trusted checkout is found.
- The guard hook no-ops unrelated tools and denies Config local-write MCP calls
  unless the tool input includes `apply_authority = "operator"`.
- The validator requires the complete launcher and guard ASTs to match reviewed
  programs owned by the trusted validator. Comments and formatting may differ;
  executable statements, expressions, bindings, signatures, and annotations may
  not. Candidate source is parsed from bytes so Python encoding declarations
  cannot change the program after validation. Semantic plugin changes require
  reviewing and updating those programs.
- Behavior probes execute only those validator-owned programs with isolated
  Python (`-I -S -c`), an empty environment, and time limits. Guard output remains
  bounded. They never import or execute Python from the checkout under review,
  including after a candidate file changes between validation and probing.
- The shipped launcher and guard commands use `-I -S` to exclude ambient import paths
  and site startup code. Validation rejects additional entries in the
  plugin's `mcp` and `hooks` runtime directories; tests exercise both shipped
  commands with standard-library shadow modules in those directories.
- Codex hook trust and MCP approval prompts remain host policy surfaces.

## Review Disposition

The review loop found actionable validator gaps: launchers without `_argv`
assignment could pass static validation, reviewed functions could carry
decorators that run during import, stock inventory could omit the plugin
component paths while the plugin files still existed, and launcher failure
branches could pass with nonterminal return or misplaced module-entrypoint
shapes. The validator now requires the `_argv` assignment, rejects decorators on
reviewed launcher and guard functions before behavior probes,
checks inventory component projection, accepts only terminal failure returns in
the reviewed launcher guards, and requires the module entrypoint to be final
after `launch()`.

Subsequent current-code security revalidation found that partial AST allowlists
still admitted indirect calls, extra assignment targets, and import-time
defaults. Complete AST comparison replaces that execution boundary; probes run
trusted canonical programs rather than reopening candidate files. Regression
coverage rejects unreviewed code before probing and replaces candidate files at
the probe boundary to verify that their contents cannot execute. Positive
controls retain the current plugin contract, comment and formatting flexibility,
root discovery with `start_dir` omitted, environment filtering, and the guard's
allow/deny decisions. This control assumes the validator itself comes from a
trusted checkout, as described in the repository threat model.

Before the identity rename, a fresh isolated Codex prototype using `CODEX_HOME` under `/tmp` installed
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
- `python3.14 -m unittest tests.test_validate_agentworks_integrity`
- `python3.14 -m unittest`
- `python3.14 tools/harness_capability_profiles.py validate --json`
- `python3.14 tools/validate_agentworks_integrity.py --final-closeout --json`
- `git diff --check`


## Installed runtime provenance correction

The historical review above did not bind the installed plugin to executable
server bytes. Marker-valid checkout code could replace the server after plugin
installation. Security Cloud finding `csf_e454d541d2d1852ee17c28f8`, occurrence
`occ_e97d6bdcc70fd1253a2798b3`, identified this gap.

The plugin now packages the canonical Config engine and stdio wrapper under
`mcp/runtime/tools/` with an empty package initializer. Launcher startup,
child execution, and the write guard use Python `-I -S`. The selected checkout supplies only the
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

The installed hook command is also exercised with inherited `PYTHONPATH`
pointing at checkout startup code. That code must not execute; normal denial,
operator allowance, migration denial, and malformed-input handling must remain.

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

The runtime snapshot also includes the canonical create-layer payload binding
correction merged in PR #221. Refreshing the bundle preserves that correction
for installed plugins: reviewed changes and canonical metadata determine the
document validated and written. Checkout code remains outside the installed
startup boundary. Canonical and bundled engine bytes must continue to match.


The snapshot checks also inventory `mcp/runtime/` and `mcp/runtime/tools/`.
They reject extra files, packages, and directories: an unexpected module beside
`tools/` could otherwise shadow a standard-library import after the server
inserts its runtime path. Normal `__pycache__` directories are ignored; symlinked
caches and files with that name are rejected. Both builder modes refuse extras
without deleting them. Regression tests exercise rejection in both checks and
preserve the normal-cache control. Bytecode caches remain inside the installed
plugin trust boundary; source parity does not attest arbitrary cache contents.
