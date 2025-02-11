# Att-ckWeb

This project combines the best of TomNomNom and ProjectDiscovery tools into one advanced vulnerability scanner. It performs:

- **Subdomain Enumeration:** Using Assetfinder and Subfinder.
- **Live Host Filtering:** Via HTTPX.
- **URL Harvesting:** Using WaybackURLs.
- **Endpoint Crawling:** With GoSpider.
- **Vulnerability Scanning:** Via nuclei and a custom payload-based module.
- **Report Generation:** (Optionally integrated with OpenAI for smart summaries.)

## Prerequisites

- **Python 3.9+**
- **Go Environment** (for installing external tools)
- Install the following tools:
  - [Assetfinder](https://github.com/tomnomnom/assetfinder)
  - [Subfinder](https://github.com/projectdiscovery/subfinder)
  - [HTTPX](https://github.com/projectdiscovery/httpx)
  - [WaybackURLs](https://github.com/tomnomnom/waybackurls)
  - [GoSpider](https://github.com/gospidertool/gospider)
  - [Nuclei](https://github.com/projectdiscovery/nuclei)

## Setup

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd advanced-web-scanner
