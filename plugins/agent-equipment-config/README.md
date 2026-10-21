# Agent Equipment Config Codex Plugin

This plugin equips Codex with the Agent Equipment Config routing skill, a
plugin-local MCP launcher, and a guard hook for Config local-write MCP tools.

## Install

The Works repository exposes this plugin through
`.agents/plugins/marketplace.json` as the `agentworks` repo marketplace, displayed
as Agentworks. Codex
installs the source from `./plugins/agent-equipment-config` into its plugin
cache. The installed plugin contains its executable Config runtime snapshot.
The configured Works checkout supplies the working directory for Config data.

Do not copy secrets into plugin files. The MCP config passes through only
`AGENTWORKS_ROOT`. The plugin manifest uses `mcpServers` to point at
`.mcp.json`; the referenced MCP config uses Codex's documented direct MCP
server map.

## MCP Runtime and Data Checkout

The plugin MCP entry runs from the installed plugin root and launches
`./mcp/agent_equipment_config_launcher.py` with Python isolation flags `-I -S`.
The launcher starts the bundled server only when `AGENTWORKS_ROOT` points at a checkout, or when the process
cwd is inside a checkout, containing:

- `tools/agent_equipment_config_mcp_server.py`
- `inventory/equipment.toml`
- `.agents/plugins/marketplace.json`

If neither source contains those Works markers, the launcher exits closed with
install guidance instead of starting an unexpected process.

After discovery, the launcher changes directory to the Works checkout so
relative Config paths resolve against the repository. It executes only the
server and Config engine installed under `mcp/runtime/tools/`, using `-I -S`
to exclude ambient import paths, Python environment settings, and site startup
code. Checkout marker files select a data directory; they do not authorize
checkout Python code. A missing runtime bundle fails closed.

When the canonical Config engine or server changes, refresh the snapshot before
publishing the plugin:

```bash
python3.14 tools/build_agent_equipment_config_plugin.py
python3.14 tools/build_agent_equipment_config_plugin.py --check
```

Repository validation requires byte parity with the canonical sources and rejects
extra entries in both runtime directories. Ordinary `__pycache__` directories
are ignored; symlinks and files with that name are rejected. The builder also
refuses unexpected entries rather than deleting them. Update
or reinstall the plugin to adopt a new runtime snapshot; switching branches or
editing a checkout does not change an already installed plugin's code.

## Hook Trust

`hooks/hooks.json` registers a `PreToolUse` command hook through
`python3.14 -I -S "${PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/hooks/config_write_guard.py"`.
The isolation flags exclude ambient import paths and site startup code. The quoted path is safe
for plugin cache paths containing whitespace. The hook ignores unrelated MCP
tools and denies Agent Equipment Config local-write MCP calls unless
`apply_authority = "operator"` is present in the tool input.

Codex hook trust and MCP approval prompts remain host policy surfaces. This
plugin asks Codex to prompt by default and specifically prompt for
`config.apply` and `migrate.config_apply`.

## Validate

Run these checks from the Works checkout:

```bash
python3.14 tools/build_agent_equipment_config_plugin.py --check
python3.14 -m unittest tests.test_agent_equipment_config_codex_plugin
python3.14 tools/validate_agentworks_integrity.py
```

Use the routing skill for Smith, Wielder, and Outfitter workflows; use
`docs/equipment/agent-equipment-config-integration.md` before changing adapter
behavior.
