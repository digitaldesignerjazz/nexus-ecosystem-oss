# Nexus Activation Protocol (public sketch)

Status: written for the public field. Not a live deployment log.

1. Resolve `NEXUS_ROOT` on the host (`$HOME/nexus` is the usual host root).
2. Required: `python3`. Optional: `tailscale`, `netbird`, `yggdrasil`, `docker`, `rustc`.
3. Bring up the independent mesh plane. Overlay absence must not take the plane down.
4. Attach Tailscale only when the binary and privileges exist.
5. NetBird secondary. Yggdrasil companion only.
6. Wizard Q default is `--dry-run`. No live QNET node is claimed here.
7. Prototypes last, and only with a mesh pulse (independent pulse counts).

Never log auth keys, setup keys, or Kyber material.
