# Nexus Activation Protocol

Status: **active**  
Version: **0.1**  
Datum: 2026-09-24  
Owner: Orchestrator (control plane)  
Spec-Bindung: Nexus domain map + Wizard Q v0.1 Proposed  
Klassifikation: Öffentliches Betriebsprotokoll — keine Secrets, kein skilllogin, kein Live-Claim für QNET

Public field: `digitaldesignerjazz/nexus-ecosystem-oss`  
Private runtime sibling: `digitaldesignerjazz/nexus-ecosystem`  
Public lineage sibling: `digitaldesignerjazz/Aether`

`activate` erwartet diese Datei unter `$NEXUS_ROOT/ACTIVATION_PROTOCOL.md` auf dem laufenden Knoten.

---

## 0. Satz

1. Das Mesh ist eine eigene Ebene. Overlay-Anbieter besitzen die Identität nicht.
2. Startreihenfolge gilt, solange der Operator keine andere nennt.
3. Optionale Teile (Tailscale, NetBird, Yggdrasil, Docker, Tor, I2P, rustc) dürfen fehlen. Der Stack fällt nicht.
4. Wizard Q bleibt `--dry-run`, bis lokaler State ausdrücklich `live` sagt.
5. Prototypen starten nur bei lebendem Mesh-Puls. Unabhängiger Puls zählt.
6. Keine Auth-Keys, Setup-Keys, Kyber-Materialien oder `*.env`-Körper in diesem Dokument.
7. Drei Wurzeln sind nicht dasselbe Verzeichnis. Erst auflösen, dann starten.

---

## 1. Path roots

Resolve `NEXUS_ROOT` before any start. Typical layout:

- Scripts live with the Nexus skill tree
- Runtime state lives under `$NEXUS_ROOT` (`mesh/`, `config/`, `logs/`)
- `QNET_ROOT` stays unset while no node is live

```bash
export NEXUS_ROOT="${NEXUS_ROOT:-$PWD/artifacts/nexus}"
export NEXUS_MESH="${NEXUS_MESH:-independent}"
mkdir -p "$NEXUS_ROOT"/{mesh,config,logs,mempool,receipts,qnet}
```

---

## 2. Startordnung

1. Root auflösen
2. Prerequisites (`python3` Pflicht; docker/rust optional)
3. Independent mesh plane (`prepare` → `up` → `pulse`)
4. Tailscale transport if binary present (preferred overlay dataplane)
5. NetBird optional secondary transport
6. Yggdrasil companion only — never identity replacement
7. Swarm login only as needed
8. Wizard Q dry-run until state says live
9. Prototypes last, only with mesh pulse

```bash
NEXUS_MESH=independent bash start_nexus_mesh.sh prepare
NEXUS_MESH=independent bash start_nexus_mesh.sh up
NEXUS_MESH=independent bash start_nexus_mesh.sh pulse
bash nexus_orchestrator.sh full-report
bash nexus_orchestrator.sh activate
```

---

## 3. Fingerprint-Regel

- Overlay lebend (Tailscale oder NetBird) → diesen Fingerprint in `mesh/runtime_state.md` festhalten
- sonst → `independent:<hex>` ist gültiger Wizard-Q-Anker

Wizard Q spec v0.1 is **Proposed**. No live public chain, treasury or activated opcode set is claimed here.

---

## 4. Activate-Semantik

`activate` loads this protocol, runs phase checks, names gaps, and does not invent a live overlay or a live chain.

Activate is not key import and not rune settle.

---

## 5. Verbotene Inhalte

- Overlay auth/setup keys
- Wallet seeds and Kyber secrets
- Private swarm state and correspondence
- Household coordinates and non-public personal names
