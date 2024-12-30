import socket
import threading
import os

def clean_domain(domain_input):
    domain = domain_input.strip().lower()
    if domain.startswith('http://'):
        domain = domain[7:]
    elif domain.startswith('https://'):
        domain = domain[8:]
    if domain.startswith('www.'):
        domain = domain[4:]
    return domain

def domain_to_ip(domain, unique_ips, duplicate_ips):
    try:
        ip_address = socket.gethostbyname(domain)
        if ip_address not in unique_ips:
            unique_ips.add(ip_address)
            print(f"{domain} > {ip_address}")
        else:
            duplicate_ips.add(ip_address)
            print(f"Duplicate: {domain} > {ip_address}")
    except socket.gaierror:
        pass

def save_to_file(file_name, result_list):
    try:
        with open(file_name, 'w') as file:
            for line in result_list:
                file.write(line + "\n")
        print(f"\nResults saved to {file_name}")
    except Exception as e:
        print(f"Error saving to file: {e}")

def main():
    print("Welcome to Mass Domain to IP Tool!")
    print("Created By https://github.com/pengodehandal/Mass-Domain-To-IP")
    
    file_name = input("Please enter the filename containing the domains (e.g., domains.txt): ").strip()
    if not os.path.isfile(file_name):
        print(f"The file {file_name} does not exist. Please check the file path and try again.")
        return
    
    with open(file_name, 'r') as file:
        domains = [line.strip() for line in file.readlines()]
    
    output_file_name = input("Enter the output filename for IP addresses (press Enter to use default 'DomainToIPS.txt'): ").strip()
    if not output_file_name:
        output_file_name = "DomainToIPS.txt"

    result_list = []
    duplicate_ips = set()
    unique_ips = set()

    threads = []

    print("\nProcessing domains...\n")

    for domain in domains:
        domain = clean_domain(domain)
        thread = threading.Thread(target=domain_to_ip, args=(domain, unique_ips, duplicate_ips))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    result_list = list(unique_ips)
    save_to_file(output_file_name, result_list)
    save_to_file("duplicateips.txt", list(duplicate_ips))

if __name__ == "__main__":
    main()
