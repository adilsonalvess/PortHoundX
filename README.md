# 🛠️ PortHoundX - Your Tool for Network Insights

## 🚀 Getting Started

Welcome to PortHoundX, a powerful tool designed for smart network diagnostics on Linux and EC2. With multi-port scanning, service detection, and cloud-aware troubleshooting, PortHoundX makes diagnosing network issues easy with both a command-line interface (CLI) and a graphical user interface (GUI).

## 📦 Download Now

[![Download PortHoundX](https://img.shields.io/badge/Download-Now-brightgreen)](https://github.com/adilsonalvess/PortHoundX/releases)

## 🔍 What Is PortHoundX?

PortHoundX helps you discover service issues in your network by scanning multiple ports at once. Whether you are managing a local server or cloud services, this tool detects services running on your system, making problem-solving simpler. It’s perfect for users in the devops field or those managing multi-cloud environments.

## ⚙️ Features

- **Multi-Port Scanning:** Scan several ports simultaneously to save time.
- **Service Detection:** Identify publicly accessible services on selected ports.
- **Cloud Compatibility:** Works well with AWS, GCP, and other cloud providers.
- **User-Friendly Interface:** Choose between CLI and GUI for your comfort.
- **SSH Troubleshooting:** Simplify your troubleshooting tasks over SSH.

## 🌟 System Requirements

- **OS:** Linux (Ubuntu, CentOS, etc.) or an EC2 instance running Linux.
- **Python Version:** 3.6 or higher.
- **RAM:** Minimum 1 GB recommended.
- **Disk Space:** At least 100 MB free.

## 🔄 Installation Steps

1. **Visit Releases Page**  
   Go to the following link: [Visit this page to download](https://github.com/adilsonalvess/PortHoundX/releases).

2. **Select Your Version**  
   Look for the latest version at the top of the page. Click on it to see all available files.

3. **Download the Application**  
   Locate the appropriate file for your system (CLI or GUI version). Click to download.

4. **Install the Application**  
   Depending on your system, you may need to extract the downloaded file. If it's a zip or tar file, use the command:
   ```bash
   unzip PortHoundX.zip
   ```
   or 
   ```bash
   tar -xvf PortHoundX.tar.gz
   ```

5. **Run PortHoundX**  
   Open your terminal, navigate to the extracted directory, and execute:
   ```bash
   python3 porthoundx.py
   ```
   Or, for the GUI version, double-click on the application file.

## 📋 Usage Instructions

- Once you launch PortHoundX, you can start a scan by entering the command:
  ```bash
  ./porthoundx --scan [IP Address] --ports [Port Range]
  ```
- Replace `[IP Address]` with the target's address and `[Port Range]` with the ports you want to scan, e.g., `1-65535`.

## 🔧 Troubleshooting

If you experience issues:

1. **Check Dependencies:** Ensure you have Python 3.6 or higher installed.
2. **Network Connection:** Verify your internet connection if using cloud services.
3. **Review Logs:** Check the application logs for detailed error messages.

## 🤝 Support & Contribution

We appreciate your feedback. If you have questions or issues, please submit a ticket in the Issues section of the repository. Contributions are welcome as well; feel free to fork the repository and submit a pull request for enhancements!

## 📚 Additional Resources

- Official Documentation: [Complete user guide and advanced features](#)
- Community Discussions: Join our discussions on [GitHub Discussions](#)
- Video Tutorials: Watch how-to videos on our [YouTube Channel](#)

## ⚖️ License

PortHoundX is open-source software licensed under the MIT License. You can freely use and modify it for personal or commercial projects.

## 📅 Stay Updated

Follow us for updates:
- GitHub: [PortHoundX](https://github.com/adilsonalvess/PortHoundX)
- Twitter: [@PortHoundX](#)