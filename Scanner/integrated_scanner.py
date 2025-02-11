#!/usr/bin/env python3
import subprocess
import os
import logging
import json
import argparse

# Helper function to run shell commands
def run_command(command, capture_output=True):
    try:
        result = subprocess.run(
            command, shell=True, capture_output=capture_output, text=True, check=True
        )
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running command: {command}\n{e}")
        return []

# Enumerate subdomains using assetfinder and subfinder
def get_subdomains(domain):
    subdomains = set()
    logging.info("[*] Running assetfinder...")
    assetfinder_cmd = f"assetfinder --subs-only {domain}"
    subdomains.update(run_command(assetfinder_cmd))
    
    logging.info("[*] Running subfinder...")
    subfinder_cmd = f"subfinder -d {domain} -silent"
    subdomains.update(run_command(subfinder_cmd))
    
    return list(subdomains)

# Filter live hosts using httpx
def filter_live_hosts(hosts):
    live_hosts = []
    if not hosts:
        return live_hosts
    hosts_str = "\n".join(hosts)
    logging.info("[*] Filtering live hosts using httpx...")
    try:
        with open("hosts.txt", "w") as f:
            f.write(hosts_str)
        httpx_cmd = "cat hosts.txt | httpx -silent"
        live_hosts = run_command(httpx_cmd)
        os.remove("hosts.txt")
    except Exception as e:
        logging.error(f"Error filtering live hosts: {e}")
    return live_hosts

# Harvest historical URLs using waybackurls
def get_wayback_urls(domain):
    logging.info("[*] Running waybackurls...")
    wayback_cmd = f"echo {domain} | waybackurls"
    urls = run_command(wayback_cmd)
    return urls

# Crawl endpoints using gospider
def run_gospider(url):
    logging.info(f"[*] Running gospider on {url}...")
    gospider_output_file = "gospider_output.txt"
    gospider_cmd = f"gospider -s {url} -o {gospider_output_file} -q"
    run_command(gospider_cmd, capture_output=False)
    urls = []
    try:
        with open(gospider_output_file, "r") as f:
            urls = f.read().splitlines()
        os.remove(gospider_output_file)
    except Exception as e:
        logging.error(f"Error reading gospider output: {e}")
    return urls

# Run nuclei for vulnerability scanning
def run_nuclei(urls):
    logging.info("[*] Running nuclei for vulnerability scanning...")
    nuclei_results = []
    if not urls:
        return nuclei_results
    try:
        with open("urls.txt", "w") as f:
            f.write("\n".join(urls))
        nuclei_cmd = "cat urls.txt | nuclei -silent -o nuclei_output.txt"
        run_command(nuclei_cmd, capture_output=False)
        with open("nuclei_output.txt", "r") as f:
            nuclei_results = f.read().splitlines()
        os.remove("urls.txt")
        os.remove("nuclei_output.txt")
    except Exception as e:
        logging.error(f"Error running nuclei: {e}")
    return nuclei_results

# Run custom vulnerability scan with extensive payloads
def custom_vulnerability_scan(urls):
    logging.info("[*] Running custom vulnerability scanner...")
    try:
        from vulnerability_scanner import scan_url_list
        return scan_url_list(urls)
    except Exception as e:
        logging.error(f"Error running custom vulnerability scan: {e}")
        return []

# Aggregate results from all modules
def aggregate_results(subdomains, live_hosts, wayback_urls, gospider_urls, nuclei_results, custom_results):
    aggregated = {
        "subdomains": subdomains,
        "live_hosts": live_hosts,
        "wayback_urls": wayback_urls,
        "gospider_urls": gospider_urls,
        "nuclei_results": nuclei_results,
        "custom_results": custom_results,
    }
    return aggregated

def main(domain):
    logging.info(f"Starting integrated scan for: {domain}")
    
    # Step 1: Enumerate subdomains
    subdomains = get_subdomains(domain)
    logging.info(f"Discovered {len(subdomains)} subdomains.")
    
    # Step 2: Filter live hosts
    live_hosts = filter_live_hosts(subdomains)
    logging.info(f"Filtered {len(live_hosts)} live hosts.")
    
    # Step 3: Harvest historical URLs
    wayback_urls = get_wayback_urls(domain)
    logging.info(f"Collected {len(wayback_urls)} URLs from waybackurls.")
    
    # Step 4: Crawl endpoints via gospider for each live host
    gospider_urls = []
    for host in live_hosts:
        urls = run_gospider(host)
        gospider_urls.extend(urls)
    gospider_urls = list(set(gospider_urls))
    logging.info(f"Discovered {len(gospider_urls)} endpoints via gospider.")
    
    # Step 5: Combine all URLs for vulnerability scanning
    all_urls = list(set(wayback_urls + gospider_urls))
    logging.info(f"Aggregated {len(all_urls)} unique URLs for vulnerability scanning.")
    
    # Step 6: Run nuclei vulnerability scanning
    nuclei_results = run_nuclei(all_urls)
    logging.info(f"Nuclei found {len(nuclei_results)} potential vulnerabilities.")
    
    # Step 7: Run custom payload-based vulnerability scanning
    custom_results = custom_vulnerability_scan(all_urls)
    logging.info(f"Custom scanner found {len(custom_results)} issues.")
    
    # Aggregate everything and save results
    results = aggregate_results(subdomains, live_hosts, wayback_urls, gospider_urls, nuclei_results, custom_results)
    with open("aggregated_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    logging.info("Integrated scan complete. Results saved to aggregated_results.json")
    
    # Optionally, you can use OpenAI integration to summarize the findings here:
    try:
        from openai_integration import generate_summary
        summary = generate_summary(custom_results)
        logging.info("OpenAI Summary:\n" + summary)
    except Exception as e:
        logging.error(f"Error generating OpenAI summary: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Integrated Advanced Scanner using TomNomNom & ProjectDiscovery tools"
    )
    parser.add_argument("-d", "--domain", required=True, help="Target domain to scan (e.g., example.com)")
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO)
    main(args.domain)
