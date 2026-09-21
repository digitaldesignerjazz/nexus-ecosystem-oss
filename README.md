# Nexus Ecosystem (public OSS field)

Public orchestration sketches for the Nexus stack: independent mesh plane, optional Tailscale transport, proposed QNET / Wizard Q runes.

This is **not** a live chain, not a treasury, and not the private swarm runtime.

| Field | Repo |
| --- | --- |
| This public ecosystem | [`digitaldesignerjazz/nexus-ecosystem-oss`](https://github.com/digitaldesignerjazz/nexus-ecosystem-oss) |
| Public specs / contribution | [`digitaldesignerjazz/Aether`](https://github.com/digitaldesignerjazz/Aether) |
| Public skill excerpts | [`digitaldesignerjazz/nexus-skills`](https://github.com/digitaldesignerjazz/nexus-skills) |
| Public hub | [`digitaldesignerjazz/nexus`](https://github.com/digitaldesignerjazz/nexus) |
| Private runtime | `nexus-ecosystem` (stays private) |

Operator public identity: Esslinger & Co. / `digitaldesignerjazz`.  
Wizard Q opcode spec is **v0.1 Proposed**.

## Plane vs transport

- The mesh *plane* is local-sovereign (`NEXUS_MESH=independent`). Identity and pulse live under `$NEXUS_ROOT/mesh/`.
- Tailscale is the preferred *transport* when the binary exists on a privileged host.
- NetBird is a supported secondary transport. Yggdrasil is a companion overlay, never the identity.
- If every overlay binary is missing, the plane still stays up.

## Quick start (Linux host)

```bash
export NEXUS_ROOT="$HOME/nexus"
mkdir -p "$NEXUS_ROOT"/{config,mesh,logs,scripts}
cp config/tailscale.env.example "$NEXUS_ROOT/config/"
# copy scripts/ into $NEXUS_ROOT/scripts and chmod +x

# transport (needs tailscale + privileges)
bash scripts/start_nexus_tailscale.sh prepare
# edit $NEXUS_ROOT/config/tailscale.env locally — never commit it
sudo bash scripts/start_nexus_tailscale.sh login
```

Funnel is public HTTPS to a single local port. Serve stays inside the tailnet. Do not Funnel home directories or state trees.

## Do not publish

- `tailscale.env`, setup keys, wallet seeds, Kyber material
- skilllogin files under `ai_agents/`
- mempool, receipts, local ledgers with live parameters
- private correspondence or household internals

## License

Apache-2.0. See `LICENSE`.
