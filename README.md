# Network and Domain Scanning Tool

## **Description**
This script integrates Nmap, FeroxBuster, and Gobuster for comprehensive network and domain scanning. It's designed for security professionals and enthusiasts to identify open ports, services, vulnerabilities, and to enumerate directories and subdomains.

## **Features**
- **Nmap Scan**: Discovers open ports and services.
- **FeroxBuster**: Bruteforces web directories.
- **Gobuster**: Enumerates DNS and VHosts.
- **Output Logging**: Logs results into a markdown file.

## **Prerequisites**
- Python 3.x
- Nmap
- FeroxBuster
- Gobuster
- Administrative privileges for `/etc/hosts` updates

## **Installation**
sudo apt-get update
sudo apt-get install python3 nmap gobuster feroxbuster

## **Usage**
Run the script with the target IP address. Options available for batch mode and output file naming.
python3 autonumerator.py -T 10.129.230.183

### **Options** (batch is still in the works
- `-T, --ip` : Target IP (required)
- `-B, --batch` : Batch mode without prompts
- `-o, --output` : Output file name (default: `scan_results.md`)

### **Host File Format**
When prompted to enter a domain name for scanning or updating the `/etc/hosts` file, ensure the format is correct:
- Format: `example.htb`
- dns/vhost: `dev`

## **Output**
All scan results are saved in the specified markdown file, detailing each step and output.

## **License**
MIT License. See `LICENSE` for details.

