import socket
import json
import ipaddress
import subprocess


# ---------------- Networking Utilities ----------------
def resolve_host(host):
    """Resolve hostname to IP address"""
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        return "Unresolved"


def is_private_ip(ip):
    """Check if IP is private"""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        return False


def is_reachable(ip):
    """Check reachability using ping"""
    try:
        output = subprocess.run(
            ["ping", "-n", "1", ip] if socket.gethostname().endswith("windows") else ["ping", "-c", "1", ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return output.returncode == 0
    except Exception:
        return False


def scan_port(ip, port, timeout=1.0):
    """Check if a port is open"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            return sock.connect_ex((ip, port)) == 0
    except Exception:
        return False


def detect_service(ip, port):
    """Detect simple service type by port number"""
    common_services = {
        22: "SSH",
        80: "HTTP",
        443: "HTTPS",
        3306: "MySQL",
        5432: "PostgreSQL",
        6379: "Redis",
    }
    return common_services.get(port, "Unknown Service")


# ---------------- Cloud Provider Detection ----------------
def detect_cloud_provider(ip):
    """Basic cloud provider detection (placeholder rules)"""
    if ip.startswith("35.") or ip.startswith("34."):
        return "GCP"
    elif ip.startswith("13.") or ip.startswith("52.") or ip.startswith("3."):
        return "AWS"
    elif ip.startswith("20.") or ip.startswith("40."):
        return "Azure"
    else:
        return "Unknown"


# ---------------- Output Formatting ----------------
def to_json(results):
    return json.dumps(results, indent=4)


def format_human_readable(results):
    """Format results into a human-readable string"""
    output = []
    output.append(f"Host: {results['host']}")
    output.append(f"IP: {results['ip']}")
    output.append(f"Private: {results['is_private']}")
    output.append(f"Reachable: {'✅ Yes' if results['reachable'] else '❌ No'}")
    output.append("Ports:")
    for port, status in results["ports"].items():
        if isinstance(status, str):  # when service detection is enabled
            output.append(f"  - {port}: ✅ {status}")
        else:
            output.append(f"  - {port}: {'✅ Open' if status else '❌ Closed'}")
    output.append(f"Cloud Provider: {results['cloud_provider']}")
    return "\n".join(output)
