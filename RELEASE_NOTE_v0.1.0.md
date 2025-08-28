# Release v0.1.0 – PortHoundX

**Release Date:** 2025-08-28  

## 🚀 Overview

PortHoundX v0.1.0 is the **first functional release** of our network diagnostic and troubleshooting tool.  
It combines **CLI and GUI interfaces** to provide engineers and DevOps professionals with a **reasoned insight** into network connectivity, port availability, service detection, and cloud awareness.  

This release focuses on core functionality with a focus on usability and actionable diagnostics.

---

## ✨ Key Features in v0.1.0

- **Dual Interface:** Run diagnostics via **CLI** or **Tkinter GUI**.  
- **Multi-Port Scanning:** Check essential ports like SSH (22), HTTP (80), HTTPS (443), MySQL (3306) and more.  
- **Service Detection:** Identify common services like HTTP, HTTPS, MySQL, MongoDB, Kafka, and more.  
- **Cloud Awareness:** Detect whether the host belongs to **AWS, GCP, Azure, IBM Cloud**.  
- **Reasoned Diagnostics:** Suggest likely causes for failures (e.g., firewall blocks, closed ports, unreachable hosts).  
- **Pretty CLI Output + JSON Export:** Structured outputs for automated or human-readable use.  

---

## 🛠 Installation

```bash
git clone https://github.com/<your-username>/PortHoundX.git
cd PortHoundX
pip install -r requirements.txt
```

---

## 💻 Usage

### CLI Example:

```bash
python src/porthoundx.py --host 8.8.8.8 --ports 22 80 443 --detect-services
```

### GUI Example:

```bash
python src/porthoundx.py --gui
```

- Enter host/IP.  
- Select ports.  
- Enable service detection and/or JSON output (optional).  
- Click **Run Diagnostics**.  

---

## 📊 Sample Output

**CLI Pretty Output:**

```
Host: 8.8.8.8
IP: 8.8.8.8
Private: False
Reachable: ✅ Yes
Ports:
  - 22: ❌ Closed
  - 80: ✅ Open (HTTP Detected)
  - 443: ✅ Open (HTTPS Detected)
Cloud Provider: GCP
```

**JSON Output:**

```json
{
  "host": "8.8.8.8",
  "ip": "8.8.8.8",
  "is_private": false,
  "reachable": true,
  "ports": {
    "22": false,
    "80": true,
    "443": true
  },
  "cloud_provider": "GCP"
}
```

---

## 🔮 Future Scope

- Advanced troubleshooting reasoning with **firewall, ACL, and DNS insights**.  
- Expanded **service detection**: Kafka, Redis, RabbitMQ, ElasticSearch, etc.  
- Extended cloud fingerprinting with **region hints**.  
- Optional **traceroute & latency analysis**.  
- Security-focused features like **TLS/SSL misconfiguration checks**.  

---

## ❤️ Contributions

We welcome **issues, feature suggestions, and pull requests**!  
PortHoundX is designed to grow as a **reasoning-based network diagnostics tool** for engineers, and your contributions are invaluable.  

---

**PortHoundX isn’t just a port scanner — it’s your network reasoning assistant.**
