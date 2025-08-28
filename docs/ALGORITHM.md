
# PortHoundX - Algorithm & Design

## Overview
PortHoundX is a multi-purpose diagnostic tool for **port scanning, service detection, and cloud provider awareness**.  
It supports both **CLI** and **GUI** modes for usability.

---

## High-Level Algorithm

### 1. Input Phase
- Accepts a **host** (IP or DNS name).
- Accepts a list of **ports** to scan (default: 22, 80, 443).
- Options:
  - JSON output (`--json`).
  - Service detection (`--detect-services`).
  - GUI mode (`--gui`).

### 2. Resolution Phase
- Resolve hostname → IP (`socket.gethostbyname`).
- Check if the IP is **private or public** (`ipaddress` library).

### 3. Connectivity Phase
- **Ping Test** → Check if host is reachable.
- **Port Scan** → For each port:
  - Try connecting via `socket.create_connection`.
  - Mark port as open or closed.

### 4. Service Detection (Optional)
- If a port is open, map it to a known service (e.g., 22 → SSH, 80 → HTTP, 443 → HTTPS, etc.).

### 5. Cloud Detection
- Query `ipinfo.io` API to detect cloud provider (AWS, GCP, Azure, IBM, Other).

### 6. Output Phase
- If JSON enabled → structured machine-readable output.
- Otherwise → human-readable CLI with colors (`colorama`).
- GUI mode → Tkinter window with inputs & scrollable results.

---

## Files & Roles

### `porthoundx.py`
- Main entrypoint.
- Handles:
  - Argument parsing (CLI).
  - GUI launch.
  - Orchestrates functions from `utils.py`.

### `utils.py`
- Helper functions:
  - `resolve_host()` → DNS resolution.
  - `is_private_ip()` → Check if IP is private.
  - `check_ping()` → Host reachability.
  - `check_port()` → TCP port scanning.
  - `detect_service()` → Service mapping.
  - `detect_cloud()` → Cloud provider detection.
  - `pretty_format()` → CLI color formatting.

---

## Flowchart (Simplified)

```
 Start
   |
   v
 Get Input (host, ports, options)
   |
   v
 Resolve Host → IP → Private/Public
   |
   v
 Ping Host → Reachable?
   |
   v
 For each port:
     Open? → (Yes) → Detect Service
   |
   v
 Detect Cloud Provider
   |
   v
 Format Output → CLI / JSON / GUI
   |
   v
 End
```

---

## Future Extensions
- Async scanning for speed (e.g., `asyncio`).
- OS fingerprinting.
- Export results to CSV/DB.
- Plugin system for new protocols.
