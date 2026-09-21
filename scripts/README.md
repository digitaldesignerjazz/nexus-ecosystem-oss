# Host scripts

Default root: `$NEXUS_ROOT` or `$HOME/nexus`.

- `start_nexus_tailscale.sh` — prepare | status | login | up | down | pulse
- `start_nexus_funnel.sh` — status | on <port> | off | allow-check
- `start_nexus_independent_mesh.sh` — plane helper (needs `independent_mesh.py` beside it)

Never commit `tailscale.env`.
