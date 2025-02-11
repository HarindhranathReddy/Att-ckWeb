# Att-ckWeb

# Advanced Web Scanner

An integrated, open-source vulnerability scanner that combines the best of TomNomNom and ProjectDiscovery tools with custom payload testing and AI-powered analysis. This tool:

- **Enumerates Subdomains** using [assetfinder](https://github.com/tomnomnom/assetfinder) and [subfinder](https://github.com/projectdiscovery/subfinder).
- **Filters Live Hosts** using [httpx](https://github.com/projectdiscovery/httpx).
- **Harvests Historical URLs** via [waybackurls](https://github.com/tomnomnom/waybackurls).
- **Crawls Endpoints** using [gospider](https://github.com/gospidertool/gospider).
- **Performs Vulnerability Scanning** with both [nuclei](https://github.com/projectdiscovery/nuclei) and a custom payload-based module.
- **Analyzes HTTP Interactions** using the OpenAI API for expert vulnerability insights.
- **(Optional) Provides a Web Dashboard** built with Flask to view results.

> **Disclaimer:**  
> Use this tool responsibly and only for authorized penetration testing. The code is for educational and authorized testing purposes only.

## Prerequisites

- **Python 3.9+**
- **Go Environment** (for installing external tools)
- Install the following tools (available via `go install`):
  - [Assetfinder](https://github.com/tomnomnom/assetfinder)
  - [Subfinder](https://github.com/projectdiscovery/subfinder)
  - [HTTPX](https://github.com/projectdiscovery/httpx)
  - [WaybackURLs](https://github.com/tomnomnom/waybackurls)
  - [GoSpider](https://github.com/gospidertool/gospider)
  - [Nuclei](https://github.com/projectdiscovery/nuclei)

## Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd advanced-web-scanner
