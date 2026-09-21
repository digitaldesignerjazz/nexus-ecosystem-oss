#!/usr/bin/env python3
"""Nexus independent mesh control plane (public OSS helper).

Identity, peers and pulse live under NEXUS_ROOT. Overlays are optional.
No auth keys are written.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import socket
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

NEXUS_ROOT = Path(os.environ.get("NEXUS_ROOT", str(Path.home() / "nexus")))
MESH_DIR = NEXUS_ROOT / "mesh"
CONFIG_DIR = NEXUS_ROOT / "config"
IDENTITY_FILE = MESH_DIR / "identity.json"
PEERS_FILE = MESH_DIR / "peers.json"
PULSE_FILE = MESH_DIR / "pulse.json"
STATE_FILE = MESH_DIR / "runtime_state.md"


def utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ensure_dirs() -> None:
    MESH_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    (NEXUS_ROOT / "logs").mkdir(parents=True, exist_ok=True)


def load_json(path: Path, default: Any) -> Any:
    if not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def dump_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def which(name: str) -> bool:
    return any(
        (Path(folder) / name).is_file() and os.access(Path(folder) / name, os.X_OK)
        for folder in os.environ.get("PATH", "").split(os.pathsep)
    )


def transport_board() -> dict[str, str]:
    return {
        "tailscale": "present" if which("tailscale") else "missing",
        "netbird": "present" if which("netbird") else "missing",
        "yggdrasil": "present" if which("yggdrasil") else "missing",
    }


def make_identity() -> dict[str, Any]:
    host = socket.gethostname()
    seed = hashlib.sha256(f"nexus-independent|{host}|{os.environ.get('USER', 'nexus')}".encode()).hexdigest()
    fp = hashlib.sha256(f"fp|{seed}".encode()).hexdigest()
    return {
        "schema": "nexus.mesh.identity.v1",
        "plane": "independent",
        "node_id": f"nxm-{seed[:16]}",
        "fingerprint": f"independent:{fp}",
        "hostname": host,
        "created_at": utcnow(),
        "sovereign": True,
        "vendor_control_plane": "none",
        "preferred_transport": "none",
    }


def load_or_create_identity() -> dict[str, Any]:
    existing = load_json(IDENTITY_FILE, None)
    if isinstance(existing, dict) and existing.get("node_id") and existing.get("fingerprint"):
        existing["last_seen"] = utcnow()
        dump_json(IDENTITY_FILE, existing)
        return existing
    ident = make_identity()
    dump_json(IDENTITY_FILE, ident)
    return ident


def load_peers(ident: dict[str, Any]) -> dict[str, Any]:
    peers = load_json(PEERS_FILE, None)
    self_peer = {
        "peer_id": ident["node_id"],
        "fingerprint": ident["fingerprint"],
        "role": "self",
        "transport": "local-control-plane",
        "status": "online",
        "introduced_at": ident.get("created_at", utcnow()),
    }
    if not isinstance(peers, dict) or not isinstance(peers.get("peers"), list):
        peers = {"schema": "nexus.mesh.peers.v1", "plane": "independent", "peers": [self_peer]}
    ids = {p.get("peer_id") for p in peers["peers"] if isinstance(p, dict)}
    if ident["node_id"] not in ids:
        peers["peers"].insert(0, self_peer)
    peers["updated_at"] = utcnow()
    dump_json(PEERS_FILE, peers)
    return peers


def pulse_now(ident: dict[str, Any], peers: dict[str, Any]) -> dict[str, Any]:
    board = transport_board()
    pulse = {
        "schema": "nexus.mesh.pulse.v1",
        "plane": "independent",
        "timestamp": utcnow(),
        "unix": int(time.time()),
        "node_id": ident["node_id"],
        "fingerprint": ident["fingerprint"],
        "status": "online",
        "mode": "sovereign-local",
        "peer_count": len(peers.get("peers") or []),
        "transports_present": [n for n, s in board.items() if s == "present"],
        "transports_missing": [n for n, s in board.items() if s == "missing"],
        "blocked_on_vendor": False,
    }
    dump_json(PULSE_FILE, pulse)
    lines = [
        "# Nexus Mesh Runtime State",
        f"- timestamp: {pulse['timestamp']}",
        f"- host: {socket.gethostname()}",
        "- plane: independent",
        f"- node_id: {ident['node_id']}",
        f"- fingerprint: {ident['fingerprint']}",
        f"- pulse_status: {pulse['status']}",
        f"- tailscale_transport: {board['tailscale']}",
        f"- netbird_transport: {board['netbird']}",
        f"- yggdrasil_transport: {board['yggdrasil']}",
        "- secrets_logged: no",
        "",
    ]
    STATE_FILE.write_text("\n".join(lines), encoding="utf-8")
    return pulse


def cmd_up() -> int:
    ensure_dirs()
    ident = load_or_create_identity()
    peers = load_peers(ident)
    pulse_now(ident, peers)
    print(f"independent mesh up: {ident['node_id']} status=online vendor_control=none")
    return 0


def cmd_down() -> int:
    ensure_dirs()
    ident = load_or_create_identity()
    peers = load_peers(ident)
    pulse = pulse_now(ident, peers)
    pulse["status"] = "standby"
    dump_json(PULSE_FILE, pulse)
    print(f"independent mesh standby: {ident['node_id']} (identity kept)")
    return 0


def cmd_status() -> int:
    ensure_dirs()
    ident = load_or_create_identity()
    peers = load_peers(ident)
    pulse = load_json(PULSE_FILE, {}) or pulse_now(ident, peers)
    board = transport_board()
    print("=== independent mesh ===")
    print(f"plane=independent")
    print(f"status={pulse.get('status', 'unknown')}")
    print(f"node_id={ident.get('node_id')}")
    print(f"fingerprint={ident.get('fingerprint')}")
    print(f"peers={len(peers.get('peers') or [])}")
    print(f"tailscale={board['tailscale']}")
    print(f"state={STATE_FILE}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Nexus independent mesh control plane")
    parser.add_argument("command", nargs="?", default="status", choices=["status", "prepare", "up", "down", "pulse"])
    args = parser.parse_args()
    if args.command in {"prepare", "up", "pulse"}:
        return cmd_up()
    if args.command == "down":
        return cmd_down()
    return cmd_status()


if __name__ == "__main__":
    raise SystemExit(main())
