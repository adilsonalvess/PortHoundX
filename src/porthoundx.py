import argparse
import tkinter as tk
from tkinter import scrolledtext, messagebox
import utils


class PortHoundXDiagnostics:
    def __init__(self, host, ports, detect_services=False):
        self.host = host
        self.ports = ports
        self.detect_services = detect_services

    def run(self, json_output=False):
        ip = utils.resolve_host(self.host)
        is_private = utils.is_private_ip(ip)
        reachable = utils.is_reachable(ip)

        results = {
            "host": self.host,
            "ip": ip,
            "is_private": is_private,
            "reachable": reachable,
            "ports": {},
            "cloud_provider": utils.detect_cloud_provider(ip),
        }

        # Scan ports
        for port in self.ports:
            status = utils.scan_port(ip, port)
            results["ports"][port] = status

            # If enabled, detect service type
            if self.detect_services and status:
                service = utils.detect_service(ip, port)
                results["ports"][port] = f"Open ({service})"

        if json_output:
            return utils.to_json(results)
        else:
            return utils.format_human_readable(results)


# ---------------- CLI Handling ----------------
def cli_mode(args):
    diag = PortHoundXDiagnostics(args.host, args.ports, detect_services=args.detect_services)
    output = diag.run(json_output=args.json)
    print(output)


# ---------------- GUI Handling ----------------
def gui_mode():
    def run_diagnostics():
        host = entry_host.get().strip()
        ports_input = entry_ports.get().strip()

        if not host:
            messagebox.showerror("Error", "Host cannot be empty.")
            return

        try:
            ports = [int(p.strip()) for p in ports_input.split(",") if p.strip()]
        except ValueError:
            messagebox.showerror("Error", "Ports must be integers separated by commas.")
            return

        diag = PortHoundXDiagnostics(host, ports, detect_services=var_services.get())
        output = diag.run(json_output=var_json.get())

        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, output)

    root = tk.Tk()
    root.title("PortHoundX - Multi-Cloud Diagnostics")

    tk.Label(root, text="Host/IP/DNS:").grid(row=0, column=0, sticky="w")
    entry_host = tk.Entry(root, width=40)
    entry_host.grid(row=0, column=1)

    tk.Label(root, text="Ports (comma-separated):").grid(row=1, column=0, sticky="w")
    entry_ports = tk.Entry(root, width=40)
    entry_ports.insert(0, "22,80,443,3306")  # Default common ports
    entry_ports.grid(row=1, column=1)

    var_services = tk.BooleanVar()
    tk.Checkbutton(root, text="Detect Services", variable=var_services).grid(row=2, column=0, sticky="w")

    var_json = tk.BooleanVar()
    tk.Checkbutton(root, text="JSON Output", variable=var_json).grid(row=2, column=1, sticky="w")

    tk.Button(root, text="Run Diagnostics", command=run_diagnostics).grid(row=3, column=0, columnspan=2, pady=5)

    text_output = scrolledtext.ScrolledText(root, width=80, height=20)
    text_output.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    root.mainloop()


# ---------------- Main Entry ----------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PortHoundX - Multi-Cloud Diagnostics Tool")

    parser.add_argument("--host", help="Host or IP address to scan")
    parser.add_argument("--ports", nargs="+", type=int, default=[22, 80, 443], help="Ports to scan")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument("--detect-services", action="store_true", help="Detect running services")
    parser.add_argument("--gui", action="store_true", help="Run in GUI mode")

    args = parser.parse_args()

    if args.gui:
        gui_mode()
    elif args.host:
        cli_mode(args)
    else:
        parser.error("Either --host (for CLI) or --gui must be provided.")
