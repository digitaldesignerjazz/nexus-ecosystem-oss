# Host scripts

`.sh` files are Bash. Do not run them with `python3`.

```bash
export NEXUS_ROOT="$HOME/nexus"
chmod +x start_nexus_independent_mesh.sh
bash start_nexus_independent_mesh.sh up
# or directly:
python3 independent_mesh.py up
python3 independent_mesh.py status
```

State is written to `$NEXUS_ROOT/mesh/` (default `~/nexus/mesh`), not into this git checkout.
