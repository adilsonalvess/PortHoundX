"""
diagnosis_map.py
----------------
Knowledge base for PortHoundX troubleshooting.

This module maps well-known ports → services, likely causes, and actionable fixes.
It can be used by both CLI and GUI layers to produce human-readable guidance
and JSON outputs.

Usage (example):
    from diagnosis_map import get_service_name, build_diagnosis

    service = get_service_name(22)  # "SSH"
    diag = build_diagnosis(port=22, status="closed", cloud="AWS")
    print(diag["possible_causes"])
    print(diag["suggested_fixes"])
"""

from typing import Dict, List, Optional

# ------------------------------
# Port → Service mapping
# ------------------------------
PORT_SERVICES: Dict[int, str] = {
    20:  "FTP-Data",
    21:  "FTP",
    22:  "SSH",
    23:  "Telnet",
    25:  "SMTP",
    53:  "DNS",
    80:  "HTTP",
    110: "POP3",
    123: "NTP",
    143: "IMAP",
    161: "SNMP",
    389: "LDAP",
    443: "HTTPS",
    445: "SMB",
    465: "SMTPS",
    587: "Submission/SMTP",
    631: "IPP",
    636: "LDAPS",
    873: "rsync",
    993: "IMAPS",
    995: "POP3S",
    1433: "MSSQL",
    1521: "Oracle DB",
    2049: "NFS",
    2379: "etcd",
    2380: "etcd-peer",
    27017: "MongoDB",
    3000: "App/Dev (Grafana etc.)",
    3306: "MySQL",
    3389: "RDP",
    4430: "Custom HTTPS",
    5000: "App/Dev",
    5432: "PostgreSQL",
    5601: "Kibana",
    5672: "RabbitMQ (AMQP)",
    5900: "VNC",
    6379: "Redis",
    6443: "Kubernetes API",
    7001: "WebLogic Admin",
    8000: "App/Dev",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
    8888: "Jupyter/Dev",
    9000: "MinIO/S3/Dev",
    9092: "Kafka",
    9093: "Kafka (SSL/SASL)",
    9200: "Elasticsearch",
    9300: "Elasticsearch Transport",
}

# ------------------------------
# Service-specific diagnosis DB
# For each service we define:
#  - causes_open: port open but app not responding / auth fail
#  - causes_closed: TCP refused
#  - causes_filtered: timeout/filtered
#  - fixes (generic)
# ------------------------------
DIAGNOSIS: Dict[int, Dict[str, List[str]]] = {
    22: {  # SSH
        "causes_open": [
            "Authentication failure (wrong key/user, missing authorized_keys).",
            "sshd running but bound to wrong interface/port.",
            "Host key or cipher/algorithm mismatch.",
            "PAM/account restrictions or AllowUsers/AllowGroups deny."
        ],
        "causes_closed": [
            "sshd not running or crashed.",
            "Local firewall rejects connections."
        ],
        "causes_filtered": [
            "Network firewall/ACL/Security Group blocks SSH.",
            "DDoS/IPS/Geo-IP filtering dropping SYN packets."
        ],
        "fixes": [
            "Start/restart sshd: `systemctl restart sshd` (or `service ssh restart`).",
            "Open port 22 in host firewall and cloud SG/ACL.",
            "Check key perms: `chmod 700 ~/.ssh && chmod 600 ~/.ssh/*`.",
            "Use verbose client: `ssh -vvv user@host` to inspect handshake."
        ],
    },
    80: {  # HTTP
        "causes_open": [
            "Web server up but app crashed (5xx).",
            "vHost/DNS misroute leads to default site.",
            "LB health checks failing upstream."
        ],
        "causes_closed": [
            "HTTP server not running (nginx/apache).",
            "Service bound to localhost only."
        ],
        "causes_filtered": [
            "Firewall/SG blocking inbound 80.",
            "WAF/CloudArmor/IPS drop."
        ],
        "fixes": [
            "Start nginx/apache; check `systemctl status nginx/apache2`.",
            "Validate vHost/DNS points to correct backend.",
            "Open port 80 in firewall/SG and verify LB target health."
        ],
    },
    443: {  # HTTPS
        "causes_open": [
            "TLS handshake errors (SNI mismatch, weak ciphers).",
            "Expired/invalid certificate.",
            "Backend 5xx behind LB."
        ],
        "causes_closed": [
            "HTTPS service not running or bound incorrectly.",
        ],
        "causes_filtered": [
            "Firewall/SG or WAF blocking 443.",
        ],
        "fixes": [
            "Check cert chain: `openssl s_client -connect host:443 -servername host`.",
            "Renew/replace certificate; confirm SNI/vHost config.",
            "Open 443 in firewall/SG; verify LB health checks."
        ],
    },
    53: {  # DNS (TCP here; UDP issues are similar)
        "causes_open": [
            "DNS queries refused (recursion disabled or ACL).",
            "Authoritative zones misconfigured."
        ],
        "causes_closed": [
            "named/CoreDNS/dnsmasq not running.",
            "Listening only on loopback."
        ],
        "causes_filtered": [
            "UDP/TCP 53 blocked by firewall/ACL.",
        ],
        "fixes": [
            "Restart DNS service; verify `listen-on` and ACLs.",
            "Open UDP/TCP 53; test with `dig @IP example.com`.",
            "Enable VPC DNS/resolver where applicable."
        ],
    },
    3306: {  # MySQL
        "causes_open": [
            "Authentication failure or insufficient grants.",
            "`bind-address` restricts remote access.",
            "SSL mode mismatch (client vs server)."
        ],
        "causes_closed": [
            "mysqld not running.",
        ],
        "causes_filtered": [
            "Firewall/SG/NACL blocking 3306.",
        ],
        "fixes": [
            "Start MySQL; `systemctl status mysql`.",
            "Set `bind-address=0.0.0.0` and restart.",
            "Grant remote access: `GRANT ... TO 'user'@'%'`.",
            "Open port 3306 in firewall/SG."
        ],
    },
    5432: {  # PostgreSQL
        "causes_open": [
            "`pg_hba.conf` missing client rule.",
            "`sslmode` mismatch.",
            "DB max_connections exhausted."
        ],
        "causes_closed": [
            "postgres not running/bound.",
        ],
        "causes_filtered": [
            "Firewall/SG block.",
        ],
        "fixes": [
            "Update `listen_addresses='*'` in postgresql.conf.",
            "Add client in `pg_hba.conf` (host/all/method).",
            "Open 5432; restart service."
        ],
    },
    27017: {  # MongoDB
        "causes_open": [
            "Auth required but missing credentials.",
            "`bindIp` restricts remote access.",
            "IP not whitelisted (Atlas)."
        ],
        "causes_closed": [
            "mongod not running/bound.",
        ],
        "causes_filtered": [
            "Firewall/SG block.",
        ],
        "fixes": [
            "Set `bindIp: 0.0.0.0` in mongod.conf; restart.",
            "Add client IP to Atlas IP Access List.",
            "Open 27017; use proper Mongo URI with user/pass and optional TLS."
        ],
    },
    6379: {  # Redis
        "causes_open": [
            "`requirepass` enabled; client missing password.",
            "Protected-mode on; remote blocked.",
        ],
        "causes_closed": [
            "redis-server not running.",
        ],
        "causes_filtered": [
            "Firewall/SG block.",
        ],
        "fixes": [
            "Set `bind 0.0.0.0` and auth in redis.conf.",
            "Use `redis-cli -a <password>` or TLS as required.",
            "Open 6379 or prefer private networking."
        ],
    },
    9092: {  # Kafka
        "causes_open": [
            "`advertised.listeners` not reachable from client.",
            "SASL/TLS mismatch.",
            "Broker up but ZK/Controller issues."
        ],
        "causes_closed": [
            "Broker not running.",
        ],
        "causes_filtered": [
            "Firewall/SG block or LB misconfig.",
        ],
        "fixes": [
            "Fix `advertised.listeners` to routable host/IP.",
            "Align SASL_SSL config (mechanism, truststore).",
            "Open 9092/9093; verify cluster health."
        ],
    },
    25: {  # SMTP
        "causes_open": [
            "Auth/TLS misconfig (STARTTLS vs SMTPS).",
            "ISP/Cloud blocks outbound 25."
        ],
        "causes_closed": [
            "MTA not running.",
        ],
        "causes_filtered": [
            "Firewall/Cloud provider blocks 25 (common).",
        ],
        "fixes": [
            "Use 587 + STARTTLS where possible.",
            "For AWS request port-25 removal; otherwise use SES/SMTP relay.",
            "Open 25/465/587 as applicable; restart postfix/exim."
        ],
    },
    3389: {  # RDP
        "causes_open": [
            "NLA/auth policy mismatch.",
            "Session caps/max sessions."
        ],
        "causes_closed": [
            "TermService not running.",
        ],
        "causes_filtered": [
            "Firewall/SG/NACL block; IPS filtering.",
        ],
        "fixes": [
            "Enable RDP; ensure NLA policy matches client.",
            "Open 3389; confirm Windows Firewall inbound rule.",
            "Consider VPN/Bastion for public access."
        ],
    },
    445: {  # SMB
        "causes_open": [
            "Auth/NTLM issues; share permissions.",
            "SMB version mismatch (SMB1 disabled)."
        ],
        "causes_closed": [
            "SMB service not running.",
        ],
        "causes_filtered": [
            "Firewall/SG block; IDS drop.",
        ],
        "fixes": [
            "Open 445; verify share and NTFS permissions.",
            "Align SMB protocol versions; prefer SMBv2/v3."
        ],
    },
    123: {  # NTP
        "causes_open": [
            "Server denies mode 6/7 queries; normal.",
            "Stratum/peering issues."
        ],
        "causes_closed": [
            "ntpd/chronyd not running.",
        ],
        "causes_filtered": [
            "UDP 123 blocked.",
        ],
        "fixes": [
            "Open UDP 123; use `chronyc sources`. ",
            "Prefer internal NTP or cloud time service."
        ],
    },
    21: {  # FTP
        "causes_open": [
            "Passive ports not opened (data channel fails).",
            "Auth policy/cleartext vs TLS FTPS mismatch."
        ],
        "causes_closed": [
            "vsftpd/proftpd not running.",
        ],
        "causes_filtered": [
            "Firewall/SG block (control/data).",
        ],
        "fixes": [
            "Open control (21) + passive port range.",
            "Enable FTPS/TLS; configure PASV range in server and firewall."
        ],
    },
    9200: {  # Elasticsearch
        "causes_open": [
            "Security plugin/auth required.",
            "Node bound to loopback; HTTP reachable locally only."
        ],
        "causes_closed": [
            "Elasticsearch not running.",
        ],
        "causes_filtered": [
            "Firewall/SG block.",
        ],
        "fixes": [
            "Bind to 0.0.0.0 for remote (with auth!).",
            "Enable auth (x-pack), avoid exposing 9200 publicly.",
            "Open 9200 only to trusted networks."
        ],
    },
    5672: {  # RabbitMQ (AMQP)
        "causes_open": [
            "Auth/vhost permissions missing.",
            "TLS required but client plain."
        ],
        "causes_closed": [
            "RabbitMQ not running or listener off.",
        ],
        "causes_filtered": [
            "Firewall/SG block.",
        ],
        "fixes": [
            "Open 5672 (and 15672 for UI if needed).",
            "Create user/vhost; align TLS settings."
        ],
    },
    6443: {  # Kubernetes API
        "causes_open": [
            "Client cert/token missing or RBAC denies.",
            "Cluster API behind LB with health/routing issues."
        ],
        "causes_closed": [
            "kube-apiserver not reachable/not running.",
        ],
        "causes_filtered": [
            "Firewall/NetworkPolicy/LB blocks.",
        ],
        "fixes": [
            "Use correct kubeconfig/context; check RBAC.",
            "Open 6443; verify control-plane health and LB target status."
        ],
    },
}

# ------------------------------
# Cloud-specific hints
# ------------------------------
CLOUD_HINTS: Dict[str, Dict[str, List[str]]] = {
    "AWS": {
        "causes": [
            "Security Group or NACL denies inbound/outbound.",
            "Elastic Load Balancer target unhealthy.",
            "VPC DNS hostnames/resolver disabled.",
            "AWS blocks outbound SMTP(25) by default."
        ],
        "fixes": [
            "Check SG inbound/outbound + NACL rules.",
            "Verify ELB/Target Group health checks.",
            "Enable VPC DNS resolution/hostnames if needed.",
            "Use 587/SES or request port 25 unblock."
        ],
    },
    "Azure": {
        "causes": [
            "NSG or Azure Firewall rule denies traffic.",
            "App Gateway/LB probe failing.",
        ],
        "fixes": [
            "Review NSG effective security rules.",
            "Check LB backend pool and health probes."
        ],
    },
    "GCP": {
        "causes": [
            "VPC firewall rule missing/denies ingress.",
            "Cloud Armor policy blocking.",
            "LB backend service health fails."
        ],
        "fixes": [
            "Add/allow appropriate `ingress` rule for port.",
            "Review Cloud Armor security policy logs.",
            "Check backend health; service named ports."
        ],
    },
    "Kubernetes": {
        "causes": [
            "NetworkPolicy denies pod ingress/egress.",
            "Service has no Endpoints (selector mismatch).",
            "CoreDNS misconfig or CrashLoopBackOff."
        ],
        "fixes": [
            "Inspect NetworkPolicies; temporarily allow-all to test.",
            "Check `kubectl get endpoints` for backing pods.",
            "Check CoreDNS logs and `kubectl -n kube-system get pods`."
        ],
    },
}

# ------------------------------
# Helpers
# ------------------------------

def get_service_name(port: int) -> str:
    """Return a friendly service name for a port."""
    return PORT_SERVICES.get(port, "Unknown")

def _status_key(status: str) -> str:
    """Map status → causes key in DIAGNOSIS."""
    s = status.lower()
    if s.startswith("open"):
        return "causes_open"
    if "refused" in s or s == "closed":
        return "causes_closed"
    if "filtered" in s or "timeout" in s or s == "filtered":
        return "causes_filtered"
    # fallback if ambiguous
    return "causes_filtered"

def build_diagnosis(
    port: int,
    status: str,
    cloud: Optional[str] = None,
    extra_signals: Optional[Dict[str, bool]] = None,
) -> Dict[str, List[str]]:
    """
    Build a diagnosis payload for a given port/status, optionally enriching with cloud hints.

    Parameters
    ----------
    port : int
        The TCP port observed.
    status : str
        One of: "open", "closed", "filtered (timeout)", "closed (refused)", ...
    cloud : Optional[str]
        Cloud context: "AWS", "Azure", "GCP", "Kubernetes", or None.
    extra_signals : Optional[Dict[str, bool]]
        Optional signals your scanner collects, e.g.:
            {"ping_ok": True, "dns_ok": True, "is_private": False}

    Returns
    -------
    dict with keys:
        - service
        - possible_causes
        - suggested_fixes
    """
    service = get_service_name(port)
    base = DIAGNOSIS.get(port, {
        "causes_open": [
            "Application accepts TCP but higher-layer protocol fails (auth/protocol)."
        ],
        "causes_closed": [
            "No process listening; service down or misbound."
        ],
        "causes_filtered": [
            "Firewall/ACL silently dropping packets."
        ],
        "fixes": [
            "Start the service; bind to correct interface/port.",
            "Open the port in host firewall and perimeter controls.",
            "Validate app/protocol configuration."
        ],
    })

    key = _status_key(status)
    possible_causes = list(base.get(key, []))
    suggested_fixes = list(base.get("fixes", []))

    # Enrich with cloud hints if provided
    if cloud and cloud in CLOUD_HINTS:
        possible_causes += CLOUD_HINTS[cloud]["causes"]
        suggested_fixes += CLOUD_HINTS[cloud]["fixes"]

    # Optional heuristics based on signals
    signals = extra_signals or {}
    ping_ok = signals.get("ping_ok")
    if ping_ok is False and key != "causes_closed":
        # If host not pingable, prioritize reachability/routing
        possible_causes.insert(0, "Host not reachable (ICMP fails): routing/VPN/ACL issue.")
        suggested_fixes.insert(0, "Check routing/VPN/peering and ICMP blocks; verify the correct IP.")

    dns_ok = signals.get("dns_ok")
    if dns_ok is False:
        possible_causes.insert(0, "DNS resolution failed or wrong record.")
        suggested_fixes.insert(0, "Fix DNS record or use direct IP; verify /etc/resolv.conf or cloud DNS.")

    is_private = signals.get("is_private")
    if is_private is True:
        suggested_fixes.append("Use VPN/DirectConnect/Peering or Bastion to reach private IP.")

    return {
        "service": service,
        "possible_causes": dedupe_preserve_order(possible_causes),
        "suggested_fixes": dedupe_preserve_order(suggested_fixes),
    }

def dedupe_preserve_order(items: List[str]) -> List[str]:
    """De-duplicate while preserving order."""
    seen = set()
    out = []
    for x in items:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


# ------------------------------
# Self-test / Demonstration
# ------------------------------
if __name__ == "__main__":
    samples = [
        (22, "closed", "AWS", {"ping_ok": True, "dns_ok": True, "is_private": False}),
        (3306, "filtered (timeout)", "GCP", {"ping_ok": True, "dns_ok": True}),
        (443, "open", "Azure", {"ping_ok": True, "dns_ok": True}),
        (9092, "closed (refused)", None, {"ping_ok": True, "dns_ok": True}),
        (6443, "filtered", "Kubernetes", {"ping_ok": False, "dns_ok": True}),
    ]
    for port, status, cloud, signals in samples:
        d = build_diagnosis(port, status, cloud, signals)
        print(f"\nPort {port} ({d['service']}), Status: {status}, Cloud: {cloud or 'N/A'}")
        print("Possible Causes:")
        for c in d["possible_causes"]:
            print(" -", c)
        print("Suggested Fixes:")
        for f in d["suggested_fixes"]:
            print(" -", f)
