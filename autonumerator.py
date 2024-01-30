import argparse
import subprocess
import signal
import os
import sys

# Function to get the ANSI color codes for your Zsh theme
def get_color_codes():
    try:
        color_codes = {
            "reset": "\033[0m",
            "red": "\033[31m",
            "green": "\033[32m",
            "yellow": "\033[33m",
            "blue": "\033[34m",
            "magenta": "\033[35m",
            "cyan": "\033[36m",
            "white": "\033[37m",
        }
        return color_codes
    except Exception as e:
        print(f"Error getting color codes: {str(e)}")
        sys.exit(1)

# Function to print colored text to the terminal
def print_colored(text, color):
    color_codes = get_color_codes()
    if color in color_codes:
        print(f"{color_codes[color]}{text}{color_codes['reset']}")
    else:
        print(text)

# Function to print a markdown-style section title with #
def print_section_title(title):
    print_colored(f"\n# {title}\n", "magenta")

def run_command(command, output_file, description, show_results=True, show_errors=True, return_output=False):
    def interrupt_handler(signum, frame):
        print_colored(f"\n{description} interrupted.", "red")
        process.kill()
        raise KeyboardInterrupt

    signal.signal(signal.SIGINT, interrupt_handler)  # Handle Ctrl + C
    with open(output_file, "a") as file:
        file.write(f"\n# {description}\n\n")
        file.write("```shell\n")
        file.write(f"Running: {description}\n")
        file.write(f"Command: {' '.join(command)}\n")
    
    output_lines = []
    process = subprocess.Popen(
        command,
        text=True,
        stderr=subprocess.STDOUT if show_errors else subprocess.DEVNULL,
        stdout=subprocess.PIPE
    )

    try:
        for line in iter(process.stdout.readline, ''):
            with open(output_file, "a") as file:
                if show_results:
                    file.write(line)
                if return_output:
                    output_lines.append(line.strip())
                print(line.strip())  # Print the output to the terminal

        process.stdout.close()
        process.wait()

    except KeyboardInterrupt:
        # Handle any cleanup here if necessary
        pass

    with open(output_file, "a") as file:
        file.write("```\n")

    return output_lines

def ask_to_run_tool(description):
    response = input(f"Do you want to run {description}? (y/n): ").lower()
    return response in ["y", "yes"]

def update_hosts_file(ip, hostname):
    try:
        with open("/etc/hosts", "a") as hosts_file:
            hosts_file.write(f"{ip} {hostname}\n")
        print_colored(f"Updated /etc/hosts with {ip} {hostname}", "green")
    except PermissionError:
        print_colored("Permission denied. Please run the script with administrative privileges to update /etc/hosts.", "red")

def main():
    parser = argparse.ArgumentParser(description='Nmap, FeroxBuster, and Gobuster Scanning Tool')
    parser.add_argument('-T', '--ip', help='IP address', required=True)
    parser.add_argument('-B', '--batch', action='store_true', help='Run all tools without asking')
    parser.add_argument('-o', '--output', help='Output file name (default: scan_results.md)', default='scan_results.md')
    args = parser.parse_args()

    output_file = args.output

    if args.batch or ask_to_run_tool("Nmap Scan"):
        run_command(["nmap", "-sCV", "-T4", args.ip], output_file, "Nmap Scan Results")

    domain = input("Enter Domain Name for Scanning: ")
    update_hosts_file(args.ip, domain)

    if args.batch or ask_to_run_tool("FeroxBuster"):
        run_command(["feroxbuster", "-u", f"http://{domain}", "-x", "pdf,js,html,php,txt,json,docx", "-C", "404", "-v"], output_file, "FeroxBuster Results", show_errors=False)

    wordlist = "/usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-110000.txt"
    
    try:
        if args.batch or ask_to_run_tool("Gobuster DNS"):
            run_command(["gobuster", "dns", "-d", domain, "-w", wordlist, "-q", "-t", "35"], output_file, "Gobuster DNS Results", show_results=True, return_output=True)

        if args.batch or ask_to_run_tool("Gobuster Vhost"):
            run_command(["gobuster", "vhost", "-u", f"http://{domain}", "-w", wordlist, "-q", "-t", "35", "--append-domain"], output_file, "Gobuster Vhost Results", show_results=True, return_output=True)

    except KeyboardInterrupt:
        print_colored("\nMoving to the next step.", "yellow")

    subdomain = input("Enter identified dns or vhost name (leave blank if none): ")
    if subdomain:
        update_hosts_file(args.ip, f"{subdomain}.{domain}")

    # Run FeroxBuster with the added subdomain
    if subdomain:
        if args.batch or ask_to_run_tool("FeroxBuster"):
            run_command(["feroxbuster", "-u", f"http://{subdomain}.{domain}", "-x", "pdf,js,html,php,txt,json,docx", "-C", "404", "-v"], output_file, "FeroxBuster Results", show_errors=False)

    print_colored(f"Scanning complete. Results saved to {output_file}", "green")

if __name__ == '__main__':
    main()
