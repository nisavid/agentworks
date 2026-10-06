# ADR 0023: Adopt Agentworks Identity

Status: Accepted

## Context

Agentworks is the accepted project and repository name in
[#216](https://github.com/nisavid/agentworks/issues/216). The project's direction
is a harness-refit workshop where each Agent creates or equips the equipment
it needs for its assigned task, domain, and context.

## Decision

Use **Agentworks** as the formal project name and **the Works** as its
unambiguous shorthand. Use `nisavid/agentworks` as the canonical repository and
tracker identity. Current documentation, metadata, examples, and validation
labels use this identity.

This decision supersedes Agent Armory as the current project name. Earlier
ADRs, source anchors, dated plans, review reports, and closeout records remain
historical evidence. The Forge retains its established meaning. This identity
increment does not implement Store, Bench, other domain architecture, or new
self-outfitting capabilities; those contracts remain in #216.

## Active Identifiers

Use Agentworks names for current producers and consumers:

- the `agentworks` marketplace key and `agent-equipment-config@agentworks`
  installed-plugin identity;
- `AGENTWORKS_ROOT` for explicit launcher discovery;
- `agentworks.equipment-stock.v1`,
  `agentworks.config.authoring-plan.v1`, and `x-agentworks`;
- `agentworks_integrity.validation_result.v1`, the `agentworks_integrity`
  validation boundary, and `tools/validate_agentworks_integrity.py`;
- Agentworks example plugin identifiers, Config namespace keys, and current
  artwork;
- the `Works role mapping` evaluation-record field label.

Current source accepts these identifiers without old-name aliases. The
launcher checks a valid `AGENTWORKS_ROOT`, then the current directory and its
parents for the trusted checkout shape. It does not use or forward the old
root environment variable. Obsolete marketplace markers, stock schemas, and
authoring-plan schemas are refused.

Update consumer configuration and prepare new plans through the owning
workflow. A schema-name change does not requalify an old plan or receipt.
Historical records, recorded source anchors, and archived assets retain their
names; they are evidence, not active compatibility interfaces.

## Consequences

Do not reuse `nisavid/agent-armory`: GitHub's repository and Git transport
redirects depend on the old name remaining unused. GitHub Pages URLs and hosted
Action references need separate migration rather than relying on those
redirects, as described in
[GitHub's rename guidance](https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository).

Repository redirects do not requalify plans, receipts, or response checks
bound to canonical repository coordinates. The unfinished discussion-comment
transport in [#215](https://github.com/nisavid/agentworks/issues/215) checks
requested and returned repository names exactly. Requests bound to
`nisavid/agent-armory` should therefore fail closed when GitHub returns
`nisavid/agentworks`; that is a source-based inference, not an executed
transport result. Its owning workflow must requalify the canonical target
before integration or resumed writes. Preserve existing plans and receipts as
historical evidence, reconcile unknown outcomes, and prepare new requests
through the owning workflow rather than rewriting evidence or blindly
replaying a write.

Existing checkouts and worktrees can keep their directory names while using
the canonical remote. Moving the stable checkout and repointing saved harness
projects requires preserving active worktree registration and updating the
harness's project binding together.

External consumers remain responsible for updating their canonical repository
references. Issue #216 tracks that rollout and the broader domain changes;
this decision does not rename unrelated repositories or publish new packages.

## Known Consumer Follow-Ups

The bounded reference inventory found these external surfaces. Their owning
repositories carry the changes; the identity increment leaves them intact.

| Repository | Surface | Disposition |
| --- | --- | --- |
| `nisavid/dotfiles` | `home/dot_agents/skills/triaging-agent-armory-issues/SKILL.md` and `PRESSURE-SCENARIOS.md` | Rename the installed skill and update current project mentions, canonical tracker commands, and trigger text through its owning workflow. |
| `nisavid/fork-ops` | `CONTEXT.md` and `specs/fork-ops-foundation/interface-decision-record.md` | Update current generic-equipment and Issue Ops references to Agentworks. |
| `nisavid/fork-ops` | `docs/agents/fork-ops-32-equipment-migration-case-study.md` | Review current interpretation text separately from the recorded migration evidence. |
| `nisavid/provingkit` | `CONTEXT.md` | Already uses Agentworks; the old project name appears as vocabulary to avoid. |
| `nisavid/provingkit` | `docs/superpowers/research/2026-09-17-mergecraft-relation-inventory.md` | Retain the dated inventory as historical evidence and rely on the repository redirect. |

Saved harness projects and existing checkout directory names also need a
coordinated local migration. The canonical remote can change independently.
This inventory does not claim to cover consumers outside the inspected
repositories.
